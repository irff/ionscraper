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

class RmolSpider(CrawlSpider):
    name = "rmol"

    # allowed_domains = [
	 #    "rmol.com",
    #     ]

    start_urls = ["http://rmol.co"]

    rules = (
        # Extract links matching 'read' and parse them with the spider's method parse_item
        # Rule(SgmlLinkExtractor(allow=('', )), follow=True),
        Rule(SgmlLinkExtractor(
            allow=('read'),
            deny=('facebook.com','twitter.com')),follow=True, callback='parse_item'),
        Rule(SgmlLinkExtractor(
            allow=('/','\w{1}[a-zA-Z0-9](/)\w[a-zA-Z0-9]{1}'),
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
        news['provider'] = "rmol.co"

        if "/login" in response.url or "/register" in response.url:
            raise DropItem("URL not allowed")

        yield self.parse_item_default(response, news)



    def parse_item_default(self, response, news):
        news['title'] = response.xpath("//head/title/text()").extract()[0]
        news['content'] = helper.item_merge(response.xpath("//*[@id='primary-column']/p[1]").extract())
        news['content'] = helper.clear_item(news['content'])

        author = response.xpath("//*[@id='primary-column']/div[4]/font/text()").extract()
        if len(author) > 0:
            news['author'] = author[0]
        else:
            news['author'] = " "

        date = response.url.split("/")
        if len(date) > 0:
            news['publish'] = self.rmol_date_from_url(date)
        else:
            news['publish'] = news['timestamp']

        news['location'] = " "

        return news

    def rmol_date_from_url(self, url):
        return helper.formatted_date(url[4], url[5], url[6], "00", "00") - timedelta(hours=-7)
