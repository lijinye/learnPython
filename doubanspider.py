# -*- coding:utf-8 -*-
import time
import pymongo
from bs4 import BeautifulSoup
import aiohttp
import asyncio
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.1 Safari/605.1.15',
    'Host': 'book.douban.com',
    'Referer': 'https://book.douban.com/',
    'Cookie': 'bid=oYgs_fojlz8; gr_user_id=89172f5c-85a0-4b05-891e-92d835d5952e; _vwo_uuid_v2=D5CC65AC439489575BF9ACA044ABB99E3|1ca16f3dc8929a67945bb2ad48bf962a; __yadk_uid=C74zVyclu1xJQi831giZ4qwvLO5Wrv8m; Hm_lvt_16a14f3002af32bf3a75dfe352478639=1530349543; push_noty_num=0; push_doumail_num=0; ap=1; ct=y; __utmz=30149280.1530408847.3.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmv=30149280.17491; __utmc=30149280; __utmc=81379588; __utmz=81379588.1530530216.9.4.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/misc/sorry; ps=y; dbcl2="174918513:VzFodo9SX6w"; ck=wrzS; _pk_ref.100001.3ac3=%5B%22%22%2C%22%22%2C1530538060%2C%22https%3A%2F%2Fwww.douban.com%2Fmisc%2Fsorry%3Foriginal-url%3Dhttps%253A%252F%252Fbook.douban.com%252Ftag%252F%2525E6%252597%2525A5%2525E6%25259C%2525AC%22%5D; _pk_ses.100001.3ac3=*; __utma=30149280.913797728.1530349451.1530535518.1530538060.11; __utma=81379588.987976908.1530349451.1530535518.1530538060.11; __utmt_douban=1; __utmt=1; __utmb=30149280.12.10.1530538060; __utmb=81379588.12.10.1530538060; _pk_id.100001.3ac3=77c1124b488ba1c8.1530349451.11.1530538990.1530535518.'
}
typeurl = 'https://book.douban.com/tag/?view=cloud'
host = 'https://book.douban.com'
client = pymongo.MongoClient()
db = client['douban']
collection = db['doubanbooks']


def get_booktype():
    session = requests.session()
    res = session.get(url=typeurl, headers=headers)
    # print(res.text)
    if res.status_code == 200:
        soup = BeautifulSoup(res.text, 'lxml')
        types = soup.select('table.tagCol > tbody > tr a')
        booktype = []
        for type in types:
            booktype.append({
                'url': type['href'],
                'type': type.string
            })
        return booktype


async def get_book_detail(session, type, detail_url):
    print('url=', host + detail_url)
    try:
        async with session.get(url=host + detail_url) as response:
            if response.status == 200:
                soup = BeautifulSoup(await response.text(), 'lxml')
                items = soup.select('#subject_list > ul > li')
                if items:
                    for item in items:
                        bookdetail = {
                            'type': type,
                            'name': item.select('div.info > h2 > a')[0]['title'],
                            'author': item.select('div.info > div.pub')[0].string.strip().split('/')[0],
                            'time': item.select('div.info > div.pub')[0].string.strip().split('/')[-2],
                            'price': item.select('div.info > div.pub')[0].string.strip().split('/')[-1],
                            'score': item.select('div.info > div.star.clearfix > span.rating_nums')[
                                0].string if item.select(
                                'div.info > div.star.clearfix > span.rating_nums') else '0',
                            'numbers': item.select('div.info > div.star.clearfix > span.pl')[0].string.strip()
                        }
                        collection.insert_one(bookdetail)
                asyncio.sleep(5)
                if soup.select('#subject_list > div.paginator > span.next > a'):
                    next_url = soup.select('#subject_list > div.paginator > span.next > a')[0]['href']
                    await get_book_detail(session, type, next_url)
    except Exception:
        pass


async def main(type, detail_url):
    async with aiohttp.ClientSession(headers=headers) as session:
        await get_book_detail(session, type, detail_url)


if __name__ == '__main__':
    booktypes = get_booktype()
    print('booktypes==', booktypes)
    loop = asyncio.get_event_loop()
    size = 10
    for i in range(0, len(booktypes), size):
        if i + size > len(booktypes):
            types = booktypes[i:len(booktypes)]
        else:
            types = booktypes[i:i + size]
        tasks = [main(type['type'], type['url']) for type in types]
        loop.run_until_complete(asyncio.wait(tasks))
        time.sleep(5)
    client.close()
