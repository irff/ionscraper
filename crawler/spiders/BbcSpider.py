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
import re

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

class NytimesSpider(CrawlSpider):
    name = "bbc"

    allowed_domains = [
	    "bbc.com",
        ]

    start_urls = ["http://www.bbc.com"]

    rules = (
        # Extract links matching 'read' and parse them with the spider's method parse_item
        # Rule(SgmlLinkExtractor(allow=('', )), follow=True),
        Rule(SgmlLinkExtractor(
            allow=('/news/','(bbc.com/)\w'),
            deny=('facebook.com','twitter.com','/signin?','ssl.bbc.com','/comments?')),follow=True, callback='parse_item'),
        Rule(SgmlLinkExtractor(
            allow=('/pages/','/news/','(bbc.com/)\w','/'),
            deny=('facebook.com','twitter.com','/signin?','ssl.bbc.com','/comments?')),follow=True),
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
        news['provider'] = "bbc.com"

        if "/signin?" in response.url or "ssl.bbc.com" in response.url or "/comments?" in response.url:
            raise DropItem("URL not allowed")

        yield self.parse_item_default(response, news)



    def parse_item_default(self, response, news):
        news['title'] = helper.html_to_string(response.xpath("//h1").extract()[0])
        news['content'] = helper.item_merge(response.xpath("//div[@property='articleBody']").extract())
        news['title'] = helper.clear_item(news['title'])
        news['content'] = helper.clear_item(news['content'])

        news['author'] = " "

        date = response.css(".date::attr(data-datetime)").extract()
        if len(date) > 0:
            news['publish'] = self.bbc_date(date[0])
        else:
            news['publish'] = news['timestamp']

        news['location'] = " "

        return news


    def bbc_date(self, date_string):
        date = date_string.split(" ")
        year = date[2]
        month = helper.get_month(date[1])
        day = date[0]
        hour = "00"
        minute = "00"
        second = "00"
        return helper.formatted_date_with_second(year,month,day,hour,minute,second) + timedelta(hours=-7)

