import scrapy
from scrapy import log
from crawler.NewsItem import NewsItem
from scrapy.contrib.spiders import CrawlSpider,  Rule
from scrapy.spider import Spider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.exceptions import DropItem
from datetime import datetime,  timedelta
import helper

"""
If you want to debug for a page,
    Change RepublikaSpider Class extends 'Spider' class
    Change start_urls with a url that you want to debug
    Change 'parse_item' method to 'parse'
If you want to crawl and follow all links ,
    Change RepublikaSpider Class extends 'CrawlSpider' class
    Change start_urls with 'http://republika.co.id'
    Change 'parse' method to 'parse_item'
"""


class BeritasatuSpider(CrawlSpider):
    name = "beritasatu"
    allowed_domains = [
        "beritasatu.com",
    ]
    start_urls = ["http://www.beritasatu.com/"]

    rules = (
        Rule(SgmlLinkExtractor(
            allow=('nasional','dunia','megapolitan','ekonomi','properti','pasar-modal','sepakbola','olahraga','iptek','kesra','gaya-hidup','food-travel','hiburan','figur','pemilu-2014'),
            deny=('reg', 'sso', 'login', 'utm_source=wp','member','video','galeri-foto','blog')),
            follow=True),
        Rule(SgmlLinkExtractor(
            allow=('\w{2}[a-zA-Z0-9](/)\d[0-9]{5}'),
            deny=('reg', 'sso', 'login', 'utm_source=wp','member','video','galeri-foto','blog'  )),
            follow=True,callback='parse_item'),

    )

    """
    if use Spider,  change function to 'parse'
    if use CrawlSpider,  change function to 'parse_item'
    """
    def parse_item(self,  response):
        self.log('Hi,  this is an item page! %s' % response.url)
        news = NewsItem()
        news['url'] = response.url

        if 'login' in response.url or 'utm_source=wp' in response.url or 'sso' in response.url or 'reg' in response.url or 'member' in response.url or 'video' in response.url or 'galeri-foto' in response.url:
                raise DropItem("URL not allowed")

        title = response.xpath("//*/h1[contains(@class, 'mtb10') and contains(@class, 'fwnormal') and contains(@class, 'f30')]/text()").extract()[0]
        publish = response.xpath("//*[contains(@class, 'c6') and contains(@class, 'left') and contains(@class, 'mt5')]/text()").extract()
        if len(publish) < 1:
            publish = response.xpath("//*[contains(@class, 'c99') and contains(@class, 'left') and contains(@class, 'mt5')]/text()").extract()
        publish = self.berita_date(publish[0])
        body = response.xpath("//*[contains(@class,'f14') and contains(@class,'c6') and contains(@class,bodyp)]").extract()
        body = helper.item_merge(body)
        author = response.xpath("//*[text()[contains(.,'Penulis')]]/text()").extract()
        if len(author) < 1:
            author = None
        elif isinstance(author,list):
            author = author[0].split("Penulis: ")
        body = helper.clear_item(body)
        body = helper.html_to_string(body)
        location = body.split("-",1)[0].strip()
        body = body.split("-",1)[1].split("Penulis",1)[0]

        news['title'] = title
        news['author'] = author
        news['publish'] = publish
        news['timestamp'] = datetime.utcnow()
        news['provider'] = "beritasatu"
        news['content'] = body
        news['location'] = location
        yield news

    def berita_date(self, plain_string):
        if plain_string is None:
            return None

        plain_string = helper.html_to_string(plain_string)

        string_date = plain_string.split(", ")[1]
        string_time = plain_string.split("| ")[1]
        date = string_date.split(" ")
        day = date[0]
        month = helper.get_month(date[1])
        year = date[2]
        hour = string_time.split(":")[0]
        minute = string_time.split(":")[1]
        return helper.formatted_date(str(year),str(month),str(day),str(hour),str(minute))