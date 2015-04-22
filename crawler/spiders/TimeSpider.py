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

class TimeSpider(CrawlSpider):
    name = "time"

    allowed_domains = [
	    "time.com",
        ]

    start_urls = ["http://time.com"]

    rules = (
        # Extract links matching 'read' and parse them with the spider's method parse_item
        # Rule(SgmlLinkExtractor(allow=('', )), follow=True),
        Rule(SgmlLinkExtractor(
            allow=('\w{2}[a-zA-Z0-9](/)\d[0-9]{5}'),
            deny=('facebook.com','twitter.com','subscription.time.com')),follow=True, callback='parse_item'),
        Rule(SgmlLinkExtractor(
            allow=('/tag/','/topic/','/'),
            deny=('facebook.com','twitter.com','subscription.time.com')),follow=True),
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
        news['provider'] = "time.com"

        if "subscription.time.com" in response.url:
            raise DropItem("URL not allowed")

        yield self.parse_item_default(response, news)



    def parse_item_default(self, response, news):
        news['title'] = helper.html_to_string(response.xpath("//h2[@itemprop='headline']").extract()[0])
        news['content'] = helper.item_merge(response.xpath("//section[@itemprop='articleBody']").extract())
        news['title'] = helper.clear_item(news['title'])
        news['content'] = helper.clear_item(news['content'])

        author = response.xpath("//a[@itemprop='author']/text()").extract()
        if len(author) > 0:
            news['author'] = author[0]
        else:
            news['author'] = " "

        date = response.css("time::attr(datetime)").extract()
        if len(date) > 0:
            news['publish'] = self.time_date(date[0])
        else:
            news['publish'] = news['timestamp']

        news['location'] = " "

        return news


    def time_date(self, date_string):
        a = re.compile("\d{4}(-)\d{2}(-)\d{2}( )\d{2}(:)\d{2}(:)\d{2}")

        if a.match(date_string):
            year = date_string[0:4]
            month = date_string[5:7]
            day = date_string[8:10]
            hour =  date_string[11:13]
            minute = date_string[14:16]
            second = date_string[17:19]
        else:
            date = date_string.split(" ")
            year = date[2]
            month = helper.get_month(date[0])
            day = date[1]
            day = day[0:len(day) - 1]
            hour = "00"
            minute = "00"
            second = "00"

        return helper.formatted_date_with_second(year,month,day,hour,minute,second) + timedelta(hours=-7)