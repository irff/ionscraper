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

class BbcIndoSpider(CrawlSpider):
    name = "bbcindo"
    allowed_domains = [
	    "www.bbc.co.uk",
        ]

    start_urls = ["http://www.bbc.co.uk/indonesia"]

    rules = (
        # Extract links matching 'read' and parse them with the spider's method parse_item
        # Rule(SgmlLinkExtractor(allow=('', )), follow=True),
        Rule(SgmlLinkExtractor(
            allow=('/indonesia/','/indonesia'),
            deny=('www.facebook.com','twitter.com','/privacy/','.xml')),follow=True, callback='parse_item'),
        Rule(SgmlLinkExtractor(
            allow=('/indonesia',''),
            deny=('www.facebook.com','twitter.com','/privacy/','.xml')),follow=True),
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
        news['provider'] = "bbc.co.uk/indonesia"

        if "/login" in response.url:
            raise DropItem("URL not allowed")

        yield self.parse_item_default(response, news)



    def parse_item_default(self, response, news):
        news['title'] = helper.html_to_string(response.xpath("//h1").extract()[0])
        news['content'] = helper.item_merge(response.xpath("//div[@class='story-body__inner']").extract())
        news['title'] = helper.clear_item(news['title'])
        news['content'] = helper.clear_item(news['content'])

        # BBC Indo no author
        news['author'] = " "

        date = response.css(".story-body .date::attr(data-seconds)").extract()
        if len(date) > 0:
            news['publish'] = self.bbcindo_date(date[0])
        else:
            logging.log(logging.WARNING, helper.DATE_WARN)
            news['publish'] = news['timestamp']

        news['location'] = " "
        return news



    def bbcindo_date(self, plain_string):
        return datetime.fromtimestamp(float(plain_string)) + timedelta(hours=-7)
