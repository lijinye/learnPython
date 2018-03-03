# -*- coding:utf-8 -*-
#爬取豆瓣电影TOP250存入mysql

import requests
from lxml import etree
import pymysql
import re
from multiprocessing import Pool

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='mydb', charset='utf8')
cursor = conn.cursor()

def get_detail_urls(url):
    res=requests.get(url,headers=headers)
    selector=etree.HTML(res.text)
    detail_urls=selector.xpath('//div[@class="hd"]/a/@href')
    for detail_url in detail_urls:
        get_details(detail_url)


def get_details(detail_url):
    res=requests.get(detail_url,headers=headers)
    s=etree.HTML(res.text)
    try:
        name=s.xpath('//*[@id="content"]/h1/span[1]/text()')[0]
        director=s.xpath('//*[@id="info"]/span[1]/span[2]/a/text()')[0]
        actors=s.xpath('//*[@id="info"]/span[3]/span[2]')[0]
        actor=actors.xpath('string(.)')
        style=re.findall('<span property="v:genre">(.*?)</span>', res.text, re.S)
        style='/'.join(style)
        country=re.findall('<span class="pl">制片国家/地区:</span>(.*?)<br/>', res.text, re.S)[0]
        release_time=s.xpath('//*[@property="v:initialReleaseDate"]/text()')[0]
        time=s.xpath('//*[@id="info"]/span[@property="v:runtime"]/text()')[0]
        score=s.xpath('//*[@id="interest_sectl"]/div[1]/div[2]/strong/text()')[0]
        sql='insert into doubanmovies(name,director,actor,style,country,release_time,time,score) values ("%s","%s","%s","%s","%s","%s","%s","%s")' % (name,director,actor,style,country,release_time,time,score)
        # print(sql)
        cursor.execute(sql)
        conn.commit()
    except IndexError:
        pass
if __name__=='__main__':
    urls=['https://movie.douban.com/top250?start={0}&filter='.format(i) for i in range(0,226,25)]
    # pool=Pool(processes=4)
    # pool.map(get_detail_urls,urls)
    for url in urls:
        get_detail_urls(url)
    conn.close()