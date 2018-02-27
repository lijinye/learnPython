# -*- coding:utf-8 -*-
#爬取糗事百科段子信息，需要爬取的信息有用户ID，用户等级，用户性别，发表段子文字信息，好笑数量和评论数量

import requests
import re

headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}

info=[]
def get_gender(gender):
    if 'women'==gender:
        return '女'
    else:
        return '男'
def get_info(url):
    res=requests.get(url,headers=headers)
    if res.status_code==200:
        resp=res.content.decode('utf-8')
        IDs=re.findall('<h2>(.*?)</h2>',resp,re.S)
        levels=re.findall('<div class="articleGender \w+Icon">(.*?)</div>',resp)
        genders=re.findall('<div class="articleGender (.*?)Icon">',resp)
        contents=re.findall('<div class="content">.*?<span>(.*?)</span>',resp,re.S)
        laughs=re.findall('<span class="stats-vote"><i class="number">(\d+)</i>',resp)
        comments=re.findall('<i class="number">(\d+)</i> 评论',resp)
        for ID,level,gender,content,laugh,comment in zip(IDs,levels,genders,contents,laughs,comments):
            data={
                'ID':ID.strip(),
                'level':level,
                'gender':get_gender(gender),
                'content':content.strip().replace('<br/>',''),
                'laugh':laugh,
                'comment':comment
            }
            info.append(data)
    else:
        pass

if __name__=='__main__':
    urls=['https://www.qiushibaike.com/text/page/{0}/'.format(i) for i in range(1,2)]
    for url in urls:
        get_info(url)
    f = open('糗事百科.txt', 'a+', encoding='utf-8')
    # print(info)
    for info_dict in info:
        f.write(info_dict['ID']+'\n')
        f.write(info_dict['level']+'\n')
        f.write(info_dict['gender']+'\n')
        f.write(info_dict['content']+'\n')
        f.write(info_dict['laugh']+'\n')
        f.write(info_dict['comment']+'\n\n')
    f.close()