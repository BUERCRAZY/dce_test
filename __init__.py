from selenium.webdriver import Chrome
from dce_test.create_app import *


def load_driver(path='e:\webdrivers\chromedriver.exe', wait_time=10):
    driver = Chrome(path)
    driver.implicitly_wait(wait_time)
    return driver

def load_page(driver, path='http://10.6.171.139', wait_time=10):
    driver.implicitly_wait(wait_time)   
    driver.get(path)

    
def login(driver, user='admin', pw='changeme', wait_time=10):
    driver.implicitly_wait(wait_time)
    element_login = driver.find_elements_by_tag_name('input')
    element_login[0].send_keys(user)
    element_login[1].send_keys(pw)
    driver.find_element_by_tag_name('button').click()


