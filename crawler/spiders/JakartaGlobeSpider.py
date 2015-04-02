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

class JakartaGlobeSpider(CrawlSpider):
    name = "jakartaglobe"

    allowed_domains = [
	    "thejakartaglobe.beritasatu.com",
        ]

    start_urls = ["http://thejakartaglobe.beritasatu.com"]

    rules = (
        # Extract links matching 'read' and parse them with the spider's method parse_item
        # Rule(SgmlLinkExtractor(allow=('', )), follow=True),
        Rule(SgmlLinkExtractor(
            allow=('/news'),
            deny=('facebook.com','twitter.com','multimedia')),follow=True, callback='parse_item'),
        Rule(SgmlLinkExtractor(
            allow=('/'),
            deny=('facebook.com','twitter.com','multimedia')),follow=True),
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
        news['provider'] = "thejakartaglobe.beritasatu.com"

        if "com/multimedia" in response.url:
            raise DropItem("URL not allowed")

        yield self.parse_item_default(response, news)



    def parse_item_default(self, response, news):
        news['title'] = helper.html_to_string(response.xpath("//h1").extract()[0])
        news['content'] = helper.item_merge(response.xpath("//div[@class='entry-content']").extract())
        news['title'] = helper.clear_item(news['title'])
        news['content'] = helper.clear_item(news['content'])

        author = response.xpath("//div[@class='options']/div[1]/a/text()").extract()
        if len(author) > 0:
            news['author'] = author[0]
        else:
            news['author'] = " "

        date = response.xpath("//div[@class='options']/div[1]/text()").extract()
        if len(date) > 0:
            news['publish'] = self.tg_date(date[1])
        else:
            news['publish'] = news['timestamp']

        location = response.xpath("//div[@class='entry-content']/p/strong/text()").extract()
        if len(location) > 0:
            news['location'] = location[0]
        else:
            news['location'] = " "

        return news


    def tg_date(self, plain_string):
        date_string = plain_string.split(" ")
        year = date_string[6]
        month = helper.get_month(date_string[4])
        day = date_string[5].replace(",","")

        time_string = date_string[2].split(":")
        hour =  time_string[0]
        if "pm" in date_string[3]:
            hour = str(int(hour) + 7)
        minute = time_string[1]

        return helper.formatted_date(year,month,day,hour,minute) + timedelta(hours=-7)
