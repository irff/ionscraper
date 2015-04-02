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

class OkezoneSpider(CrawlSpider):
    name = "okezone"

    allowed_domains = [
	    "okezone.com",
        "news.okezone.com",
        "economy.okezone.com",
        "lifestyle.okezone.com",
        "celebrity.okezone.com",
        "bole.okezone.com",
        "sports.okezone.com",
        "techno.okezone.com",
        "foto.okezone.com"
        ]

    start_urls = ["http://okezone.com"]

    rules = (
        # Extract links matching 'read' and parse them with the spider's method parse_item
        # Rule(SgmlLinkExtractor(allow=('', )), follow=True),
        Rule(SgmlLinkExtractor(
            allow=('/read','/view'),
            deny=('/login','/SignUp')),follow=True, callback='parse_item'),
        Rule(SgmlLinkExtractor(
            allow=('/'),
            deny=('/login','/SignUp')),follow=True),
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
        news['provider'] = "okezone.com"

        if "/register" in response.url or "warungkopi.okezone" in response.url:
            raise DropItem("URL not allowed")

        yield self.parse_item_default(response, news)



    def parse_item_default(self, response, news):
        news['title'] = helper.html_to_string(response.xpath("//h1").extract()[0])
        news['content'] = helper.item_merge(response.xpath("//div[@id='contentx']").extract())
        news['title'] = helper.clear_item(news['title'])
        news['content'] = helper.clear_item(news['content'])

        author = response.xpath("//div[@class='nmreporter']/div/text()").extract()
        if len(author) > 0:
            news['author'] = author[0]
        else:
            news['author'] = " "

        date = response.xpath("//time/text()").extract()
        if len(date) > 0:
            news['publish'] = self.okezone_date(date[0])
        else:
            news['publish'] = news['timestamp']

        news['location'] = " "

        return news

    def okezone_date(self, plain_string):
        date_string = plain_string.split(" ")

        year = date_string[3]
        month = helper.get_month(date_string[2])
        day = date_string[1]

        time_string = date_string[5].split(":")
        hour =  time_string[0]
        minute = time_string[1]
        return helper.formatted_date(year,month,day,hour,minute) + timedelta(hours=-7)
