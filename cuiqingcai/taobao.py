# -*- coding:utf-8 -*-

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from urllib.parse import quote
from pyquery import PyQuery as pq
import pymongo

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
browser = webdriver.Chrome(chrome_options=chrome_options)
wait = WebDriverWait(browser, 10)
KEYWORD = 'ipad'
MAX_PAGE = 10
client = pymongo.MongoClient('localhost')
db = client['taobao']


def index_page(page):
    """
    抓取索引页
    :param page:页码
    :return:
    """
    print("正在爬取第", page, "页")
    try:
        url = 'https://s.taobao.com/search?q=' + quote(KEYWORD)
        browser.get(url)
        if page > 1:
            input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager div.form > input')))
            submit = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager div.form > span.btn.J_Submit')))
            input.clear()
            input.send_keys(page)
            submit.click()
        wait.until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#mainsrp-pager li.item.active > span'), str(page)))
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.m-itemlist .items .item')))
        get_products()
    except TimeoutException:
        index_page(page)


def get_products():
    """
    提取商品数据
    :return:
    """
    html = browser.page_source
    doc = pq(html)
    # print(doc('.m-itemlist .items .item'))
    items = doc('.m-itemlist .items .item').items()
    for item in items:
        # print('item==',items.html())
        product = {
            'image': item.find('.pic .img').attr('data-src'),
            'price': item.find('.price').text().replace('\n',''),
            'deal': item.find('.deal-cnt').text(),
            'title': item.find('.title').text().replace('\n',','),
            'shop': item.find('.shop').text(),
            'location': item.find('.location').text()
        }
        print(product)
        save_to_mongo(product)


def save_to_mongo(product):
    """
    保存至mongoDB
    :param product:
    :return:
    """
    try:
        if db['products'].insert_one(product):
            print('保存成功')
    except Exception:
        print('保存失败')


def main():
    """
    遍历每一页
    :return:
    """
    for i in range(1, MAX_PAGE + 1):
        index_page(i)


if __name__ == '__main__':
    main()
