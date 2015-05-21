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
import re

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

class DetikSpider(CrawlSpider):
    name = "detik"

    allowed_domains = [
	    "detik.com",
        ]

    start_urls = ["http://www.detik.com/"]

    rules = (
        # Extract links matching 'read' and parse them with the spider's method parse_item
        # Rule(SgmlLinkExtractor(allow=('', )), follow=True),
        Rule(SgmlLinkExtractor(
            allow=('/read'),
            deny=('facebook.com','twitter.com','connect.detik','m.detik','tv.detik')),follow=True, callback='parse_item'),
        Rule(SgmlLinkExtractor(
            allow=('indeks','/'),
            deny=('facebook.com','twitter.com','connect.detik','m.detik','tv.detik')),follow=True),
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
        news['provider'] = "detik.com"

        if "user/login" in response.url or "user/register" in response.url:
            raise DropItem("URL not allowed")

        if "news.detik.com" in response.url:
            yield self.parse_item_news(response, news)
        else:
            yield self.parse_item_default(response, news)



    def parse_item_default(self, response, news):
        news['title'] = helper.html_to_string(response.xpath("//head/title").extract()[0])
        news['content'] = helper.item_merge(response.xpath("//div[@class='text_detail']").extract())
        news['title'] = helper.clear_item(news['title'])
        news['content'] = helper.clear_item(news['content'])

        author = response.xpath("//div[@class='author']/strong/text()").extract()
        if len(author) > 0:
            news['author'] = author[0]
        else:
            news['author'] = " "

        news['publish'] = self.detik_date(response.url)

        location = response.xpath("//div[@class='text_detail']/strong/text()").extract()
        if len(location) > 0:
            news['location'] = location[0]
        else:
            news['location'] = " "

        return news

    def parse_item_news(self, response, news):
        news['title'] = helper.html_to_string(response.xpath("//head/title").extract()[0])
        news['content'] = helper.item_merge(response.xpath("//div[@class='artikel2']").extract())
        news['title'] = helper.clear_item(news['title'])
        news['content'] = helper.clear_item(news['content'])

        author = response.xpath("//div[@class='author']/strong/text()").extract()
        if len(author) > 0:
            news['author'] = author[0]
        else:
            news['author'] = " "

        news['publish'] = self.detik_date(response.url)

        location = response.xpath("//div[@class='artikel2']/strong/text()").extract()
        if len(location) > 0:
            news['location'] = location[0]
        else:
            news['location'] = " "

        return news

    def detik_date(self, url):
        regex = re.compile("\d{4}(/)\d{2}(/)\d{2}")
        urls = url.split("/")

        if regex.match(urls[4]+"/"+urls[5]+"/"+urls[6]):
            year = urls[4]
            month = urls[5]
            day = urls[6]
        else:
            year = urls[5]
            month = urls[6]
            day = urls[7]

        hour =  "00"
        minute = "00"
        return helper.formatted_date(year,month,day,hour,minute) + timedelta(hours=-7)
