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

class CnnIndonsiaSpider(CrawlSpider):
    name = "nationalgeographic"

    allowed_domains = [
	    "news.nationalgeographic.com",
        ]

    start_urls = ["http://news.nationalgeographic.com"]

    rules = (
        # Extract links matching 'read' and parse them with the spider's method parse_item
        # Rule(SgmlLinkExtractor(allow=('', )), follow=True),
        Rule(SgmlLinkExtractor(
            allow=('(/)\d{4}(/)\d{2}(/)'),
            deny=('facebook.com','twitter.com')),follow=True, callback='parse_item'),
        Rule(SgmlLinkExtractor(
            allow=('(/)\d{4}(/)\d{2}(/)','/'),
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
        news['provider'] = "news.nationalgeographic.com"

        if "user/login" in response.url or "user/register" in response.url:
            raise DropItem("URL not allowed")

        yield self.parse_item_default(response, news)



    def parse_item_default(self, response, news):
        news['title'] = helper.html_to_string(response.xpath("//head/title").extract()[0])
        news['content'] = helper.item_merge(response.xpath("//span[@itemprop='body']").extract())
        news['title'] = helper.clear_item(news['title'])
        news['content'] = helper.clear_item(news['content'])

        author = response.xpath("//span[@itemprop='name']/text()").extract()
        if len(author) > 0:
            news['author'] = author[0]
        else:
            news['author'] = " "

        date = response.css("time::attr(datetime)").extract()
        if len(date) > 0:
            news['publish'] = self.natgeo_date(date[0])
        else:
            news['publish'] = news['timestamp']

        news['location'] = " "

        return news

    def natgeo_date(self, plain_string):
        datetime_string = plain_string.split("T")
        
        date_string = datetime_string[0].split("-")
        time_string = datetime_string[1].split(":")

        year = date_string[0]
        month = date_string[1]
        day = date_string[2]

        hour =  time_string[0]
        minute = time_string[1]
        return helper.formatted_date(year,month,day,hour,minute) + timedelta(hours=-7)
