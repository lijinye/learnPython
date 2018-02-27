# -*- coding:utf-8 -*-
#爬取斗破苍穹小说，并存储到本地文件中

import requests
import re

headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
f=open('斗破苍穹.txt','a+',encoding='utf-8')
def get_info(url):
    res=requests.get(url,headers=headers)
    if res.status_code==200:
        for t in re.findall('<p>(.*?)</p>',res.content.decode('utf-8'),re.S):
            f.write(t+'\n')
    else:
        pass

if __name__=='__main__':
    urls=['http://www.doupoxs.com/doupocangqiong/{0}.html'.format(i) for i in range(1,10)]
    for url in urls:
        get_info(url)
    f.close()