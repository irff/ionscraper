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

"""
    BELOM SELESAI BRO, RULE LINK BELUM, PARSER BELUM, BARU NYIAPIN FILE
    NANTI DILANJUTIN
"""
class SwaSpider(CrawlSpider):
    name = "swa"

    allowed_domains = [
	    "swa.com",
        ]

    start_urls = ["http://www.swa.com"]

    rules = (
        # Extract links matching 'read' and parse them with the spider's method parse_item
        # Rule(SgmlLinkExtractor(allow=('', )), follow=True),
        Rule(SgmlLinkExtractor(
            allow=('/read'),
            deny=('facebook.com','twitter.com','/newsletter','/rss')),follow=True, callback='parse_item'),
        Rule(SgmlLinkExtractor(
            allow=('indeks','/','read'),
            deny=('facebook.com','twitter.com','/newsletter','/rss')),follow=True),
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
        news['provider'] = "inilah.com"

        if "/newsletter" in response.url or "/rss" in response.url:
            raise DropItem("URL not allowed")

        yield self.parse_item_default(response, news)



    def parse_item_default(self, response, news):
        news['title'] = helper.html_to_string(response.xpath("//h2").extract()[0])
        news['content'] = helper.item_merge(response.xpath("//div[@class='txt-detail']").extract())
        news['title'] = helper.clear_item(news['title'])
        news['content'] = helper.clear_item(news['content'])

        author = response.xpath("//div[@class='w-cd']/h6/span/text()").extract()
        if len(author) > 0:
            news['author'] = author[0]
        else:
            news['author'] = " "

        date = response.xpath("//div[@class='w-cd']/h6/text()").extract()
        if len(date) > 1:
            news['publish'] = self.inilah_date(helper.clear_item(date[1]))
        else:
            news['publish'] = news['timestamp']

        if "INILAHCOM" in news['content']:
            news['location'] = news['content'][12:news['content'].find('-')]
        else:
            news['location'] = " "

        return news

    def inilah_date(self, plain_string):
        datetime_string = plain_string.split("|")
        date_string = datetime_string[1].split(" ")
        time_string = datetime_string[2].split(" ")
        time_string = time_string[1].split(":")

        year = date_string[4]
        ms = date_string[3]
        month = helper.get_month(ms)
        day = date_string[2]

        hour =  time_string[0]
        minute = time_string[1]
        return helper.formatted_date(year,month,day,hour,minute) + timedelta(hours=-7)
