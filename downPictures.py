# -*- coding:utf-8 -*-
# 下载华为商城商品图片

import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'}
proxies = {'https': 'http://lwx309353:ljy@4567@openproxy.huawei.com:8080',
           'http': 'http://lwx309353:ljy@4567@openproxy.huawei.com:8080'}

def get_info(url):
    res=requests.get(url,headers=headers,proxies=proxies)
    soup=BeautifulSoup(res.text,'lxml')
    picurls=soup.select('p.p-img > a > img')
    for picurl in picurls:
        purl=picurl.get('src')
        pic=requests.get(purl,headers=headers,proxies=proxies)
        f=open('F:\learnPython\pic\\'+picurl.get('alt').replace('/','-')+purl[-4:],'wb')
        f.write(pic.content)
        f.close()

if __name__=='__main__':
    urls = ['https://www.vmall.com/list-115-{0}-0-0'.format(i) for i in range(1, 6)]
    for url in urls:
        get_info(url)
