#!/bin/bash
yum install -y expect
echo "start to install DCE automatically"

count=1
nums=1
clair=1
level=2
LB=1
internal=1
outbound=1
ovs=1
calico=1
storage=1
login=1
version="4.0.2-33478"

while [ -n "$1" ]; do
case $1 in
  -v)version=$2;shift 2;;
  -p)para=$2;shift 2;;
  -i)vip=$2;shift 2;;
  -r)registry=$2;shift 2;;
  -n)nums=$2;shift 2;;
  -g)level=1;shift;;
  -c)clair=2;shift;;
  -l)LB=2;shift;;
  -*)echo "no such option $1";exit 1;;
  *)break;;
esac
done
echo $para

touch command.sh
echo 'bash -c "$(docker run -v /var/run/docker.sock:/var/run/docker.sock --rm daocloud.io/daocloud/dce:'$version'  install )"' > command.sh
chmod +x ./command.sh



if [ -z $vip ]
then
  echo "please enter the controller vip"
  exit
fi

if [ -z $registry ]
then
  echo "please enter the registry vip"
  exit
fi

if [ ${#para} -eq 6 ]
then
  echo "network interface confirmed"
  internal=${para:0:1}
  outbound=${para:1:1}
  ovs=${para:2:1}
  calico=${para:3:1}
  storage=${para:4:1}
  login=${para:5:1}

else
  echo "please confirm -p option network interface enter correctly"
  exit
fi

if [ $outbound !=  $internal ]
then
  count=count+1
fi
if [ $ovs != $internal ]
then
  count=count+1
  if [ $ovs == $outbound ]
  then
    echo "interface for internal_ovs should be marked with internal, or one without any mark "
    exit
  fi
fi

if [ $calico != $internal ]
then
  count=count+1
  if [ $calico == $outbound -o $calico == $ovs ]
  then
    echo "interface for calico should be marked with internal, or one without any mark"
    exit
  fi
fi

if [ $storage != $internal ]
then
  count=count+1
  if [ $storage == $calico -o $storage == $outbound -o $storage == $ovs ]
  then
    echo "interface for storage should be marked with internal, or one without any mark"
    exit
  fi
fi

if [ $login != $outbound ]
then
  count=count+1
  if [ $login == $storage -o $login == $calico -o $login == $outbound -o $login == $ovs ]
  then
    echo "interface for login should be marked with outbound, or one without any mark"
    exit
  fi
fi




if [[ $nums -lt 6 && $nums -gt 0 ]]
then
  echo "cluster sizing select correctly"
else
  echo "please confirm -n option cluster sizing select corectly"
  exit
fi


expect <<!
set timeout 5
spawn ./command.sh

expect {
  "Install DaoCloud Enterprise" {send "Y\r";exp_continue;}
  "Please select network driver" {send "\r";exp_continue;}
  "the system will be installed" {send "y\r";exp_continue}
}
expect {
  "for 'internal_management' interface" {send "$internal\r";exp_continue}
  "for 'outbound' interface" {send "$outbound\r";exp_continue}
  "for 'internal_ovs' interface" {send "$ovs\r";exp_continue}
  "for 'internal_calico' interface" {send "$calico\r";exp_continue}
  "for 'internal_storage' interface" {send "$storage\r";exp_continue}
  "for 'login' interface" {send "$login\r";exp_continue}
  "please confirm the above information" {send "y\r";exp_continue}
  "specify static route for accessing login subnet" {send "n\r";exp_continue}
  "hit "n" key to ignore checking" {send "n\r";exp_continue}
}
expect { 
  "HOST_NAME" {send "y\r";exp_continue}
  "DNS_SERVER_LIST" {send "y\r";exp_continue}
  "Install DaoCloud Enterprise" {send "Y\r";exp_continue}
  "Please select network driver" {send "\r";exp_continue}
  "the system will be installed" {send "y\r";exp_continue}
}
expect {
  "Please select VIP provider solution" {send "$LB\r";exp_continue}
  "Please specify controller VIP" {send "$vip\r";exp_continue}
  "Please specify registry VIP" {send "$registry\r";exp_continue}
  "Please select type of storage" {send "1\r";exp_continue}
  "Please select image scan driver" {send "$clair\r";exp_continue}
  "Please select cluster sizing" {send "$nums\r";exp_continue}
  "Please select reliability_level level" {send "$level\r";exp_continue}
}
set timeout -1
expect "Do you want to start DaoCloud Enterprise deployment now" 
send "Y\r"



expect eof
!

