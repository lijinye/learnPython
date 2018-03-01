# -*- coding:utf-8 -*-
# 取爬糗事百科用户地址信息，经过百度地图API转换成经纬度，最后通过BDP进行地图上的可视化

import requests
from bs4 import BeautifulSoup
import json
import csv
import re

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
           'Referer':'www.lijinye.com'}

f=open('location.csv','w',newline='',encoding='utf-8')
writer=csv.writer(f)
writer.writerow(('address','longitude','latitude'))
def get_info(url1):
    res = requests.get(url1, headers=headers)
    soup = BeautifulSoup(res.text, 'lxml')
    detail_urls = soup.select('div.author.clearfix > a:nth-of-type(2)')
    for detail_url in detail_urls:
        detail_url = 'https://www.qiushibaike.com' + detail_url.get('href')
        res_detail = requests.get(detail_url, headers=headers)
        soup_detail = BeautifulSoup(res_detail.text, 'lxml')
        have_detail=re.findall('<input type="hidden" value="(\d)"/>',str(soup_detail))
        if have_detail[0]=='0':
            address_info=soup_detail.select('div.user-col-left > div:nth-of-type(2) > ul > li:nth-of-type(4)')[0]
            # print('stripped_strings',list(address_info.stripped_strings))
            if len(list(address_info.stripped_strings))==2 and list(address_info.stripped_strings)[1]!='未知':     #<li><span>故乡:</span>内蒙古 · 赤峰</li>
                address=list(address_info.stripped_strings)[1].split('·')[1].strip()
                get_location(address)
            else:
                pass  #地址未知或没有

        else:
            pass    #没有详情


def get_location(address):
    api='http://api.map.baidu.com/geocoder/v2/'
    # print(address)
    par = {'address': address, 'output': 'json', 'ak': 'MgZOvjxWYQkEvn4SQsGtHeTsGV5n9DOA'}
    res=requests.get(api,par,headers=headers)
    # res=requests.get('http://api.map.baidu.com/geocoder/v2?ak=MgZOvjxWYQkEvn4SQsGtHeTsGV5n9DOA&output=json&address='+address,headers=headers)
    resp=json.loads(res.text)
    # print(resp)
    if resp['status']==0:
        writer.writerow((address,resp['result']['location']['lng'],resp['result']['location']['lat']))
    else:
        pass

if __name__ == '__main__':
    urls = ['https://www.qiushibaike.com/8hr/page/{0}/'.format(i) for i in range(1, 14)]
    for url in urls:
        get_info(url)
    f.close()