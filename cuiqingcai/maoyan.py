# -*- coding:utf-8 -*-
#Requests与正则表达式抓取猫眼电影排行
import requests
import re
import json
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'
}


def get_one_page(url):
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        return res.text
    return None


def parse_one_page(html):
    pattern = re.compile(
        '<dd>.*?<i class="board-index board-index-\d+">(.*?)</i>.*?<img data-src="(.*?)" alt.*?<p'
        ' class="name">.*?">(.*?)</a>.*?<p class="star">(.*?)</p>.*?<p class="releasetime">'
        '(.*?)</p>.*?<i class="integer">(.*?)</i><i class="fraction">(.*?)</i>.*?</dd>', re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield {
            'level': item[0],
            'picurl': item[1],
            'name': item[2],
            'actor': item[3].strip(),
            'releasetime': item[4],
            'score': item[5] + item[6]
        }


def write_to_file(content):
    with open('maoyan.txt', 'a', encoding='utf-8')  as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')


def main(offset):
    url = 'http://maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)


if __name__ == '__main__':
    for i in range(10):
        main(offset=i * 10)
        time.sleep(1)
