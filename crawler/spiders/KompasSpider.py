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
class KompasSpider(Spider):
    name = "kompas"
    allowed_domains = [
	    "kompas.com",
		"indeks.kompas.com",
        "nasional.kompas.com",
        "regional.kompas.com",
        "megapolitan.kompas.com",
        "internasional.kompas.com",
        "olahraga.kompas.com",
        "sains.kompas.com",
        "edukasi.kompas.com",
        "bisniskeuangan.kompas.com",
        "bola.kompas.com",
        "tekno.kompas.com",
        "entertaintment.kompas.com",
        "otomotif.kompas.com",
        "health.kompas.com",
        "female.kompas.com",
        "properti.kompas.com",
        "travel.kompas.com",
        ]
    # start_urls = [  "http://kompas.com",
	# 				#"http://indeks.kompas.com/?tanggal=1&bulan=3&tahun=2008&pos=indeks",
	# 				#"http://indeks.kompas.com/?tanggal=1&bulan=4&tahun=2008&pos=indeks",
	# 				#"http://indeks.kompas.com/?tanggal=1&bulan=5&tahun=2008&pos=indeks",
	# 				#"http://indeks.kompas.com/?tanggal=1&bulan=6&tahun=2008&pos=indeks",
	# 				#"http://indeks.kompas.com/?tanggal=1&bulan=7&tahun=2008&pos=indeks",
	# 				#"http://indeks.kompas.com/?tanggal=1&bulan=8&tahun=2008&pos=indeks",
	# 				#"http://indeks.kompas.com/?tanggal=1&bulan=9&tahun=2008&pos=indeks",
	# 				#"http://indeks.kompas.com/?tanggal=1&bulan=10&tahun=2008&pos=indeks",
	# 				#"http://indeks.kompas.com/?tanggal=1&bulan=11&tahun=2008&pos=indeks",
	# 				#"http://indeks.kompas.com/?tanggal=1&bulan=12&tahun=2008&pos=indeks",
	# ]

    start_urls = ["http://nasional.kompas.com/read/2015/03/19/12142221/Tedjo.7.WN.Tiongkok.Terduga.ISIS.Bergabung.dengan.Kelompok.Poso"]

    rules = (
        # Extract links matching 'read' and parse them with the spider's method parse_item
        # Rule(SgmlLinkExtractor(allow=('', )), follow=True),
        Rule(SgmlLinkExtractor(allow=('indeks','p=',), deny=('reg','sso','login','utm_source=wp')),follow=True),
        Rule(SgmlLinkExtractor(allow=('read/', 'read/xml/',), deny=('reg','sso','login','utm_source=wp')),follow=True, callback='parse_item'),
    )

    """
    if use Spider, change function to 'parse'
    if use CrawlSpider, change function to 'parse_item'
    """
    def parse(self, response):
        self.log('Hi, this is an item page! %s' % response.url)
        news = NewsItem()
        news['url'] = response.url

        if 'login' in response.url or 'utm_source=wp' in response.url or 'sso' in response.url or 'reg' in response.url:
            raise DropItem("URL not allowed")


        """Getting Title"""
        if 'bola.kompas.com' in response.url:
            title = response.xpath('//html/body/div/div[6]/div/div[1]/div[1]/div[2]/h2/text()').extract()
        elif 'tekno.kompas.com' in response.url:
            title = response.xpath('//html/body/div[1]/div[2]/div[5]/div[1]/div[2]/div/div[2]/div[1]/h1').extract()
        elif 'entertainment.kompas.com' in response.url:
            title = response.xpath('//html/body/div[2]/div/div/div[7]/div[4]/span[2]/text()').extract()
        elif 'otomotif.kompas.com' in response.url:
            title = response.xpath('//*[@id="skrol"]/div[1]/div[4]/h1/text()').extract()
        elif 'health.kompas.com' in response.url:
            title = response.xpath('//html/body/div[3]/div[4]/div[4]/h1/text()').extract()
        elif 'female.kompas.com' in response.url:
            title = response.xpath('//*[@id="wrap-skin"]/div/div[2]/div/div[1]/div[8]/div[3]/div[2]').extract()
        elif 'properti.kompas.com' in response.url:
            title = response.xpath('//html/body/div[1]/div[5]/div[3]/div[1]/div[2]/text()').extract()
        else:
            title = response.xpath('//h2/text()').extract()

        news['title'] = title[0]


        """Getting Content"""
        if 'tekno.kompas.com' in response.url:
            content = response.xpath('//html/body/div[1]/div[2]/div[5]/div[1]/div[2]/div/div[2]/div[2]/div[4]/text()').extract()
        elif 'entertainment.kompas.com' in response.url:
            content = response.xpath('//html/body/div[2]/div/div/div[7]/div[4]/div[9]/div[5]/text()').extract()
        elif 'otomotif.kompas.com' in response.url:
            content = response.xpath('//*[@id="skrol"]/div[1]/div[4]/div[4]/div[1]/p/text()').extract()
        elif 'health.kompas.com' in response.url:
            content = response.xpath('//html/body/div[3]/div[4]/div[4]/div[6]/div[5]/text()').extract()
        elif 'female.kompas.com' in response.url:
            content = response.css('#article_body').extract()[0]
        elif 'properti.kompas.response' in response.url:
            content = response.xpath('//html/body/div[1]/div[5]/div[3]/div[1]/div[8]/div[5]/text()').extract()
        elif 'travel.kompas.com' in response.url:
            content = response.css('.nml').extract()
        else:
            content = response.xpath('//span[@class="kcmread1114"]/p/text()').extract()

        news['content'] = content[0]

        """Getting Publish date"""""
        if 'tekno.kompas.com' in response.url:
            publish = response.xpath('html/body/div[1]/div[2]/div[5]/div[1]/div[2]/div/div[2]/div[2]/div[1]/div[1]/a[2]/text()').extract()
        elif 'entertainment.kompas.com' in response.url:
            publish = response.xpath('//html/body/div[2]/div/div/div[7]/div[4]/div[5]/div[1]/span[2]/text()').extract()
        elif 'otomotif.kompas.com' in response.url:
            publish = response.xpath('//*[@id="skrol"]/div[1]/div[4]/div[4]/div[1]/p/text()').extract()
        elif 'health.kompas.com' in response.url:
            publish = response.xpath('//html/body/div[3]/div[4]/div[4]/div[2]/div[1]/span/text()').extract()
        elif 'female.kompas.com' in response.url:
            publish = response.xpath('//*[@id="wrap-skin"]/div/div[2]/div/div[1]/div[8]/div[3]/div[4]/div[1]/span/text()').extract()
        elif 'properti.kompas.response' in response.url:
            publish = response.xpath('//html/body/div[1]/div[5]/div[3]/div[1]/div[4]/div[1]/span[2]/text()').extract()
        else:
            publish = response.xpath('//div[@class="grey small mb2"]/text()').extract()

        news['publish'] = helper.kompas_date(publish[0]) - timedelta(hours=7)

        """Getting Author"""
        if 'tekno.kompas.com' in response.url:
            author = response.xpath('//html/body/div[1]/div[2]/div[5]/div[1]/div[2]/div/div[2]/div[2]/div[1]/div[1]/a[1]/text()').extract()[0]
        elif 'entertainment.kompas.com' in response.url:
            author = response.xpath('//html/body/div[2]/div/div/div[7]/div[4]/div[11]/div[3]/text()').extract()[0]
        elif 'otomotif.kompas.com' in response.url:
            author = response.xpath('//*[@id="skrol"]/div[1]/div[4]/div[4]/div[2]/table/tbody/tr[1]/td[2]/text()').extract()[0]
        elif 'health.kompas.com' in response.url:
            author = response.xpath('//html/body/div[3]/div[4]/div[4]/div[2]/div[1]/span[1]/text()').extract()[0]
        elif 'female.kompas.com' in response.url:
            author = response.xpath('//*[@id="article_body"]/div[5]/text()').extract()[0]
        elif 'properti.kompas.response' in response.url:
            author = response.xpath('//html/body/div[1]/div[5]/div[3]/div[1]/div[4]/div[1]/span[1]/text()').extract()[0]
        elif 'travel.kompas.com' in response.url:
            author = response.xpath('//html/body/div[2]/div[5]/div/div[1]/div[2]/div[1]/h2/text()').extract()[0]
        elif 'internasional.kompas.com' in response.url:
            author = response.xpath('//html/body/div[1]/div[6]/div/div[1]/div[4]/div[3]/div[2]/div[2]/table/tbody/tr[1]/td[2]/text()').extract()[0]
        elif 'bisniskeuangan.kompas.com' in response.url:
            author = response.xpath('//html/body/div[2]/div[5]/div/div[1]/div[1]/div[3]/div[2]/div[2]/table/tbody/tr[1]/td[2]/text()').extract()[0]
        elif 'bola.kompas.com' in response.url:
            author = response.xpath('//html/body/div/div[6]/div/div[1]/div[1]/div[4]/div[2]/div[2]/table/tbody/tr[1]/td[2]').extract()[0]
        else:
            author = response.xpath('//html/body/div[1]/div[6]/div/div[1]/div[3]/div[3]/div[2]/div[2]/table/tbody/tr[1]/td[2]/text()').extract()[0]

        news['author'] = author

        """Getting location of news"""
        if 'tekno.kompas.com' in response.url:
            location = response.xpath('//html/body/div[1]/div[2]/div[5]/div[1]/div[2]/div/div[2]/div[2]/div[4]/strong/text()').extract()[0]
        elif 'entertainment.kompas.com' in response.url:
            location = response.xpath('//html/body/div[2]/div/div/div[7]/div[4]/div[9]/div[5]/strong/text()').extract()[0]
        elif 'otomotif.kompas.com' in response.url:
            location = response.xpath('//*[@id="skrol"]/div[1]/div[4]/div[4]/div[1]/p/strong[1]/text()').extract()[0]
        elif 'health.kompas.com' in response.url:
            location = ""
        elif 'female.kompas.com' in response.url:
            location = ""
        elif 'properti.kompas.response' in response.url:
            location = response.xpath('//html/body/div[1]/div[5]/div[3]/div[1]/div[8]/div[5]/strong/text()').extract()[0]
        else:
            location = news['content'][0:news['content'].find(',')]

        news['location'] = location


        """Getting Timestamp and Provider"""
        news['timestamp']= datetime.utcnow()
        news['provider'] = "kompas.com"
        yield news