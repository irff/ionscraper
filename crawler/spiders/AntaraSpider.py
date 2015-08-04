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
import logging

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

class AntaraSpider(CrawlSpider):
    name = "antara"

    allowed_domains = [
	    "www.antaranews.com",
        ]

    start_urls = ["http://www.antaranews.com"]

    rules = (
        # Extract links matching 'read' and parse them with the spider's method parse_item
        # Rule(SgmlLinkExtractor(allow=('', )), follow=True),
        Rule(SgmlLinkExtractor(
            allow=('/berita/','/berita','/foto/'),
            deny=('facebook.com','twitter.com')),follow=True, callback='parse_item'),
        Rule(SgmlLinkExtractor(
            allow=('/berita/','/berita','/foto/','/foto',''),
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
        news['provider'] = "antaranews.com"

        if "user/login" in response.url or "user/register" in response.url:
            raise DropItem("URL not allowed")

        if "otomotif.antaranews.com" in response.url:
            yield self.parse_item_otomotif(response, news)
        if "antaranews.com/foto" in response.url:
            yield self.parse_item_foto(response, news)
        if "pemilu/berita" in response.url:
            yield self.parse_item_pemilu(response, news)
        else:
            yield self.parse_item_default(response, news)



    def parse_item_default(self, response, news):
        news['title'] = helper.html_to_string(response.xpath("//h1[@class='title']/strong").extract()[0])
        news['content'] = helper.item_merge(response.xpath("//div[@itemprop='articleBody']").extract())
        news['title'] = helper.clear_item(news['title'])
        news['content'] = helper.clear_item(news['content'])

        author = response.xpath("//span[@itemprop='editor']/text()").extract()
        if len(author) > 0:
            news['author'] = author[0]
        else:
            news['author'] = " "

        date = response.css("time::attr(datetime)").extract()
        if len(date) > 0:
            news['publish'] = self.antara_date(date[0])
        else:
            logging.log(logging.WARNING, helper.DATE_WARN)
            news['publish'] = news['timestamp']

        if "(ANTARA News)" in news['content']:
            news['location'] = news['content'][0:news['content'].find('(')]
        else:
            news['location'] = " "

        return news

    def parse_item_otomotif(self, response, news):
        news['title'] = helper.html_to_string(response.xpath("//h1[@class='title']/strong").extract()[0])
        news['content'] = helper.item_merge(response.xpath("//div[@id='content_news']").extract())
        news['title'] = helper.clear_item(news['title'])
        news['content'] = helper.clear_item(news['content'])

        # no author
        news['author'] = " "

        date = response.xpath("//div[@class='date mt10']/text()").extract()
        if len(date) > 0:
            news['publish'] = self.antara_date_otomotif(date[0])
        else:
            logging.log(logging.WARNING, helper.DATE_WARN)
            news['publish'] = news['timestamp']

        if "(ANTARA News)" in news['content']:
            news['location'] = news['content'][0:news['content'].find('(')]
        else:
            news['location'] = " "

        return news

    def parse_item_pemilu(self, response, news):
        news['title'] = helper.html_to_string(response.xpath("//h1").extract()[0])
        news['content'] = helper.html_to_string(response.xpath("//div[@class='news_content']").extract()[0])
        news['title'] = helper.clear_item(news['title'])
        news['content'] = helper.clear_item(news['content'])

        # no author
        author = response.xpath("//div[@class='byline']/text()").extract()
        if len(author) > 0:
            news['author'] = author[0]
        else:
            news['author'] = " "

        date = response.xpath("//div[@class='date']/text()").extract()
        if len(date) > 0:
            news['publish'] = self.antara_date_otomotif(date[0])
        else:
            logging.log(logging.WARNING, helper.DATE_WARN)
            news['publish'] = news['timestamp']

        content = response.xpath("//div[@class='news_content']").extract()
        if len(content) > 0:
            if len(content[0]) > 16:
                news['location'] = content[0][content[0].find("</script>\n</div>") + 16:content[0].find("(ANTARA News)")]
            else:
                news['location'] = " "
        else:
            news['location'] = " "

        return news


    def parse_item_foto(self, response, news):
        news['title'] = helper.html_to_string(response.xpath("//h1[@class='title']/strong").extract()[0])
        news['content'] = helper.item_merge(response.xpath("//div[@id='descriptions']").extract())
        news['title'] = helper.clear_item(news['title'])
        news['content'] = helper.clear_item(news['content'])

        # no author
        news['author'] = " "

        date = response.xpath("//div[@class='date mt10']/text()").extract()
        if len(date) > 0:
            logging.log(logging.WARNING, helper.DATE_WARN)
            news['publish'] = self.antara_date_otomotif(date[0])
        else:
            news['publish'] = news['timestamp']

        # no location
        news['location'] = " "

        return news

    def antara_date(self, plain_string):
        date_string = plain_string[0:10]
        time_string = plain_string[11:19]
        year = date_string[0:4]
        month = date_string[5:7]
        day = date_string[8:10]
        hour =  time_string[0:2]
        minute = time_string[3:5]
        second = time_string[6:8]
        return helper.formatted_date_with_second(year,month,day,hour,minute,second) + timedelta(hours=-7)

    def antara_date_otomotif(self, plain_string):
        date_string = plain_string.split(" ")

        year = date_string[3]
        ms = date_string[2]
        month = helper.get_month(ms)
        day = date_string[1]

        time = date_string[4].split(":")
        hour =  time[0]
        minute = time[1]
        return helper.formatted_date(year,month,day,hour,minute) + timedelta(hours=-7)
