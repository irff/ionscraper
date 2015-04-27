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

class PikiranRakyatSpider(CrawlSpider):
    name = "pikiranrakyat"

    allowed_domains = [
	    "www.pikiran-rakyat.com",
        ]

    start_urls = ["http://www.pikiran-rakyat.com"]

    rules = (
        # Extract links matching 'read' and parse them with the spider's method parse_item
        # Rule(SgmlLinkExtractor(allow=('', )), follow=True),
        Rule(SgmlLinkExtractor(
            allow=('\d{4}(/)\d{2}(/)\d{2}(/)\w'),
            deny=('facebook.com','twitter.com','/rss','/contact','www/delivery')),follow=True, callback='parse_item'),
        Rule(SgmlLinkExtractor(
            allow=('/tag','/','\d{4}(/)\d{2}(/)\d{2}(/)\w'),
            deny=('facebook.com','twitter.com','/rss','/contact','www/delivery')),follow=True),
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
        news['provider'] = "pikiran-rakyat.com"

        yield self.parse_item_default(response, news)


    def parse_item_default(self, response, news):
        news['title'] = helper.html_to_string(response.xpath("//h1").extract()[0])
        news['content'] = helper.item_merge(response.xpath("//div[@class='node node-article node-promoted clearfix']/div[3]/div[@class='items-body']").extract())
        news['title'] = helper.clear_item(news['title'])
        news['content'] = helper.clear_item(news['content'])

        news['author'] = " "

        date = response.css(".submitted span::attr(content)").extract()
        if len(date) > 0:
            news['publish'] = self.pikiranrakyat_date(date[0])
        else:
            news['publish'] = news['timestamp']

        if "(PRLM)" in news['content']:
            news['location'] = news['content'][0:news['content'].find(',')]
        else:
            news['location'] = " "


        return news

    def pikiranrakyat_date(self, plain_string):
        datetime_string = plain_string.split("T")

        date_string = datetime_string[0].split("-")
        time_string = datetime_string[1].split(":")

        year = date_string[0]
        month = date_string[1]
        day = date_string[2]

        hour =  time_string[0]
        minute = time_string[1]
        return helper.formatted_date(year,month,day,hour,minute) + timedelta(hours=-7)
