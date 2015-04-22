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
    name = "nytimes"

    allowed_domains = [
	    "nytimes.com",
        ]

    start_urls = ["http://www.nytimes.com"]

    rules = (
        # Extract links matching 'read' and parse them with the spider's method parse_item
        # Rule(SgmlLinkExtractor(allow=('', )), follow=True),
        Rule(SgmlLinkExtractor(
            allow=('\d{4}(/)\d{2}(/)\d{2}(/)\w'),
            deny=('facebook.com','twitter.com','/subscriptions/','mobile.nytimes.com')),follow=True, callback='parse_item'),
        Rule(SgmlLinkExtractor(
            allow=('/pages/','/'),
            deny=('facebook.com','twitter.com','/subscriptions/','mobile.nytimes.com')),follow=True),
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
        news['provider'] = "nytimes.com"

        if "/subscriptions/" in response.url:
            raise DropItem("URL not allowed")

        yield self.parse_item_default(response, news)



    def parse_item_default(self, response, news):
        news['title'] = helper.html_to_string(response.xpath("//h1[@itemprop='headline']").extract()[0])
        news['content'] = helper.item_merge(response.xpath("//p[@itemprop='articleBody']").extract())
        news['title'] = helper.clear_item(news['title'])
        news['content'] = helper.clear_item(news['content'])

        author = response.xpath("//span[@itemprop='name']/text()").extract()
        if len(author) > 0:
            news['author'] = author[0]
        else:
            news['author'] = " "

        date = response.css("time::attr(datetime)").extract()
        if len(date) > 0:
            news['publish'] = self.nytimes_date(date[0])
        else:
            news['publish'] = news['timestamp']

        news['location'] = " "

        return news


    def nytimes_date(self, date_string):
        year = date_string[0:4]
        month = date_string[5:7]
        day = date_string[8:10]
        hour = "00"
        minute = "00"
        second = "00"
        return helper.formatted_date_with_second(year,month,day,hour,minute,second) + timedelta(hours=-7)

