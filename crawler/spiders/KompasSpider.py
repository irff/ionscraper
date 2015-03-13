import scrapy
from scrapy import log
from crawler.NewsItem import NewsItem
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.spider import Spider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.exceptions import DropItem
from datetime import datetime
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
class KompasSpider(Spider):
    name = "kompas"
    allowed_domains = [
        "nasional.kompas.com",
        "regional.kompas.com",
        "megapolitan.kompas.com",
        "internasional.kompas.com",
        "olahraga.kompas.com",
        "bola.kompas.com",
        "sains.kompas.com",
        "edukasi.kompas.com",
        "bisniskeuangan.kompas.com",
        "tekno.kompas.com"
        ]
    start_urls = ["http://edukasi.kompas.com/read/2015/03/12/19493501/Anak.di.Bawah.Usia.3.Tahun.Juga.Perlu.Pendidikan?utm_campaign=Ktkwp&utm_medium=box&utm_source=WP"]
    rules = (
        # Extract links matching 'read' and parse them with the spider's method parse_item
        # Rule(SgmlLinkExtractor(allow=('', )), follow=True),
        Rule(SgmlLinkExtractor(allow=('/index/', ), deny=('/reg/','/sso/','/login/'))),
        Rule(SgmlLinkExtractor(allow=('/read/', )),follow=True, callback='parse_item'),

    )

    """
    if use Spider, change function to 'parse'
    if use CrawlSpider, change function to 'parse_item'
    """
    def parse(self, response):
        self.log('Hi, this is an item page! %s' % response.url)
        news = NewsItem()
        news['url'] = response.url

        if 'login' in response.url:
            raise DropItem("URL not allowed")

        if 'tekno.kompas.com' in response.url:
            raise DropItem("Ini tekno.kompas")
        else:

            """Getting Title"""
            if 'bola.kompas.com' in response.url:
                title = response.xpath('//html/body/div/div[6]/div/div[1]/div[1]/div[2]/h2').extract()[0]
            else:
                title = response.xpath('//h2/text()').extract()[0]

            if len(title):
                news['title'] = title
            else:
                raise DropItem("No title")

            """Getting Content"""
            content = response.xpath('//span[@class="kcmread1114"]').extract()
            if len(content) > 0:
                news['content'] = helper.html_to_string(content[0])
            else:
                raise DropItem("No content")

            """Getting Publish date"""""
            publish = response.xpath('//div[@class="grey small mb2"]/text()').extract()
            if len(publish) > 0:
                news['publish'] = helper.kompas_date(publish[0])
            else:
                news['publish'] = "";

            """Getting Author"""
            author = response.xpath('//html/body/div[1]/div[6]/div/div[1]/div[3]/div[3]/div[2]/div[2]/table/tbody/tr[1]/td[2]').extract()
            if len(author) > 0:
                news['author'] = helper.html_to_string(author[0])
            else:
                news['author'] = " ";

            """Getting location of news"""
            location = news['content'][0:news['content'].find(',')]
            news['location'] = location

            """Getting Timestamp and Provider"""
            news['timestamp']= datetime.utcnow()
            news['provider'] = "kompas.com"
            yield news