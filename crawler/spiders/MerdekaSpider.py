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

class MerdekaSpider(CrawlSpider):
    name = "merdeka"

    allowed_domains = [
	    "merdeka.com",
        ]

    start_urls = ["http://www.merdeka.com"]

    rules = (
        # Extract links matching 'read' and parse them with the spider's method parse_item
        # Rule(SgmlLinkExtractor(allow=('', )), follow=True),
        Rule(SgmlLinkExtractor(
            allow=('(merdeka.com/)\w{3}[A-Za-z0-1]'),
            deny=('facebook.com','twitter.com','/foto/','profile.merdeka')),follow=True, callback='parse_item'),
        Rule(SgmlLinkExtractor(
            allow=('(merdeka.com/)\w{3}[A-Za-z0-1]','/tag','/index'),
            deny=('facebook.com','twitter.com','/foto/','profile.merdeka')),follow=True),
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
        news['provider'] = "merdeka.com"

        if "/foto/" in response.url or "profile.merdeka.com" in response.url:
            raise DropItem("URL not allowed")

        yield self.parse_item_default(response, news)



    def parse_item_default(self, response, news):
        news['title'] = helper.html_to_string(response.xpath("//h1").extract()[0])
        news['content'] = helper.item_merge(response.xpath("//div[@id='mdk-body-newsarea']").extract())
        news['title'] = helper.clear_item(news['title'])
        news['content'] = helper.clear_item(news['content'])

        author_date = response.xpath("//div[@id='mdk-body-news-reporter']/text()").extract()
        if len(author_date) > 1:
            author = author_date[0]
            if len(author) > 0:
                news['author'] = author
            else:
                news['author'] = " "

            date = author_date[1]
            if len(date) > 0:
                news['publish'] = self.merdeka_date(date)
            else:
                news['publish'] = news['timestamp']

        news['location'] = " "

        return news

    def merdeka_date(self, plain_string):
        datetime_string = plain_string.split(" ")
        year = datetime_string[5]
        ms = datetime_string[4]
        month = helper.get_month(ms)
        day = datetime_string[3]

        time = datetime_string[6].split(":")
        hour =  time[0]
        minute = time[1]
        return helper.formatted_date(year,month,day,hour,minute) + timedelta(hours=-7)
