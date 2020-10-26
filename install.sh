#!/bin/bash
yum install -y expect
echo "start to install DCE automatically"

touch command.sh
echo 'bash -c "$(docker run -v /var/run/docker.sock:/var/run/docker.sock --rm daocloud.io/daocloud/dce:4.0.2-33456  install ) "' > command.sh
chmod +x ./command.sh

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

while [ -n "$1" ]; do
case $1 in
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

if [[ $nums -lt 6 && $nums -gt 0 ]]
then
  echo "cluster sizing select correctly"
else
  echo "please confirm -n option cluster sizing select corectly"
  exit
fi



expect <<!
set timeout -1
spawn ./command.sh

expect {Install DaoCloud Enterprise}
send "Y\r"
expect {Please select network driver}
send "\r"
expect {the system will be installed}
send "y\r"

expect {for 'internal_management' interface :}
send "$internal\r"
expect {for 'outbound' interface :}
send "$outbound\r"
expect {for 'internal_ovs' interface :}
send "$ovs\r"
expect {for 'internal_calico' interface :}
send "$calico\r"
expect {for 'internal_storage' interface :}
send "$storage\r"
expect {for 'login' interface :}
send "$login\r"
expect {please confirm the above information}
send "y\r"


expect {HOST_NAME}
send "y\r"
expect {DNS_SERVER_LIST}
send "y\r"
expect {Please select VIP provider solution}
send "$LB\r"
expect {Please specify controller VIP:}
send "$vip\r"
expect {Please specify registry VIP:}
send "$registry\r"
expect {Please select type of storage}
send "1\r"
expect {Please select image scan driver}
send "$clair\r"
expect {Please select cluster sizing}
send "$nums\r"
expect {Please select reliability_level level}
send "$level\r"
expect {Do you want to start DaoCloud Enterprise deployment now?}
send "Y\r"

expect eof
!

