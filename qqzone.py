# -*- coding:utf-8 -*-
# 使用selenium模拟登录qq邮箱获取好友邮箱并导出到本地

from selenium import webdriver
import csv
import time

def get_info(url):
    '''
    :param url: qq邮箱地址
    :return:
    '''
    options = webdriver.ChromeOptions()
    options.add_argument(
        'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36')
    driver = webdriver.Chrome(chrome_options=options)
    driver.get(url)
    driver.implicitly_wait(4)
    # print(driver.page_source)
    #输入用户名密码登录
    if driver.find_element_by_id('login_frame'):
        driver.switch_to.frame('login_frame')
        driver.find_element_by_id('u').clear()
        driver.find_element_by_id('u').send_keys('284875929')
        driver.find_element_by_id('p').clear()
        driver.find_element_by_id('p').send_keys('LJYljy60944493')
        driver.find_element_by_id('login_button').click()
    #点击通讯录
    driver.maximize_window()
    driver.find_element_by_xpath('//*[@id="navBarTd"]/li[3]/a').click()
    # time.sleep(1)
    time.sleep(1)
    # 点击工具
    driver.switch_to.frame('mainFrame')
    driver.find_element_by_xpath('//*[@id="bar"]/div/div[1]/div[2]/a[3]').click()
    time.sleep(1)
    #点击到导出联系人
    driver.find_element_by_xpath('//*[@id="import_QMMenu__menuitem_COM_EXPORT"]').click()
    time.sleep(1)
    #选择CSV格式导出
    driver.switch_to.default_content()
    driver.find_element_by_xpath('//*[@id="qMDiAlog_iMpoRt_QMDialog_import"]/div/ul/li[2]/div/p[2]/label/input').click()
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="qMDiAlog_iMpoRt_QMDialog_geConfirmBtn"]').click()
    time.sleep(1)
    driver.execute_script('alert("操作完毕，5秒后自动关闭")')
    time.sleep(5)
    driver.quit()
if __name__ == '__main__':
    get_info('https://mail.qq.com/')
