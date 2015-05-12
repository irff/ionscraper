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

class AljazeeraSpider(CrawlSpider):
    name = "aljazeera"

    allowed_domains = [
	    "aljazeera.com",
        ]

    start_urls = ["http://www.aljazeera.com"]

    rules = (
        # Extract links matching 'read' and parse them with the spider's method parse_item
        # Rule(SgmlLinkExtractor(allow=('', )), follow=True),
        Rule(SgmlLinkExtractor(
            allow=('/news/'),
            deny=('facebook.com','twitter.com')),follow=True, callback='parse_item'),
        Rule(SgmlLinkExtractor(
            allow=('/news/','/'),
            deny=('facebook.com','twitter.com')),follow=True),
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
        news['provider'] = "aljazeera.com"

        yield self.parse_item_default(response, news)



    def parse_item_default(self, response, news):
        news['title'] = helper.html_to_string(response.xpath("//body/title").extract()[0])
        news['content'] = helper.item_merge(response.xpath("//div[@id='article-body']").extract())
        news['title'] = helper.clear_item(news['title'])
        news['content'] = helper.clear_item(news['content'])

        news['author'] = " "

        date = response.css("time::attr(datetime)").extract()
        if len(date) > 0:
            news['publish'] = self.ajazeera_date(date[0])
        else:
            news['publish'] = news['timestamp']

        news['location'] = " "

        return news

    def ajazeera_date(self, date_string):
        d = date_string.split(" ")
        year = d[2]
        month = helper.get_month(d[1])
        day = d[0]

        time = d[3].split(":")

        hour =  time[0]
        minute = time[1]
        return helper.formatted_date(year,month,day,hour,minute) + timedelta(hours=-7)
