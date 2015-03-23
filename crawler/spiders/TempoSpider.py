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
    start_urls = ["http://www.tempo.co/read/news/2015/01/27/078637910/Nurul-Arifin-Jokowi-Direcoki-Partai-Pendukung"]
    #start_urls = ["http://www.tempo.co/read/news/2015/02/04/140639978/Tahun-2015-Wajib-Kunjungi-Filipina"]
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
            title = helper.html_to_string(response.xpath("//h4[1]").extract()[0])
            content = helper.html_to_string(helper.item_merge(response.xpath("//*[@class='artikel']/p").extract()))
            content = content.split('-',1)[1].rsplit('.',1)[0]
            publish = helper.html_to_string(response.xpath("//*[@class='date']").extract()[0])
            location = helper.html_to_string(response.xpath("//strong").extract()[1])
            author = helper.html_to_string(response.xpath("//strong").extract()[-2])
            publish = helper.tempo_komunika_date(publish)
        else:
            title = helper.html_to_string(response.xpath("//*[@class='title']").extract()[0])
            content = helper.html_to_string(helper.item_merge(response.xpath("//*[@class='artikel']/p").extract()))
            details = response.xpath("//*[@class='artikel']/p/strong/text()").extract()
            if "populer" in details[-1]:
                location = details[1]
                author = details[2]
            else:
                location = helper.html_to_string(response.xpath("//strong").extract()[-2])
                author = content.rsplit('.',1)[1]
            content = content.split('-',1)[1].rsplit('.',1)[0]
            publish =  self.tempo_date(helper.html_to_string(response.xpath("//*[@class='submitted']").extract()[0]))
            
        news['title'] = title
        news['content'] = content
        news['publish'] = publish
        news['author'] = author
        news['location'] = location.replace('-','').strip()
        news['timestamp']= datetime.utcnow()
        news['provider'] = "tempo.co"
        
        yield news

    def tempo_date(self, plain_string):
        if plain_string == None:
            return None

        plain_string = helper.html_to_string(plain_string)

        string_date = plain_string[plain_string.find(",") + 2 : plain_string.find("|") - 1]
        string_time = plain_string[plain_string.find("|") + 2 : len(plain_string)]

        date = string_date.split(" ")
        day = date[0]
        year = date[2]
        ms = date[1]
        month = helper.get_month(ms)
        hour = string_time[0:2]
        minute = string_time[3:5]

        return helper.formatted_date(year,month,day,hour,minute)