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

    start_urls = ["http://tekno.kompas.com/read/2015/03/22/08090057/Kinerja.Ponsel.Oppo.Tertipis.Apakah.Kencang."]

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
        """Getting Timestamp and Provider"""
        news['timestamp']= datetime.utcnow()
        news['provider'] = "kompas.com"

        if "login" in response.url or "utm_source=wp" in response.url or "sso" in response.url:
            raise DropItem("URL not allowed")

        if "nasional.kompas.com" in response.url:
            yield self.parse_item_default(response, news)
        elif "regional.kompas.com" in response.url:
            yield self.parse_item_default(response, news)
        elif "megapolitan.kompas.com" in response.url:
            yield self.parse_item_default(response, news)
        elif "internasional.kompas.com" in response.url:
            yield self.parse_item_default(response, news)
        elif "olahraga.kompas.com" in response.url:
            yield self.parse_item_default(response, news)
        elif "sains.kompas.com" in response.url:
            yield self.parse_item_default(response, news)
        elif "edukasi.kompas.com" in response.url:
            yield self.parse_item_default(response, news)
        elif "bisniskeuangan.kompas.com" in response.url:
            yield self.parse_item_default(response, news)
        elif "bola.kompas.com" in response.url:
            yield self.parse_item_default(response, news)
        elif "tekno.kompas.com" in response.url:
            yield self.parse_item_tekno(response, news)


    def parse_item_default(self, response, news):
        news['title'] = helper.html_to_string(response.xpath("//h2").extract()[0])
        news['content'] = helper.html_to_string(response.xpath("//span[@class='kcmread1114']").extract()[0])

        author = response.xpath("//html/body/div[1]/div[6]/div/div[1]/div[3]/div[3]/div[2]/div[2]/table/tbody/tr[1]/td[2]/text()").extract();
        if len(author) > 0:
            news['author'] = author
        else:
            news['author'] = " "

        date = response.xpath('//div[@class="grey small mb2"]/text()').extract()
        if len(date) > 0:
            news['publish'] = self.kompas_date(date[0])
        else:
            raise DropItem("Publish date not found")

        location = response.xpath("//span[@class='kcmread1114']/strong[1]/text()").extract()
        if len(location) > 0:
            news['location'] = location[0][0:location[0].find(',')]
        else:
            if "KOMPAS.com" in news['content']:
                news['location'] = news['content'][0:news['content'].find(',')]
            else:
                news['location'] = " "
        return news


    def parse_item_tekno(self, response, news):
        news['title'] = helper.html_to_string(response.xpath("//h1/text()").extract()[0])
        news['content'] = helper.html_to_string(response.xpath("//div[@class='isi_artikel']").extract()[0])

        author = response.xpath("//div[@class='editor_artikel_status_artikel']/a[1]/text()").extract();
        if len(author) > 0:
            news['author'] = author
        else:
            news['author'] = " "

        date = response.xpath("//div[@class='editor_artikel left']/a[2]/text()").extract()
        time = response.xpath("//div[@class='editor_artikel left']/a[3]/text()").extract()
        if len(date) > 0 and len(time) > 0:
            date_time = date[0] + " |" +time[0]
            news['publish'] = self.kompas_date(date_time)
            # news['publish'] = date_time
        else:
            raise DropItem("Publish date not found")

        # tekno.kompas.com not have location
        news['location'] = " "

        return news

    def parse_item_entertainment(self, response, news):
        yield news

    def parse_item_otomotif(self, response, news):
        yield news

    def parse_item_health(self, response, news):
        yield news

    def parse_item_female(self, response, news):
        yield news

    def parse_item_properti(self, response, news):
        yield news

    def kompas_date(self, plain_string):
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

    def kompas_date_tekno(self, string_date, string_time):
        if string_date == None or string_time == None:
            return None

        date = string_date.split(" ")
        day = date[0]
        year = date[2]
        ms = date[1]
        month = helper.get_month(ms)
        hour = string_time[0:2]
        minute = string_time[3:5]

        return helper.formatted_date(year,month,day,hour,minute)