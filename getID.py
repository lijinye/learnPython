# -*- coding:utf-8 -*-
# 使用xpath爬取糗事百科用户ID,匿名用户的标签位置不一样
import requests
from lxml import etree

url = 'https://www.qiushibaike.com/text/'
res = requests.get(url)
selector = etree.HTML(res.text)
url_infos = selector.xpath('//div[starts-with(@class,"article block untagged mb15")]')
# url_infos = selector.xpath('//div[contains(@class,"article block untagged mb15")]')
for url_info in url_infos:
    print(url_info.xpath('div[1]/a[2]/h2/text()')[0].strip() if url_info.xpath('div[1]/a[2]/h2/text()') else url_info.xpath('div[1]/span[2]/h2/text()')[0])
    # if url_info.xpath('div[1]/a[2]/h2/text()'):
    #     print(url_info.xpath('div[1]/a[2]/h2/text()')[0].strip())
    # else:
    #     print(url_info.xpath('div[1]/span[2]/h2/text()')[0])
