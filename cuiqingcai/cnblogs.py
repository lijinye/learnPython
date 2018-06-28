# -*- coding: utf-8 -*-
import scrapy
from cnblog.items import *
import logging


class CnblogsSpider(scrapy.Spider):
    name = 'cnblogs'
    allowed_domains = ['www.cnblogs.com']
    blogurl = 'https://www.cnblogs.com/sitehome/p/{page}'

    def start_requests(self):
        yield scrapy.Request(url=self.blogurl.format(page=1), callback=self.parse, meta={'page': 1})

    def parse(self, response):
        logging.info('process:' + response.url)
        post_items = response.css('#post_list > .post_item')
        if post_items and len(post_items):
            for post_item in post_items:
                item = CnblogItem()
                item['title'] = post_item.css('div.post_item_body > h3 > a::text').extract_first().strip()
                item['author'] = post_item.css('div.post_item_body > div > a::text').extract_first().strip()
                item['release_time'] = ''.join(post_item.css('div.post_item_body > div::text').extract()).strip()
                item['comments'] = post_item.css(
                    'div.post_item_body > div > span.article_comment > a::text').extract_first().strip()
                item['view'] = post_item.css(
                    'div.post_item_body > div > span.article_view > a::text').extract_first().strip()
                item['summary'] = ''.join(post_item.css('div.post_item_body > p::text').extract()).strip()
                yield item
            if response.css('#paging_block > div > a:last-child::text').extract_first().strip() == 'Next >':
                page = response.meta.get('page') + 1
                yield scrapy.Request(url=self.blogurl.format(page=page), callback=self.parse, meta={'page': page})
