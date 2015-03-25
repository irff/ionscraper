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

class BisnisSpider(CrawlSpider):
    name = "bisnis"
    allowed_domains = [
	    "bisnis.com",
		"kabar24.bisnis.com",
        "market.bisnis.com",
        "finansial.bisnis.com",
        "industrial.binsis.com",
        "otomotif.bisnis.com",
        "jakarta.bisnis.com",
        "bola.bisnis.com",
        "lifestyle.bisnis.com",
        "gadget.bisnis.com",
        "properti.bisnis.com",
        "sport.bisnis.com",
        "traveling.bisnis.com",
        "koran.bisnis.com",
        "syariah.bisnis.com",
        "manajemen.bisnis.com",
        "entrepreneur.bisnis.com",
        "info.bisnis.com",
        "inforial.bisnis.com",
        "foto.bisnis.com",
        "bali.bisnis.com",
        "sulawesi.bisnis.com",
        "bandung.bisnis.com",
        "semarang.bisnis.com",
        "surabaya.bisnis.com",
        "sumatra.bisnis.com",
        ]

    start_urls = ["http://bisnis.com"]

    rules = (
        # Extract links matching 'read' and parse them with the spider's method parse_item
        # Rule(SgmlLinkExtractor(allow=('', )), follow=True),
        Rule(SgmlLinkExtractor(
            allow=('read/','watch/','view/'),
            deny=('/registrasi/','bigstore.bisnis.com','/forgot/','/kupon/','business.bisnis.com','id.bisnis.com')),follow=True, callback='parse_item'),
        Rule(SgmlLinkExtractor(
            allow=('read/',''),
            deny=('/registrasi/','/forgot/','/kupon/','bigstore.bisnis.com','business.bisnis.com','id.bisnis.com')),follow=True),
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
        news['provider'] = "bisnis.com"

        if "/forgot/" in response.url or "/kupon/" in response.url:
            raise DropItem("URL not allowed")

        if "foto.bisnis.com" in response.url:
            yield self.parse_item_foto(response, news)
        elif "sulawesi.bisnis.com" in response.url:
            yield self.parse_item_regional(response, news)
        elif "bandung.bisnis.com" in response.url:
            yield self.parse_item_regional(response, news)
        elif "semarang.bisnis.com" in response.url:
            yield self.parse_item_regional(response, news)
        elif "surabaya.bisnis.com" in response.url:
            yield self.parse_item_regional(response, news)
        elif "sumatra.bisnis.com" in response.url:
            yield self.parse_item_regional(response, news)
        elif "bali.bisnis.com" in response.url:
            yield self.parse_item_regional(response, news)
        elif "business.bisnis.com" in response.url:
            log.msg("Need Login: %s" % response.url, level=log.ERROR)
        else:
            yield self.parse_item_default(response, news)


    def parse_item_default(self, response, news):
        news['title'] = helper.html_to_string(response.xpath("//h1").extract()[0])
        news['content'] = helper.html_to_string(response.xpath("//div[@class='description']").extract()[0])
        news['title'] = helper.clear_item(news['title'])
        news['content'] = helper.clear_item(news['content'])

        author = response.xpath("//span[@class='editor']/text()").extract();
        if len(author) > 0:
            news['author'] = author[0]
        else:
            news['author'] = " "

        date = response.xpath("//div[@class='col-md-8 col-sm-12 col-xs-12 details']/span[@class='date']/text()").extract()
        if len(date) > 0:
            news['publish'] = self.bisnis_date(date[0])
        else:
            news['publish'] = self.bisnis_date_from_url(response.url)

        if "Bisnis.com" in news['content']:
            news['location'] = news['content'][news['content'].find(','):news['content'].find('-')]
        else:
            if "-" in news['content']:
                news['location'] = news['content'][0:news['content'].find('-')]
            else:
                news['location'] = " "
        return news

    def parse_item_foto(self, response, news):
        news['title'] = helper.html_to_string(response.xpath("//h1").extract()[0])
        news['content'] = helper.html_to_string(response.xpath("//div[@class='details-photo col-md-12 pb-30']/div[4]/p").extract()[0])
        news['title'] = helper.clear_item(news['title'])
        news['content'] = helper.clear_item(news['content'])

        author = response.xpath("//div[@class='editor mt-20']/text()").extract();
        if len(author) > 0:
            news['author'] = author[0]
        else:
            news['author'] = " "

        news['publish'] = self.bisnis_date_from_url(response.url)

        news['location'] = " "

        return news

    def parse_item_regional(self, response, news):
        news['title'] = helper.html_to_string(response.xpath("//div[@class='leftcol post-detail']/h1").extract()[0])
        news['content'] = helper.html_to_string(response.xpath("//div[@class='entry-right']").extract()[0])
        news['title'] = helper.clear_item(news['title'])
        news['content'] = helper.clear_item(news['content'])

        author = response.xpath("//div[@class='entry-editor']").extract();
        if len(author) > 0:
            news['author'] = helper.html_to_string(author[0])
        else:
            news['author'] = " "

        date = response.xpath("//span[@class='date']").extract()
        if len(date) > 0:
            date[0] = helper.html_to_string(date[0])
            news['publish'] = self.bisnis_regional_date(date[0])
        else:
            news['publish'] = self.bisnis_date_from_url(response.url)

        if "Bisnis.com" in news['content']:
            news['location'] = news['content'][news['content'].find(','):news['content'].find('-')]
        else:
            news['location'] = " "

        return news


    def bisnis_date(self, plain_string):
        if plain_string == None:
            return None

        plain_string = helper.html_to_string(plain_string)

        string_date = plain_string[plain_string.find(",") + 2 : plain_string.find(",") + 12]
        string_time = plain_string[plain_string.find(",") + 13 : plain_string.find(",") + 18]

        date = string_date.split("/")
        day = date[0]
        month = date[1]
        year = date[2]
        hour = string_time[0:2]
        minute = string_time[3:5]
        return helper.formatted_date(year,month,day,hour,minute) + timedelta(hours=-7)

    def bisnis_regional_date(self, plain_string):
        if plain_string == None:
            return None


        string_date = plain_string[plain_string.find("-") + 2 : plain_string.find(",")].strip()
        string_time = plain_string[plain_string.find(",") + 2: len(plain_string)].strip()
        date = string_date.split(" ")
        day = date[0]
        ms = date[1]
        month = helper.get_month(ms)
        year = date[2]
        hour = string_time[0:2]
        minute = string_time[3:5]

        return helper.formatted_date(year,month,day,hour,minute) + timedelta(hours=-7)

    def bisnis_date_from_url(self, url):
        if url == None:
            return None

        u = url.split("/")
        date = u[4]
        return helper.formatted_date( date[0:4], date[4:6], date[6:8], "00", "00") + timedelta(hours=-7)
