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

class WashingtonSpider(Spider):
    name = "washington"

    allowed_domains = [
	    "www.washingtonpost.com",
        ]

    start_urls = ["http://www.washingtonpost.com/world/asia_pacific/envoy-says-indonesia-leader-too-busy-to-take-australia-call/2015/03/26/87d55c2a-d385-11e4-8b1e-274d670aa9c9_story.html"]

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
    def parse(self, response):
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

        date = response.xpath("//span[@class='pb-timestamp']/text()").extract()
        if len(date) > 0:
            news['publish'] = self.wp_date(date[0])
        else:
            news['publish'] = news['timestamp']

        location = news['content'][0:news['content'].find(",")]
        if len(location):
            news['location'] = location
        else:
            news['location'] = " "

        return news

    def wp_date(self, plain_string):
        log.msg(plain_string, log.CRITICAL)
        datetime_string = plain_string.split(" ")

        date_string = datetime_string[1].split("/")
        time_string = datetime_string[2].split(":")

        year = date_string[2]
        month = date_string[1]
        day = date_string[0]

        hour =  time_string[0]
        minute = time_string[1]
        return helper.formatted_date(year,month,day,hour,minute) + timedelta(hours=-7)
