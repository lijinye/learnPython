# -*- coding:utf-8 -*-
# 爬取论坛标题，存储到本地文件

import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'}
cookie_str = '_ha_ref.3ms-hi.f914=%5B%22%22%2C%22%22%2C1519699249%2C%22http%3A%2F%2Fw3.huawei.com%2Fnext%2Findexa.html%3Flocale%3Dzh%22%5D; _ha_id.3ms-hi.f914=67-1C-5E-6E-22-C0-10-CE-DD-80-3A-2E-CE-AA-89-6B; _ha_ses.3ms-hi.f914=37b7a4ac0f0cc139945acb4c6dbca5e926cc29c3; v1st=15E137F9D8C15AD7; platuserID=lwx309353; isShowTips=yes; visitorId=DC2B41B3AA524FC09DE0AC91F7CD5F56; per_last=1507529718819; AMCV_7DA25C0158C1322D0A495DB1%40AdobeOrg=1099438348%7CMCIDTS%7C17471%7CMCMID%7C29464754826455535403117560118781890482%7CMCAID%7CNONE%7CMCOPTOUT-1509445333s%7CNONE%7CvVersion%7C2.1.0; _dmpa_id=51859a36d9ed0952c4043288138121509438133449.1509438080.1.1509438080.1509438080; _ga=GA1.2.227787174.1509438133; FORUM_LOGIN_AUTH_SECURE_CODE=67-1C-5E-6E-22-C0-10-CE-0F-DF-0F-A1-97-91-C8-AD-93-43-16-F3-24-F9-68-1A-88-90-F9-38-37-CE-BC-9A-96-58-D5-A6-90-C8-20-E6-A6-D2-C5-B5-BE-9E-4A-7D-0F-C6-70-02-04-B3-7E-48; selnode=""; 2D-4A-29-3E-6C-E6-DF-76-1D-A3-0E-21-2C-88-0E-05=67-1C-5E-6E-22-C0-10-CE-0F-DF-0F-A1-97-91-C8-AD-E6-6A-0D-98-A9-19-20-C2-9E-35-CA-98-B3-6B-50-30-96-58-D5-A6-90-C8-20-E6-8D-28-4E-FF-93-5C-AC-2E; worldwide_tag=%2Fcn; hwsso_uniportal=""; hwssot=0C-65-1F-B0-3E-47-4D-D0-8C-08-17-E4-B2-48-1A-20; hwssot3=26071752215156; suid=67-1C-5E-6E-22-C0-10-CE-DD-80-3A-2E-CE-AA-89-6B; w3Token=67-1C-5E-6E-22-C0-10-CE-E2-AC-DE-37-1C-49-C3-1F-B5-F2-02-59-1B-B3-56-5D-84-B5-D2-DD-B5-6B-2B-8C; login_uid=67-1C-5E-6E-22-C0-10-CE-DD-80-3A-2E-CE-AA-89-6B; _sid_=EA-85-D7-0C-1E-49-1D-7C-90-6B-D0-16-8B-57-E0-AE-DA-BB-BD-63-00-84-6F-33-3C-73-18-F1-BF-9F-FC-E6-78-05-D2-B5-70-DE-6A-D7; hwsso_am=77-22-F7-0E-84-9F-31-CD; login_sip=DC-25-A4-A9-2B-6A-1A-06-3F-F3-7B-E6-06-C3-08-BE-F8-2E-80-0E-92-58-96-48; login_sid=EA-85-D7-0C-1E-49-1D-7C-90-6B-D0-16-8B-57-E0-AE-DA-BB-BD-63-00-84-6F-33-3C-73-18-F1-BF-9F-FC-E6-78-05-D2-B5-70-DE-6A-D7; LtpaToken=xsOHrCTLIAlUVP2XBzryGj7RmkqVXxsnzNMFLll+GTjD+xwvtyPv5qHDCHX01HC1r9xCLoL4Xdkr9tWP7I9SwuQdY3XpWxSwvlu4b3hdgN44bripPctg/AYPig7mnCAJHHiLaiqggi7j2oDcBSuSFF3h3Ery5pEQ9KMPh3gxDV899Ae25Kq1Dh7lVtrkwoGnlitnw7XxRnR56GFusglEjqC5aXulw1BjOlEiMpi24ohDbaYc5osR/RIwIrXc4eIpN9heSdd3WwiaMgwoJVjyMVjpZEefhqxxkS2hbxqMxJu1eo2nX0kLe9GNF5o48d5WY2PUNQF+FhHAHlvJeh732omGGBU0u0lyfqHgcZ/nnUPojQ2F3SpmOw==; DGGPRO3MSMMSERVICE=0000mmebUQ2KJsjLTLIh_54E5E-:dggmwc2app992_CloneID; SZXPRO3MSDOC3MS=0000omepPTbxnvTmtpqYdjbbNVG:szxgvap1538-mwc_CloneID; hwkm_sid=2i6C-QGSSXdLzfPjJRE4KlO65Jfs77cT; hwkm_sid.sig=e-bw1prGc_yd8ypGK0RlLp6r75w; HW3MS_think_language=zh-cn; hwsso_login=""; login_logFlag=out; HW3MS_CONNECT_SESSION=au9i1k74c1429bsuirrfl7a740; HW3MS_ResourceLanguage=czowOiIiOw%3D%3D; bishengSID=000059gdql5DaQP1hYruKGfaS0U:19grdfk5i; HW3MS_resourceReadedKey=Portal-'
cookie = {}
for i in cookie_str.split(';'):
    cookie[i.split('=')[0]] = i.split('=')[1]

f = open('title.txt', 'a+', encoding="utf-8")


def get_info(url):
    req = requests.get(url, cookies=cookie, headers=headers)
    if req.status_code == 200:
        soup = BeautifulSoup(req.text, 'html.parser')
        titles = soup.select('.cl.f14 > a')
        for title in titles:
            f.write(title.get('title').strip() + '\n')
    else:
        pass


if __name__ == '__main__':
    urls = ['http://3ms.huawei.com/hi/index.php?app=bbs&mod=Index&act=all&3ms_type=menu&p={0}'.format(i) for i in
            range(1, 20)]
    for url in urls:
        get_info(url)
    f.close()
