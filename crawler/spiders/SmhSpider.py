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

class HuffingtonpostSpider(CrawlSpider):
    name = "smh"

    allowed_domains = [
	    "smh.com.au",
        ]

    start_urls = ["http://www.smh.com.au"]

    rules = (
        # Extract links matching 'read' and parse them with the spider's method parse_item
        # Rule(SgmlLinkExtractor(allow=('', )), follow=True),
        Rule(SgmlLinkExtractor(
            allow=('(-)\d{8}(-)'),
            deny=('facebook.com','twitter.com','mobile-phones.smh.com.au')),follow=True, callback='parse_item'),
        Rule(SgmlLinkExtractor(
            allow=('(com.au/)\w{1}[A-Za-z0-9]','/','/subscribe?','/comment/'),
            deny=('facebook.com','twitter.com','mobile-phones.smh.com.au')),follow=True),
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
        news['provider'] = "smh.com.au"

        if "/subscribe?" in response.url or "mobile-phones.smh.com.au" in response.url:
            raise DropItem("URL not allowed")

        yield self.parse_item_default(response, news)



    def parse_item_default(self, response, news):
        news['title'] = helper.html_to_string(response.xpath("//head/title").extract()[0])
        news['content'] = helper.item_merge(response.xpath("//div[@itemprop='articleBody']").extract())
        news['title'] = helper.clear_item(news['title'])
        news['content'] = helper.clear_item(news['content'])

        news['author'] = " "

        date = response.xpath("//time/text()").extract()
        if len(date) > 0:
            news['publish'] = self.smh_date(date[0])
        else:
            news['publish'] = news['timestamp']

        news['location'] = " "

        return news

    def smh_date(self, date_string):
        date_string = helper.clear_item(date_string)

        d = date_string.split(" ")

        if len(d) > 0:
            return datetime.utcnow()

        log.msg(str(d),log.CRITICAL)
        year = d[2 + 16]
        month = helper.get_month(d[0 + 16])
        day = d[1 + 16][:len(d[1 + 16])-1]

        hour =  "00"
        minute = "00"
        return helper.formatted_date(year,month,day,hour,minute) + timedelta(hours=-7)
