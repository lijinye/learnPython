# -*- coding:utf-8 -*-
# 获取拉勾网招聘信息存入mongoDB

import requests
import json
import pymongo
import time

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36'
                         ' (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
           'Cookie': 'user_trace_token=20180304180217-1ebaf2bb-1f93-11e8-9bde-525400f775ce; LGUID=20180304180217-1ebaf7a9-1f93-11e8-9bde-525400f775ce; JSESSIONID=ABAAABAAADEAAFI91F98B89A20D07F7F7E3867CE7D30D37; index_location_city=%E5%85%A8%E5%9B%BD; TG-TRACK-CODE=search_code; _gid=GA1.2.53432555.1520157737; _gat=1; _ga=GA1.2.191506701.1520157737; LGSID=20180304180217-1ebaf472-1f93-11e8-9bde-525400f775ce; LGRID=20180304183853-3bfcbe07-1f98-11e8-b124-5254005c3644; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1520157737; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1520159934; SEARCH_ID=c3bca63a55b54e41a57056e48c2e08b5',
           'Connection': 'keep-alive',
           'X-Requested-With': 'XMLHttpRequest',
           'Referer': 'https://www.lagou.com/jobs/list_python?city=%E5%85%A8%E5%9B%BD&cl=false&fromSearch=true&labelWords=&suginput='
           }

client = pymongo.MongoClient('localhost', 27017)
mydb = client['mydb']
lagou = mydb['lagou']


def get_info(url, param):
    res = requests.post(url, data=param, headers=headers)
    res_json = json.loads(res.text)
    # print(res_json)
    results = res_json['content']['positionResult']['result']
    for result in results:
        infos = {
            'positionName': result['positionName'],
            'salary': result['salary'],
            'companyFullName': result['companyFullName'],
            'city': result['city'],
            'companyLabelList': result['companyLabelList'],
            'formatCreateTime': result['formatCreateTime'],
            'workYear': result['workYear'],
            'education': result['education']
        }
        lagou.insert_one(infos)
        time.sleep(2)
    print('page {0} success'.format(param['pn']))


if __name__ == '__main__':
    url = 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false&isSchoolJob=0'
    for i in range(1, 31):
        param = {
            'first': 'false',
            'pn': str(i),
            'kd': 'python'
        }
        get_info(url, param)
        print('Done')
