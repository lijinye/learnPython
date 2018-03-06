# -*- coding:utf-8 -*-
# 使用Selenium+chrome爬取3ms内容并写入mysql

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import pymysql

conn=pymysql.connect(host='127.0.0.1',port=3306,user='root',db='mydb',charset='utf8')
cursor=conn.cursor()

options = webdriver.ChromeOptions()
options.add_argument(
    'User-Agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3282.119 Safari/537.36')
# 设置代理
options.add_argument("--proxy-server=http://202.20.16.82:10152")
driver = webdriver.Chrome(chrome_options=options)

# driver=webdriver.PhantomJS()
# cookies_str = '_ha_ref.3ms-hi.f914=%5B%22%22%2C%22%22%2C1518509090%2C%22http%3A%2F%2Fw3.huawei.com%2Fnext%2Findexa.html%3Flocale%3Dzh%22%5D;_ha_id.3ms-hi.f914=67-1C-5E-6E-22-C0-10-CE-DD-80-3A-2E-CE-AA-89-6B; _ha_ses.3ms-hi.f914=f3110ca05ad0239592e13c65b39512d1f3b86eed; v1st=15E137F9D8C15AD7;platuserID=lwx309353; isShowTips=yes; visitorId=DC2B41B3AA524FC09DE0AC91F7CD5F56; per_last=1507529718819; AMCV_7DA25C0158C1322D0A495DB1%40AdobeOrg=1099438348%7CMCIDTS%7C17471%7CMCMID%7C29464754826455535403117560118781890482%7CMCAID%7CNONE%7CMCOPTOUT-1509445333s%7CNONE%7CvVersion%7C2.1.0; _dmpa_id=51859a36d9ed0952c4043288138121509438133449.1509438080.1.1509438080.1509438080; _ga=GA1.2.227787174.1509438133; FORUM_LOGIN_AUTH_SECURE_CODE=67-1C-5E-6E-22-C0-10-CE-0F-DF-0F-A1-97-91-C8-AD-93-43-16-F3-24-F9-68-1A-88-90-F9-38-37-CE-BC-9A-96-58-D5-A6-90-C8-20-E6-A6-D2-C5-B5-BE-9E-4A-7D-0F-C6-70-02-04-B3-7E-48; selnode=""; 2D-4A-29-3E-6C-E6-DF-76-1D-A3-0E-21-2C-88-0E-05=67-1C-5E-6E-22-C0-10-CE-0F-DF-0F-A1-97-91-C8-AD-E6-6A-0D-98-A9-19-20-C2-9E-35-CA-98-B3-6B-50-30-96-58-D5-A6-90-C8-20-E6-8D-28-4E-FF-93-5C-AC-2E; HW3MS_think_language=zh-cn; worldwide_tag=%2Fcn; lang=en; PHPSESSID=3ig7lp07i2i5a71p16osago8s3; DGGPRO3MSMMSERVICE=0000XlxiPdNwfmChO5MiEFnXm3p:dggmwc4app992_CloneID; SZXPRO3MSDOC3MS=0000PFlautcqhXvtKOA0N45WDVc:szxxap1538-mwc_CloneID; hwkm_sid=CLxH482-KLsmd-cOqggfdInG7EGSUbKr; hwkm_sid.sig=VLO8C_JwqtSskM3hdfgc5F579Dw; hwsso_login=""; HW3MS_CONNECT_SESSION=ddu7h5jkrgp9e4r94jlc2nage5; HW3MS_resourceReadedKey=GroupWiki-4580719; HW3MS_ResourceLanguage=czowOiIiOw%3D%3D'
url = 'http://3ms.huawei.com/hi/group/2034789/wikis.html?category=1266061#category=all'

driver.get(url)
driver.maximize_window()
# driver.fullscreen_window()
# driver.implicitly_wait(10)
'''''隐式等待和显示等待都存在时，超时时间取二者中较大的'''
# time.sleep(4)
# driver.delete_all_cookies()
# driver.add_cookie({'name':'hello','value':'lijinye'})
# print(driver.page_source)
# print(driver.get_cookies())
# for i in cookies_str.split(';'):
#     driver.add_cookie({'name':i.split('=')[0],'value':i.split('=')[1]})
# driver.get(url)
# time.sleep(4)
# print(driver.page_source)
a=True
while a:
    titles = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.f12.pl5 > a')))
    authors = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'td.lh16.mt5 > a')))
    createtimes = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'td.lh16.mt5 > em')))
    for title,author,createtime in zip(titles,authors,createtimes):
        sql='insert into useselenium(title,author,createtime,url) values("{0}","{1}","{2}","{3}")'.format(title.text,author.text,createtime.text,title.get_attribute('href'))
        print(sql)
        cursor.execute(sql)
        conn.commit()
    try:
        driver.find_element_by_link_text('下一页').click()
        time.sleep(1)
    except:
        a=False
# titles = driver.find_elements_by_css_selector('.f12.pl5 > a')
driver.execute_script('alert("爬取完毕,3S后自动关闭")')
time.sleep(3)
driver.quit()
conn.close()
# for title in titles:
#     print(title.text)
