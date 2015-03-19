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


class TempoSpider(CrawlSpider):
    name = "tempo"
    allowed_domains = ["tempo.co","komunika.tempo.co",]
    #"http://komunika.tempo.co/read/news/2015/02/04/273639939/ujian-nasional-online-jangan-sampai-server-ngadat",
    #"http://www.tempo.co/read/news/2015/03/19/063651357/Jusuf-Kalla-Pelaporan-Majalah-Tempo-Urusan-Dewan-Pers",
    #"http://komunika.tempo.co/read/news/2015/02/04/273639932/cara-menteri-arief-gaet-1-juta-wisman-per-bulan",
    start_urls = ["http://tempo.co"]

    rules = (
        Rule(SgmlLinkExtractor(allow=('indeks'), deny=('reg','sso','login','utm_source=wp')),follow=True),
        Rule(SgmlLinkExtractor(allow=('read/'), deny=('reg','sso','login','utm_source=wp')),follow=True, callback='parse_item'),

    )

    """
    if use Spider, change function to 'parse'
    if use CrawlSpider, change function to 'parse_item'
    """
    def parse_item(self, response):
        self.log('Hi, this is an item page! %s' % response.url)
        news = NewsItem()
        news['url'] = response.url

        if 'login' in response.url or 'utm_source=wp' in response.url or 'sso' in response.url or 'reg' in response.url:
            raise DropItem("URL not allowed")

        if 'komunika' in response.url:
            title = helper.html_to_string(response.xpath("//*[@id='main-left-620']/div/div[1]/div[1]/h4").extract()[0])
            content = helper.paragraph_aggregator(response.xpath("//*[@id='main-left-620']/div/div[1]/div[1]/p").extract())
            publish =  helper.html_to_string(response.xpath("//*[@id='main-left-620']/div/div[1]/div[1]/div[1]").extract()[0])
            author = content.rsplit('.',1)[1]
            location = helper.html_to_string(response.xpath("//*[@id='main-left-620']/div/div[1]/div[1]/p[2]/span[2]/strong").extract()[0])
            content = content.split('-',1)[1]
            content = content.rsplit('.',1)[0]
            publish = helper.tempo_komunika_date(publish)
        else:
            title = helper.html_to_string(response.xpath("//*[@id='content']/h1").extract()[0])
            content = helper.html_to_string(response.xpath("//*[@id='content']/div[5]/p").extract()[0])
            publish =  helper.kompas_date(helper.html_to_string(response.xpath("//*[@id='content']/div[2]").extract()[0]))
            author = response.xpath("//*[@id='content']/div[5]/p[2]/strong[3]").extract()[0]
            location = helper.html_to_string(response.xpath("//*[@id='content']/div[5]/p[2]/strong[2]").extract()[0])
            content = content.split('-',1)[1]
            content = content.rsplit('.',1)[0]
            author = helper.html_to_string(author)

        news['title'] = title
        news['content'] = content
        news['publish'] = publish
        news['author'] = author
        news['location'] = location
        news['timestamp']= datetime.utcnow()
        news['provider'] = "tempo.co"
        
        yield news