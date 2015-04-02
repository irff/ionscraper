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

class VivaSpider(CrawlSpider):
    name = "viva"

    allowed_domains = [
	    "www.viva.co.id",
        "news.viva.co.id",
        "politik.news.viva.co.id",
        "bisnis.news.viva.co.id",
        "nasional.news.viva.co.id",
        "metro.news.viva.co.id",
        "dunia.news.viva.co.id",
        "teknologi.viva.co.id",
        "sport.news.viva.co.id",
        "analisis.news.viva.co.id",
        "fokus.news.viva.co.id",
        "bola.viva.co.id",
        "live.viva.co.id",
        "foto.viva.co.id"
        ]

    start_urls = ["http://www.viva.co.id"]

    rules = (
        # Extract links matching 'read' and parse them with the spider's method parse_item
        # Rule(SgmlLinkExtractor(allow=('', )), follow=True),
        Rule(SgmlLinkExtractor(
            allow=('/news','/read'),
            deny=('facebook.com','twitter.com','m.viva.co.id')),follow=True, callback='parse_item'),
        Rule(SgmlLinkExtractor(
            allow=('/indeks','/','/indeks?page'),
            deny=('facebook.com','twitter.com','m.viva.co.id')),follow=True),
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
        news['provider'] = "viva.co.id"

        if "m.viva.co.id" in response.url:
            raise DropItem("URL not allowed")

        if 'foto.viva' in response.url:
            yield self.parse_item_foto(response, news)
        else:
            yield self.parse_item_default(response, news)



    def parse_item_default(self, response, news):
        news['title'] = helper.html_to_string(response.xpath("//h1").extract()[0])
        news['content'] = helper.item_merge(response.xpath("//div[@id='article-content']").extract())
        news['title'] = helper.clear_item(news['title'])
        news['content'] = helper.clear_item(news['content'])

        author = response.xpath("//div[@class='author']/b/text()").extract()
        if len(author) > 0:
            news['author'] = author[0]
        else:
            news['author'] = " "

        date = response.xpath("//div[@class='date']/text()").extract()
        if len(date) > 0:
            news['publish'] = self.viva_date(date[0])
        else:
            news['publish'] = news['timestamp']

        news['location'] = " "

        return news

    def parse_item_foto(self, response, news):
        news['title'] = helper.html_to_string(response.xpath("//h1").extract()[0])
        news['content'] = helper.item_merge(response.xpath("//div[@class='summary']").extract())
        news['title'] = helper.clear_item(news['title'])
        news['content'] = helper.clear_item(news['content'])

        news['author'] = " "

        date = response.xpath("//div[@class='date fr']/text()").extract()
        if len(date) > 0:
            news['publish'] = self.viva_date(date[0])
        else:
            news['publish'] = news['timestamp']

        news['location'] = " "

        return news

    def viva_date(self, plain_string):
        date_string = plain_string.split(" ")
        year = date_string[3]
        month = helper.get_month(date_string[2])
        day = date_string[1]

        time_string = date_string[5].split(":")
        hour =  time_string[0]
        minute = time_string[1]
        return helper.formatted_date(year,month,day,hour,minute) + timedelta(hours=-7)
