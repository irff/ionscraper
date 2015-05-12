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

class ReutersSpider(CrawlSpider):
    name = "reuters"

    allowed_domains = [
	    "reuters.com",
        ]

    start_urls = ["http://www.reuters.com"]

    rules = (
        # Extract links matching 'read' and parse them with the spider's method parse_item
        # Rule(SgmlLinkExtractor(allow=('', )), follow=True),
        Rule(SgmlLinkExtractor(
            allow=('com/article','(/)\d{4}(/)\d{2}(/)\d{2}'),
            deny=('facebook.com','twitter.com','/login/','/registration/')),follow=True, callback='parse_item'),
        Rule(SgmlLinkExtractor(
            allow=('com/article','(/)\d{4}(/)\d{2}(/)\d{2}','/'),
            deny=('facebook.com','twitter.com','/login/','/registration/')),follow=True),
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
        news['provider'] = "reuters.com"

        if "/login/" in response.url or "/registration/" in response.url:
            raise DropItem("URL not allowed")

        yield self.parse_item_default(response, news)



    def parse_item_default(self, response, news):
        title = response.xpath("//h1").extract()
        if len(title) > 0:
            news['title'] = helper.html_to_string(title[0])
        else:
            news['title'] = response.xpath("//head/title/text()").extract()[0]

        news['content'] = helper.item_merge(response.xpath("//span[@id='articleText']").extract())
        news['title'] = helper.clear_item(news['title'])
        news['content'] = helper.clear_item(news['content'])

        author = response.xpath("//span[@class='byline']/text()").extract()
        if len(author) > 0:
            news['author'] = helper.clear_item(author[0])
        else:
            news['author'] = " "

        date = response.url.split("/")
        if len(date) >= 5:
            news['publish'] = self.reuters_date(date)
        else:
            news['publish'] = news['timestamp']

        location = response.xpath("//span[@class='location']/text()").extract()
        if len(location) > 0:
            news['location'] = helper.clear_item(location[0])
        else:
            news['location'] = " "


        return news

    def reuters_date(self, date_string):

        year = date_string[4]
        month = date_string[5]
        day = date_string[6]

        hour =  "00"
        minute = "00"
        return helper.formatted_date(year,month,day,hour,minute) + timedelta(hours=-7)
