from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from jianshu.items import JianshuItem
from scrapy.http import Request


class jianshu(CrawlSpider):
    name = 'jianshu'
    start_urls = ['https://www.jianshu.com/recommendations/users?page=1']

    def parse(self, response):
        selector = Selector(response)
        base_url = 'https://www.jianshu.com/u/'
        infos = selector.xpath('//div[@class="col-xs-8"]')
        for info in infos:
            author_url = base_url + info.xpath('div/a/@href').extract()[0].split('/')[-1]
            author_name = info.xpath('div/a/h4/text()').extract()[0].strip()
            yield Request(author_url, meta={'author_name': author_name, 'author_url': author_url}, callback=self.parse_item)
        urls = ['https://www.jianshu.com/recommendations/users?page={0}'.format(i) for i in range(2, 10)]
        for url in urls:
            yield Request(url, callback=self.parse)

    def parse_item(self, response):
        item = JianshuItem()
        item['author_url'] = response.meta['author_url']
        item['author_name'] = response.meta['author_name']
        try:
            selector = Selector(response)
            fans = selector.xpath('//div[@class="info"]/ul/li[2]/div/a/p/text()').extract()[0]
            articles = selector.xpath('//div[@class="info"]/ul/li[3]/div/a/p/text()').extract()[0]
            word_count = selector.xpath('//div[@class="info"]/ul/li[4]/div/p/text()').extract()[0]
            item['fans'] = fans
            item['articles'] = articles
            item['word_count'] = word_count
            yield item
        except:
            pass
