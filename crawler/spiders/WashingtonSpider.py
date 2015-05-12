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

class WashingtonSpider(CrawlSpider):
    name = "washington"

    allowed_domains = [
	    "www.washingtonpost.com",
        ]

    start_urls = ["http://www.washingtonpost.com"]

    rules = (
        # Extract links matching 'read' and parse them with the spider's method parse_item
        # Rule(SgmlLinkExtractor(allow=('', )), follow=True),
        Rule(SgmlLinkExtractor(
            allow=('\w{1}[a-zA-Z0-9](/)\d[a-zA-Z0-9]{1}'),
            deny=('subscribe.washingtonpost.com')),follow=True, callback='parse_item'),
        Rule(SgmlLinkExtractor(
            allow=('/','\w{1}[a-zA-Z0-9](/)\d[a-zA-Z0-9]{1}',''),
            deny=('subscribe.washingtonpost.com')),follow=True),
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
        news['provider'] = "cnnindonesia.com"

        if "user/login" in response.url or "user/register" in response.url:
            raise DropItem("URL not allowed")

        yield self.parse_item_default(response, news)



    def parse_item_default(self, response, news):
        news['title'] = helper.html_to_string(response.xpath("//h1").extract()[0])
        news['content'] = helper.item_merge(response.xpath("//article").extract())
        news['title'] = helper.clear_item(news['title'])
        news['content'] = helper.clear_item(news['content'])

        author = response.xpath("//span[@class='pb-byline']/text()").extract()
        if len(author) > 0:
            news['author'] = author[0]
        else:
            news['author'] = " "

        date = response.url.split("/")
        if len(date) > 8:
            news['publish'] = self.wp_date(date)
        else:
            news['publish'] = news['timestamp']

        location = news['content'][0:news['content'].find(",")]
        if len(location):
            news['location'] = location
        else:
            news['location'] = " "

        return news

    def wp_date(self, date_string):
        year = date_string[6]
        month = date_string[7]
        day = date_string[8]

        hour =  "00"
        minute = "00"
        return helper.formatted_date(year,month,day,hour,minute) + timedelta(hours=-7)
