__author__ = 'Kandito Agung'

import scrapy
from scrapy import log
from crawler.NewsItem import NewsItem
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.spider import Spider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.exceptions import DropItem
from datetime import datetime, timedelta
import helper

"""
If you want to debug for a page,
    Change KompasSpider Class extends 'Spider' class
    Change start_urls with a url that you want to debug
    Change 'parse_item' method to 'parse'
If you want crawling and follow link , Change Kompas
    Change KompasSpider Class extends 'CrawlSpider' class
    Change start_urls with 'http://kompas.com'
    Change 'parse' method to 'parse_item'
"""

class BijakSpider(CrawlSpider):
    name = "bijaks"
    allowed_domains = [
	    "bijaks.net",
        ]

    start_urls = ["http://www.bijaks.net"]

    rules = (
        # Extract links matching 'read' and parse them with the spider's method parse_item
        # Rule(SgmlLinkExtractor(allow=('', )), follow=True),
        Rule(SgmlLinkExtractor(
            allow=('news/','/scandal/'),
            deny=('home/login','news/index','/aktor/','/profile/')),follow=True, callback='parse_item'),
        Rule(SgmlLinkExtractor(
            allow=('home/','news/','news/index',''),
            deny=('home/login','/aktor/','/profile/')),follow=True),
    )

    """
    if use Spider, change function to 'parse'
    if use CrawlSpider, change function to 'parse_item'
    """
    def parse_item(self, response):
        log.msg("Get: %s" % response.url, level=log.INFO)

        news = NewsItem()
        news['url'] = response.url
        """Getting Timestamp and Provider"""
        news['timestamp']= datetime.utcnow()
        news['provider'] = "bijaks.net"

        if "/login" in response.url:
            raise DropItem("URL not allowed")

        if "/scandal/" in response.url:
            yield self.parse_item_scandal(response, news)
        else:
            yield self.parse_item_default(response, news)



    def parse_item_default(self, response, news):
        news['title'] = helper.html_to_string(response.xpath("//h2").extract()[0])
        news['content'] = helper.item_merge(response.xpath("//div[@class='news-detail']/p").extract())
        news['title'] = helper.clear_item(news['title'])
        news['content'] = helper.clear_item(news['content'])

        # Bijaks no author
        news['author'] = " "

        date = response.xpath("//h4/text()").extract()
        if len(date) > 0:
            news['publish'] = self.bijaks_date(date[0])
        else:
            logging.log(logging.WARNING, helper.DATE_WARN)
            news['publish'] = news['timestamp']

        if "BIJAKS" in news['content']:
            news['location'] = news['content'][0:news['content'].find(',')]
        else:
            news['location'] = " "
        return news

    def parse_item_scandal(self, response, news):
        news['title'] = helper.html_to_string(response.xpath("//h2").extract()[0])
        news['content'] = helper.item_merge(response.xpath("//div[@class='tab-content']").extract())
        news['title'] = helper.clear_item(news['title'])
        news['content'] = helper.clear_item(news['content'])

        # Bijaks no author
        news['author'] = " "

        date = response.xpath("//*[@id='myCarousel']/div[4]/div[3]/div[2]/span/text()").extract()
        if len(date) > 0:
            news['publish'] = self.bijaks_scandal_date(date[0])
        else:
            news['publish'] = news['timestamp']

        if "BIJAKS" in news['content']:
            news['location'] = news['content'][0:news['content'].find(',')]
        else:
            news['location'] = " "
        return news


    def bijaks_date(self, plain_string):
        if plain_string == None:
            return None

        plain_string = helper.html_to_string(plain_string)
        date = plain_string.split(" ")

        day = date[0]
        month = helper.get_month(date[1])
        year = date[2]

        time = date[3].split(":")
        hour = time[0]
        minute = time[1]

        return helper.formatted_date(year,month,day,hour,minute) + timedelta(hours=-7)


    def bijaks_scandal_date(self, plain_string):
        if plain_string == None:
            return None

        plain_string = helper.html_to_string(plain_string)
        date = plain_string.split(" ")

        day = date[0]
        month = helper.get_month(date[1])
        year = date[2]

        hour = "00"
        minute = "00"

        return helper.formatted_date(year,month,day,hour,minute) + timedelta(hours=-7)
