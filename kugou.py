# -*- coding:utf-8 -*-
#爬取酷狗榜单中TOP500的信息
import requests
from bs4 import BeautifulSoup

headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}

def get_info(url):
    req=requests.get(url,headers=headers)
    #print(req.request.headers)
    soup=BeautifulSoup(req.text,'lxml')
    songandsingers=soup.select('.pc_temp_songname')
    #print('songandsingers',songandsingers)
    times=soup.select('.pc_temp_time')
    #print('times',times)
    ranks=soup.select('.pc_temp_num')
    #print('ranks',ranks)
    for rank,time,songandsinger in zip(ranks,times,songandsingers):
        data={
            'time':time.get_text().strip(),
            'song':songandsinger.get_text().split('-')[1].strip(),
            'singer':songandsinger.get_text().split('-')[0].strip(),
            'rank':rank.get_text().strip()
        }
        print(data)

if __name__=='__main__':
    urls=['http://www.kugou.com/yy/rank/home/{0}-8888.html?from=rank'.format(i) for i in range(1,20)]
    for url in urls:
        get_info(url)