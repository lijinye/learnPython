# -*- coding:utf-8 -*-
# 使用lxml爬取内容并保存到csv文件
import requests
from lxml import etree
import csv

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'}
cookies_str = '_ha_ref.3ms-hi.f914=%5B%22%22%2C%22%22%2C1518509090%2C%22http%3A%2F%2Fw3.huawei.com%2Fnext%2Findexa.html%3Flocale%3Dzh%22%5D;_ha_id.3ms-hi.f914=67-1C-5E-6E-22-C0-10-CE-DD-80-3A-2E-CE-AA-89-6B; _ha_ses.3ms-hi.f914=f3110ca05ad0239592e13c65b39512d1f3b86eed; v1st=15E137F9D8C15AD7;platuserID=lwx309353; isShowTips=yes; visitorId=DC2B41B3AA524FC09DE0AC91F7CD5F56; per_last=1507529718819; AMCV_7DA25C0158C1322D0A495DB1%40AdobeOrg=1099438348%7CMCIDTS%7C17471%7CMCMID%7C29464754826455535403117560118781890482%7CMCAID%7CNONE%7CMCOPTOUT-1509445333s%7CNONE%7CvVersion%7C2.1.0; _dmpa_id=51859a36d9ed0952c4043288138121509438133449.1509438080.1.1509438080.1509438080; _ga=GA1.2.227787174.1509438133; FORUM_LOGIN_AUTH_SECURE_CODE=67-1C-5E-6E-22-C0-10-CE-0F-DF-0F-A1-97-91-C8-AD-93-43-16-F3-24-F9-68-1A-88-90-F9-38-37-CE-BC-9A-96-58-D5-A6-90-C8-20-E6-A6-D2-C5-B5-BE-9E-4A-7D-0F-C6-70-02-04-B3-7E-48; selnode=""; 2D-4A-29-3E-6C-E6-DF-76-1D-A3-0E-21-2C-88-0E-05=67-1C-5E-6E-22-C0-10-CE-0F-DF-0F-A1-97-91-C8-AD-E6-6A-0D-98-A9-19-20-C2-9E-35-CA-98-B3-6B-50-30-96-58-D5-A6-90-C8-20-E6-8D-28-4E-FF-93-5C-AC-2E; HW3MS_think_language=zh-cn; worldwide_tag=%2Fcn; lang=en; PHPSESSID=3ig7lp07i2i5a71p16osago8s3; DGGPRO3MSMMSERVICE=0000XlxiPdNwfmChO5MiEFnXm3p:dggmwc4app992_CloneID; SZXPRO3MSDOC3MS=0000PFlautcqhXvtKOA0N45WDVc:szxxap1538-mwc_CloneID; hwkm_sid=CLxH482-KLsmd-cOqggfdInG7EGSUbKr; hwkm_sid.sig=VLO8C_JwqtSskM3hdfgc5F579Dw; hwsso_login=""; HW3MS_CONNECT_SESSION=ddu7h5jkrgp9e4r94jlc2nage5; HW3MS_resourceReadedKey=GroupWiki-4580719; HW3MS_ResourceLanguage=czowOiIiOw%3D%3D'
cookie = {}
for i in cookies_str.split(';'):
    cookie[i.split('=')[0]] = i.split('=')[1]

info = []


def get_link(single_url):
    res = requests.get(single_url, headers=headers, cookies=cookie)
    soup = etree.HTML(res.text)
    detail_links = soup.xpath('//*[@id="wikiList"]/table/tr[@class="w_b"]')
    for detail_link in detail_links:
        link = detail_link.xpath('td[2]/a/@href')[0]
        get_info(link)


def get_info(detail_link):
    res = requests.get(detail_link, headers=headers, cookies=cookie)
    soup = etree.HTML(res.text)
    author = soup.xpath('//a[@class="mr5 cllink preview"]/text()')
    edit_count = soup.xpath('/html/body/div[2]/div[1]/div[2]/div[2]/div[1]/div[2]/p[3]/text()')
    last_update_time = soup.xpath('/html/body/div[2]/div[1]/div[2]/div[2]/div[1]/div[2]/p[4]/text()')
    title = soup.xpath('/html/body/div[2]/div[1]/div[2]/div[1]/div/h3/div[1]/text()')
    try:
        data = {
            'author': author[0],
            'edit_count': edit_count[0].strip().split('：')[1],
            'last_update_time': last_update_time[0].strip().split('：')[1],
            'title': title[0].strip()
        }
        info.append(data)
    except IndexError:
        pass


if __name__ == '__main__':
    urls = [
        'http://3ms.huawei.com/hi/index.php?app=group&mod=Wiki&act=wiki_list&gid=2034789&typeOrder=all&category=all&p={}'.format(
            number) for number in range(1, 14)]
    for single_url in urls:
        get_link(single_url)
    f = open('3ms.csv', 'wt', encoding='utf-8', newline='')
    writer = csv.writer(f)
    writer.writerow(('作者', '标题', '编辑数', '最后编辑时间'))
    for i in info:
        writer.writerow((i['author'], i['title'], i['edit_count'], i['last_update_time']))
    f.close()
