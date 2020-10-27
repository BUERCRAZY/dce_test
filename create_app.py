from time import sleep


def get_menu(driver):
    menu = driver.find_element_by_class_name('sidebar')
    # dashboard, app_center, integration, workloads, network, storage, infrastructure, settings = menu.find_elements_by_class_name('menu-section')
    #  0 看板  1 应用中心  2 交付中心  3  容器管理  4 网络管理  5 存储  6 基础设施  7 设置
    # return dashboard, app_center, integration, workloads, network, storage, infrastructure, settings
    return menu.find_elements_by_class_name('menu-section')
    
    
def create_action(driver, n): # 创建应用 
    app_center=get_menu(driver)[1]
    app_center.find_element_by_class_name('name').click()  # app page
    driver.find_element_by_class_name('dao-btn.blue.has-icon').click() # click create button
    # 选择创建方式
    sleep(1)
    select_window=driver.find_element_by_class_name('dao-dialog-container')
    # print('len:', len(select_window.find_elements_by_tag_name('input')))
    create_method=select_window.find_elements_by_tag_name('input')[n]    # 0 从模版创建  1 从镜像创建  2 从yaml创建
    create_method.click()
    driver.find_element_by_class_name('dao-btn.blue.has-icon.compact').click() # continue
    

def select_image(driver, image_name, choose_image):# 0-选择镜像
    image_search=choose_image.find_element_by_class_name('dao-input-inner')
    search_input=image_search.find_element_by_tag_name('input')
    search_input.send_keys(image_name)
    clear_button=image_search.find_element_by_class_name('icon.close-icon')
    # clear_button.click()  # clear搜索框


def select_template(driver, template_name, choose_template):
    template_search=choose_template.find_element_by_class_name('dao-input-inner')
    template_input=template_search.find_element_by_tag_name('input')
    template_input.send_keys(template_name)
    clear_button=template_search.find_element_by_class_name('icon.close-icon')
    # clear_button.click()  # clear搜索框


def create_from_yaml(driver, template_name='dao-2048', app_name='dao-2048-test'):
    create_action(driver, 2) # n=2 从yaml创建
    input_area=driver.find_element_by_class_name('dao-popover-rel')
    input_app_name=input_area.find_element_by_tag_name('input')
    input_app_name.send_keys(app_name)
    
    if template_name=='dao-2048':
        select_yaml=driver.find_element_by_class_name('mt-sm')
        yaml_2048=select_yaml.find_element_by_tag_name('a')
        yaml_2048.click()
    sleep(10) 
    deploy_button=driver.find_element_by_class_name('dao-btn.blue')
    deploy_button.click()
    



def create_from_template(driver, template_name='dao-2048', app_name='dao-2048-test'):
    create_action(driver, 0) # n=0 从模版创建
    # 选择模版
    choose_template=find_steps_content(driver)[0]
    select_template(driver, template_name, choose_template)
    selected=choose_template.find_element_by_class_name('dao-card-main')
    selected.click()
    # continue
    continue_button_2(driver)
    
    # 应用信息
    chooose_name=find_steps_content(driver)[1]
    setting_section=chooose_name.find_elements_by_class_name('dao-setting-section')
    app_name=setting_section[2]
    input_app_name=app_name.find_element_by_tag_name('input')
    input_app_name.clear()
    input_app_name.send_keys('dao-2048-test')
    # continue
    continue_button_2(driver)
    
    # 变量文件
    
    
    # continue
    continue_button_2(driver)
    # 检查部署
    sleep(5)
    footer=driver.find_element_by_class_name('upload-app-footer')
    deploy_button=footer.find_element_by_class_name('dao-btn.blue')
    deploy_button.click()
    sleep(30)
    view_button=driver.find_element_by_class_name('dao-btn.has-icon.blue')
    view_button.click()
    
def continue_button_2(driver):
    footer=driver.find_element_by_class_name('upload-app-footer')
    continue_button=footer.find_element_by_class_name('dao-btn.blue.compact')
    continue_button.click()
    


def create_from_image(driver, image_name='dao-2048', app_name='dao-2048-test', service_type=0, \
    instance_num=1, cpu_limit=[0.128, 0.256], memory_limit=[128, 128], policy_list=[0,0,[0,0,25,25]]):
    create_action(driver, 1) # n=1 从镜像创建
    # step_content=driver.find_elements_by_class_name('dao-step-content')
    # 创建应用 9 步：0-选择镜像；1-应用信息；2-计算资源；3-网络资源；4-存储资源；5-调度与发布；6-容器配置；7-检查部署 8-存储资源
    # choose_image, app_info, compute_settings, network_settings, storage_null, schedule, pod_settings, check_deploy, storage_settings=step_content
    # choose_image=step_content[0]
    choose_image=find_steps_content(driver)[0]
    # 0-选择镜像
    select_image(driver, image_name, choose_image)
    
    # continue
    continue_button(driver)
    # print('image has been choosed, sleep 2 seconds')
    sleep(2)
    # 1-应用信息
    app_info=find_steps_content(driver)[1]
    app_info_setting(driver, app_info, image_name+app_name, image_name, service_type, instance_num)
    
    # continue
    continue_button(driver)
    
    # 2-计算资源
    compute_info=find_steps_content(driver)[2]
    if cpu_limit==[0.064, 0.128] and memory_limit==[256, 256]:
        pass
    else:
        compute_info_setting(driver, compute_info, cpu_limit, memory_limit)
    
    # continue
    continue_button(driver)
    
    # 3-网络资源
    #
    
    # continue
    continue_button(driver)
    
    # 4-存储资源
    #
    
    # continue
    continue_button(driver)
    # 5-调度与发布
    schedule_info=find_steps_content(driver)[5]
    schedule_policy, release_plicy, use_percent=policy_list
    if schedule_policy==0 and release_plicy ==0 and use_percent==[0, 0, 25, 25]:
        pass
    else:
        schedule_info_setting(driver, schedule_policy, release_plicy)
    
    # continue
    continue_button(driver)
    
    # 6-容器配置
    #
    
    # continue
    continue_button(driver)
    
    # 7-检查部署
    #
    
    # continue
    continue_button(driver)

   
    
    
def find_steps_content(driver):
    step_content=driver.find_elements_by_class_name('dao-step-content')
    return step_content
   
   
def continue_button(driver):
    sleep(2)
    bottom=driver.find_element_by_class_name('from-registry-footer')
    bottom.find_element_by_class_name('dao-btn.blue').click()
   
   
def app_info_setting(driver, app_info, app_name='dao-2048-test', image_name='dao-2048', service_type=0, instance_num=1):   
   # 应用信息
    #4 layout： 选择名称，扩展，标签，注解
    
    app_info_setting_layout=app_info.find_elements_by_class_name('dao-setting-layout')
    # print('len:',app_info_setting_layout)
    choose_name_layout, extension_layout, label_layout, note_layout=app_info_setting_layout
    
    ## 选择名称4 section： 镜像，应用名，服务名，服务类型
    choose_name_list=choose_name_layout.find_elements_by_class_name('dao-setting-section')
    
    
    # 应用名
    input_app_name=choose_name_list[1].find_element_by_tag_name('input')
    sleep(2)
    input_app_name.clear()
    input_app_name.send_keys(' ')
    input_app_name.clear()
    input_app_name.send_keys(app_name)

    # 服务名
    input_service_name=choose_name_list[2].find_element_by_tag_name('input')
    input_service_name.clear()
    input_service_name.send_keys(app_name+'--'+image_name)

    # 服务类型： 0-无状态；1-有状态
    input_service_type=choose_name_list[3].find_elements_by_class_name('dao-radio-simple')
    input_service_type[service_type].click()

    ## 扩展
    input_instance_num=extension_layout.find_element_by_tag_name('input')
    input_instance_num.clear()
    input_instance_num.send_keys(instance_num)

    ## 标签
    
    
    ## 注解
    

# 2-计算资源   #内存单位未选择
def compute_info_setting(driver, compute_info, cpu_limit, memory_limit):
    compute_limit=compute_info.find_elements_by_class_name('dark-form')
    
    cpu_input=compute_limit[0].find_elements_by_tag_name('input')
    cpu_request_input, cpu_limit_input=cpu_input
    cpu_request_input.clear()
    #cpu_request_input.click()
    cpu_request_input.send_keys(str(cpu_limit[0]))
    cpu_limit_input.clear()
    #cpu_limit_input.click()
    cpu_limit_input.send_keys(str(cpu_limit[1]))
    
    memory_input=compute_limit[1].find_elements_by_tag_name('input')
    memory_request_input, memory_limit_input=memory_input
    memory_request_input.clear()
    memory_request_input.send_keys(str(memory_limit[0]))
    memory_limit_input.clear()
    memory_limit_input.send_keys(str(memory_limit[1]))
    
    



