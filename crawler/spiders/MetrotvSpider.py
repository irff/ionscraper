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

class MetrotvSpider(CrawlSpider):
    name = "metrotv"

    allowed_domains = [
	    "www.metrotvnews.com",
        "news.metrotvnews.com",
        "jatim.metrotvnews.com",
        "jabar.metrotvnews.com",
        "internasional.metrotvnews.com",
        "ekonomi.metrotvnews.com",
        "bola.metrotvnews.com",
        "olahraga.metrotvnews.com",
        "teknologi.metrotvnews.com",
        "otomotif.metrotvnews.com",
        "hiburan.metrotvnews.com",
        "rona.metrotvnews.com"
        ]

    start_urls = ["http://www.metrotvnews.com"]

    rules = (
        # Extract links matching 'read' and parse them with the spider's method parse_item
        # Rule(SgmlLinkExtractor(allow=('', )), follow=True),
        Rule(SgmlLinkExtractor(
            allow=('/read'),
            deny=('www.facebook.com','twitter.com','foto.metrotvnews.com')),follow=True, callback='parse_item'),
        Rule(SgmlLinkExtractor(
            allow=('/','','index'),
            deny=('www.facebook.com','twitter.com','foto.metrotvnews.com')),follow=True),
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
        news['provider'] = "metrotvnews.com"

        if "/login" in response.url:
            raise DropItem("URL not allowed")

        if "jatim.metrotvnews" in response.url or "jabar.metrotvnews.com" in response.url:
            yield self.parse_item_jatimbar(response, news)
        else:
            yield self.parse_item_default(response, news)


    def parse_item_default(self, response, news):
        news['title'] = helper.html_to_string(response.xpath("//h1").extract()[0])
        news['content'] = helper.item_merge(response.xpath("//div[@class='info demo']").extract())
        news['title'] = helper.clear_item(news['title'])
        news['content'] = helper.clear_item(news['content'])

        author = response.xpath("//div[@class='nate']/text()").extract()
        if len(author) > 0:
            news['author'] = author[0]
        else:
            news['author'] = " "

        date = response.xpath("//div[@class='nate']/span/text()").extract()
        if len(date) > 0:
            if "WIB" in date[0]:
                news['publish'] = self.metrotv_date(date[0])
            else:
                news['publish'] = self.metrotv_date_from_url(response.url)
        else:
            news['publish'] = news['timestamp']

        location = response.xpath("//div[@class='info demo']/strong/text()").extract()
        if len(location) > 0:
            location = location[0].split(",")
            if len(location) > 1:
                news['location'] = location[1]
            else:
                news['location'] = " "
        else:
            news['location'] = " "
        return news

    def parse_item_jatimbar(self, response, news):
        news['title'] = helper.html_to_string(response.xpath("//h1").extract()[0])
        news['content'] = helper.item_merge(response.xpath("//div[@class='article']").extract())
        news['title'] = helper.clear_item(news['title'])
        news['content'] = helper.clear_item(news['content'])

        author_date = response.xpath("//span[@class='red']/text()").extract()

        author = ""
        date = ""
        if len(author_date) > 0:
            ad = author_date[0].split("-")
            author = ad[0]
            date = ad[1]

        if len(author) > 0:
            news['author'] = author
        else:
            news['author'] = " "

        if len(date) > 0:
            if "WIB" in date:
                news['publish'] = self.metrotv_date(date)
            else:
                news['publish'] = self.metrotv_date_from_url(response.url)
        else:
            news['publish'] = news['timestamp']

        location = response.xpath("//div[@class='article']/strong/text()").extract()
        if len(location) > 0:
            location = location[0].split(",")
            if len(location) > 1:
                news['location'] = location[1]
            else:
                news['location'] = " "
        else:
            news['location'] = " "
        return news


    def metrotv_date(self, plain_string):
        date_string = plain_string.split(" ")
        year = date_string[3]
        month = helper.get_month(date_string[2])
        day = date_string[1]

        time_string = date_string[4].split(":")
        hour =  time_string[0]
        minute = time_string[1]
        return helper.formatted_date(year,month,day,hour,minute) + timedelta(hours=-7)

    def metrotv_date_from_url(self, url):
        if url == None:
            return None

        u = url.split("/")

        return helper.formatted_date(u[4], u[5], u[6], "00", "00") - timedelta(hours=-7)
