# -*- coding:utf-8 -*-
import time
import pymongo
from bs4 import BeautifulSoup
import aiohttp
import asyncio

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    'Host': 'book.douban.com',
    'Referer': 'https://book.douban.com/',
    'Cookie': 'bid=oYgs_fojlz8; gr_user_id=89172f5c-85a0-4b05-891e-92d835d5952e; _vwo_uuid_v2=D5CC65AC439489575BF9ACA044ABB99E3|1ca16f3dc8929a67945bb2ad48bf962a; __yadk_uid=C74zVyclu1xJQi831giZ4qwvLO5Wrv8m; Hm_lvt_16a14f3002af32bf3a75dfe352478639=1530349543; dbcl2="174918513:BxqD0znrfm8"; push_noty_num=0; push_doumail_num=0; ap=1; ct=y; ck=KVwc; _pk_ref.100001.3ac3=%5B%22%22%2C%22%22%2C1530408847%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DlkOSpBdRVz6Bsf82cHruIUtQDW4CG7ZYQMIFXk0jAIlSnMeOkzaGo3usGDJhULgG%26wd%3D%26eqid%3Dab4457f5000414fd000000055b382edf%22%5D; __utma=30149280.913797728.1530349451.1530364419.1530408847.3; __utmc=30149280; __utmz=30149280.1530408847.3.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utma=81379588.987976908.1530349451.1530364419.1530408847.3; __utmc=81379588; __utmz=81379588.1530408847.3.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; _pk_id.100001.3ac3=77c1124b488ba1c8.1530349451.3.1530408979.1530364652.'
}
typeurl = 'https://book.douban.com/tag/?view=cloud'
host = 'https://book.douban.com'
client = pymongo.MongoClient()
db = client['douban']
collection = db['doubanbooks']


async def main():
    async with aiohttp.ClientSession() as session:
        async with session.get(url=typeurl, headers=headers) as res:
            if res.status == 200:
                soup = BeautifulSoup(await res.text(), 'lxml')
                types = soup.select('table.tagCol > tbody > tr a')
                for type in types:
                    await get_book_detail(session, type.string, type['href'])
                    asyncio.sleep(1)


async def get_book_detail(session, type, detail_url):
    print('url=', host + detail_url)
    try:
        async with session.get(url=host + detail_url, headers=headers) as response:
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
                asyncio.sleep(1)
                if soup.select('#subject_list > div.paginator > span.next > a'):
                    next_url = soup.select('#subject_list > div.paginator > span.next > a')[0]['href']
                    await get_book_detail(session, type, next_url)
    except Exception:
        pass


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    client.close()
