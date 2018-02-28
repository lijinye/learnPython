# -*- coding:utf-8 -*-
# 使用lxml爬取内容并保存到excel文件

import requests
import xlwt
from lxml import etree
import re

proxies = {'https': 'http://lwx309353:ljy@4567@openproxy.huawei.com:8080',
           'http': 'http://lwx309353:ljy@4567@openproxy.huawei.com:8080'}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'}
all_info_list = []


def get_info(url):
    res = requests.get(url, headers=headers)
    selector = etree.HTML(res.text)
    infos = selector.xpath('//*[@id="post_list"]/div')
    for info in infos:
        try:
            title = info.xpath('div[2]/h3/a/text()')[0].strip()
            author = info.xpath('div[2]/div/a/text()')[0].strip()
            time = info.xpath('div[2]/div/text()')[0].strip()
            comment = info.xpath('div[2]/div/span[1]/a/text()')[0].strip()
            view = info.xpath('div[2]/div/span[2]/a/text()')[0].strip()
            info_list = [title, author, time, comment, view]
            all_info_list.append(info_list)
        except IndexError:
            pass


if __name__ == '__main__':
    urls = ['https://www.cnblogs.com/sitehome/p/{0}'.format(i) for i in range(12, 13)]
    for u in urls:
        get_info(u)
    header = ['title', 'author', 'time', 'comment', 'view']
    book = xlwt.Workbook(encoding='utf-8')
    sheet = book.add_sheet('sheet1')
    for h in range(len(header)):
        sheet.write(0, h, header[h])
    i = 1
    print(all_info_list)
    for list in all_info_list:
        j = 0
        for data in list:
            sheet.write(i, j, data)
            j += 1
        i += 1
    book.save('bokeyuan.xls')
