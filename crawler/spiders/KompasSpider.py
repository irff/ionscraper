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
<<<<<<< HEAD

class KompasSpider(CrawlSpider):
=======
class KompasSpider(Spider):
>>>>>>> spider_kompas
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
<<<<<<< HEAD
        "foto.kompas.com",
        "video.kompas.com",
        ]

    start_urls = ["http://kompas.com"]
=======
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
>>>>>>> spider_kompas

    rules = (
        # Extract links matching 'read' and parse them with the spider's method parse_item
        # Rule(SgmlLinkExtractor(allow=('', )), follow=True),
        Rule(SgmlLinkExtractor(allow=('indeks','p=',), deny=('sso','login.kompas.com','utm_source=wp')),follow=True),
        Rule(SgmlLinkExtractor(allow=('read/', 'read/xml/','detail/'), deny=('/sso/','login.kompas.com','utm_source=wp')),follow=True, callback='parse_item'),
    )

    """
    if use Spider, change function to 'parse'
    if use CrawlSpider, change function to 'parse_item'
    """
<<<<<<< HEAD
    def parse_item(self, response):
        log.msg("Get: %s" % response.url, level=log.DEBUG)
=======
    def parse(self, response):
        self.log('Hi, this is an item page! %s' % response.url)
>>>>>>> spider_kompas
        news = NewsItem()
        news['url'] = response.url
        """Getting Timestamp and Provider"""
        news['timestamp']= datetime.utcnow()
        news['provider'] = "kompas.com"

        if "/login/" in response.url or "utm_source=wp" in response.url or "/sso/" in response.url:
            raise DropItem("URL not allowed")

<<<<<<< HEAD
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
        elif "entertainment.kompas.com" in response.url:
            yield self.parse_item_entertainment(response, news)
        elif "otomotif.kompas.com" in response.url:
            yield self.parse_item_otomotif(response, news)
        elif "health.kompas.com" in response.url:
            yield self.parse_item_health(response, news)
        elif "female.kompas.com" in response.url:
            yield  self.parse_item_female(response, news)
        elif "properti.kompas.com" in response.url:
            yield self.parse_item_properti(response, news)
        elif "travel.kompas.com" in response.url:
            yield self.parse_item_travel(response, news)
        elif "foto.kompas.com" in response.url:
            yield self.parse_item_foto(response, news)
        elif "video.kompas.com" in response.url:
            yield self.parse_item_video(response, news)
        else:
            yield self.parse_item_universal(response, news)

    def parse_item_default(self, response, news):
        news['title'] = helper.html_to_string(response.xpath("//h2").extract()[0])
        news['content'] = helper.html_to_string(response.xpath("//span[@class='kcmread1114']").extract()[0])

        author = response.xpath("//html/body/div[1]/div[6]/div/div[1]/div[3]/div[3]/div[2]/div[2]/table/tbody/tr[1]/td[2]/text()").extract();
        if len(author) > 0:
            news['author'] = author[0]
        else:
            news['author'] = " "

        date = response.xpath("//div[@class='grey small mb2']/text()").extract()
        if len(date) > 0:
            news['publish'] = self.kompas_date(date[0])
        else:
            news['publish'] = self.kompas_date_from_url(response.url)

        location = response.xpath("//span[@class='kcmread1114']/strong[1]/text()").extract()
        if len(location) > 0:
            news['location'] = location[0][0:location[0].find(',')]
        else:
            if "KOMPAS.com" in news['content']:
                news['location'] = news['content'][0:news['content'].find(',')]
            else:
                news['location'] = " "

        news['content'] = helper.clear_item(news['content'])
        return news


    def parse_item_tekno(self, response, news):
        news['title'] = helper.html_to_string(response.xpath("//h1/text()").extract()[0])
        news['content'] = helper.html_to_string(response.xpath("//div[@class='isi_artikel']").extract()[0])

        author = response.xpath("//div[@class='editor_artikel_status_artikel']/a[1]/text()").extract();
        if len(author) > 0:
            news['author'] = author[0]
        else:
            news['author'] = " "

        date = response.xpath("//div[@class='editor_artikel left']/a[2]/text()").extract()
        time = response.xpath("//div[@class='editor_artikel left']/a[3]/text()").extract()
        if len(date) > 0 and len(time) > 0:
            date_time = date[0] + " |" +time[0]
            news['publish'] = self.kompas_date(date_time)
            # news['publish'] = date_time
        else:
            news['publish'] = self.kompas_date_from_url(response.url)

        # tekno.kompas.com not have location
        news['location'] = " "

        news['content'] = helper.clear_item(news['content'])
        return news

    def parse_item_entertainment(self, response, news):
        news['title'] = helper.html_to_string(response.xpath("//span[@class='judul judul_artikel2011']/text()").extract()[0])
        news['content'] = helper.html_to_string(response.xpath("//div[@class='isi_berita pt_5']").extract()[0])

        author = response.xpath("//span[@class='c_abu01_kompas2011'][1]/text()").extract();
        if len(author) > 0 and "WIB" not in author[0]:
            news['author'] = author[0]
        else:
            author_down = response.xpath("]//span[@class='c_abu01_kompas2011'][2]/text()").extract();
            if len(author_down) > 0:
                news['author'] = author_down[0]
            else:
                news['author'] = " "

        date = response.xpath("//span[@class='c_abu01_kompas2011'][1]/text()").extract()
        if len(date) > 0 and "WIB" in date[0]:
            news['publish'] = self.kompas_date(date[0])
        else:
            date_down = response.xpath("//span[@class='c_abu01_kompas2011'][2]/text()").extract();
            if len(date_down) > 0:
                news['publish'] = self.kompas_date(date_down[0])
            else:
                news['publish'] = self.kompas_date_from_url(response.url)

        location = response.xpath("//div[@class='isi_berita pt_5']/strong/text()").extract()
        if len(location) > 0:
            news['location'] = location[0][0:location[0].find(',')]
        else:
            if "KOMPAS.com" in news['content']:
                news['location'] = news['content'][0:news['content'].find(',')]
            else:
                news['location'] = " "

        news['content'] = helper.clear_item(news['content'])
        return news

    def parse_item_otomotif(self, response, news):
        news['title'] = helper.html_to_string(response.xpath("//div[@class='baca-content']/h1").extract()[0])
        news['content'] = helper.html_to_string(response.xpath("//div[@class='div-read']").extract()[0])

        author = response.xpath("//div[@class='penulis-editor']/table/tbody/tr[2]/td[2]/text()").extract();
        if len(author) > 0 and "WIB" not in author[0]:
            news['author'] = author[0]
        else:
            news['author'] = " "

        date = response.xpath("//div[@class='grey small mb2']/text()").extract()
        if len(date) > 0:
            news['publish'] = self.kompas_date(date[0])
        else:
            news['publish'] = self.kompas_date_from_url(response.url)

        location = response.xpath("//div[@class='div-read']/strong/text()").extract()
        if len(location) > 0:
            news['location'] = location[0][0:location[0].find(',')]
        else:
            if "KOMPAS.com" in news['content']:
                news['location'] = news['content'][0:news['content'].find(',')]
            else:
                news['location'] = " "
        news['content'] = helper.clear_item(news['content'])
        return news

    def parse_item_health(self, response, news):
        news['title'] = helper.html_to_string(response.xpath("//div[@class='isi_artikel']/h1").extract()[0])
        news['content'] = helper.html_to_string(response.xpath("//div[@class='isi_berita pt_5']").extract()[0])

        author = response.xpath("//div[@class='left']/div[1]/span[1]/text()").extract();
        if len(author) > 0 and "WIB" not in author[0]:
            news['author'] = author[0]
        else:
            author_down = response.xpath("//div[@class='left']/div[2]/span[1]/text()").extract();
            if len(author_down) > 0:
                news['author'] = author_down[0]
            else:
                news['author'] = " "

        date = response.xpath("//div[@class='left']/div[1]/span[1]/text()").extract()
        if len(date) > 0 and "WIB" in date[0]:
            news['publish'] = self.kompas_date(date[0])
        else:
            date_down = response.xpath("//div[@class='left']/div[1]/span[2]/text()").extract();
            if len(date_down) > 0:
                news['publish'] = self.kompas_date(date_down[0])
            else:
                news['publish'] = self.kompas_date_from_url(response.url)

        location = response.xpath("//div[@class='isi_berita pt_5']/p/strong/text()").extract()
        if len(location) > 0:
            news['location'] = location[0][0:location[0].find(',')]
        else:
            if "KOMPAS.com" in news['content']:
                news['location'] = news['content'][0:news['content'].find(',')]
            else:
                news['location'] = " "
        news['content'] = helper.clear_item(news['content'])
        return news

    def parse_item_female(self, response, news):
        news['title'] = helper.html_to_string(response.xpath("//div[@class='pt_20']/div[2]").extract()[0])
        news['content'] = response.xpath("//div[@id='article_body']/p/text()").extract()[0]

        author = response.xpath("//*[@id='article_body']/div[8]/text()").extract();
        if len(author) > 0 and "WIB" not in author[0]:
            news['author'] = author[0]
        else:
            news['author'] = " "

        date = response.xpath("//*[@id='wrap-skin']/div/div[2]/div/div[1]/div[8]/div[3]/div[4]/div[1]/span").extract()
        if len(date) > 0:
            news['publish'] = self.kompas_date(date[0])
        else:
            news['publish'] = self.kompas_date_from_url(response.url)

        # female.kompas.com not have location
        news['location'] = " "

        news['content'] = helper.clear_item(news['content'])
        return news

    def parse_item_properti(self, response, news):
        news['title'] = helper.html_to_string(response.xpath("//div[@class='judul_artikel2011 pb_10 pt_10']").extract()[0])
        news['content'] = helper.html_to_string(response.xpath("//div[@class='isi_berita pt_5']").extract()[0])

        author = response.xpath("//div[@class='left arial']/div/span[1]/text()").extract();
        if len(author) > 0 and "WIB" not in author[0]:
            news['author'] = author[0]
        else:
            news['author'] = " "

        date = response.xpath("//div[@class='left arial']/div/span[2]/text()").extract()
        if len(date) > 0:
            news['publish'] = self.kompas_date(date[0])
        else:
            news['publish'] = self.kompas_date_from_url(response.url)

        location = response.xpath("//div[@class='isi_berita pt_5']/strong/text()").extract()
        if len(location) > 0:
            news['location'] = location[0][0:location[0].find(',')]
        else:
            if "KOMPAS.com" in news['content']:
                news['location'] = news['content'][0:news['content'].find(',')]
            else:
                news['location'] = " "

        news['content'] = helper.clear_item(news['content'])
        return news

    def parse_item_travel(self, response, news):
        news['title'] = helper.html_to_string(response.xpath("//h2").extract()[0])
        news['content'] = helper.html_to_string(response.xpath("//div[@class='kcm-read-content-text']/div[2]").extract()[0])

        author = response.xpath("html/body/div[2]/div[5]/div/div[1]/div[2]/div[3]/div[2]/div[5]/table/tbody/tr[1]/td[2]/text()").extract();
        if len(author) > 0:
            news['author'] = author[0]
        else:
            news['author'] = " "

        author = response.xpath("html/body/div[2]/div[5]/div/div[1]/div[2]/div[3]/div[2]/div[5]/table/tbody/tr[1]/td[2]/text()").extract();
        if len(author) > 0 and "WIB" not in author[0]:
            news['author'] = author[0]
        else:
            news['author'] = " "

        date = response.xpath("//div[@class='left arial']/div/span[2]/text()").extract()
        if len(date) > 0:
            news['publish'] = self.kompas_date(date[0])
        else:
            news['publish'] = self.kompas_date_from_url(response.url)

        location = response.xpath("//div[@class='kcm-read-content-text']/div[2]/p/strong/text()").extract()
        if len(location) > 0:
            news['location'] = location[0][0:location[0].find(',')]
        else:
            if "KOMPAS.com" in news['content']:
                news['location'] = news['content'][0:news['content'].find(',')]
            else:
                news['location'] = " "
        news['content'] = helper.clear_item(news['content'])
        return news

    def parse_item_foto(self, response, news):
        news['title'] = helper.html_to_string(response.xpath("//div[@class='title_artikel']/h1").extract()[0])
        news['content'] = helper.html_to_string(response.xpath("//div[@class='artikel']/div[@class='isi_artikel']").extract()[0])

        author = response.xpath("//div[@class='artikel']/div[@class='editor_artikel_status_artikel']/div/a[1]/text()").extract();
        if len(author) > 0:
            news['author'] = author[0]
        else:
            news['author'] = " "

        news['publish'] = self.kompas_date_from_url(response.url)

        location = response.xpath("//div[@class='isi_artikel']/p/span/strong/text()").extract()
        if len(location) > 0:
            news['location'] = location[0][0:location[0].find(',')]
        else:
            if "KOMPAS.com" in news['content']:
                news['location'] = news['content'][0:news['content'].find(',')]
            else:
                news['location'] = " "
        news['content'] = helper.clear_item(news['content'])
        return news

    def parse_item_video(self, response, news):
        news['title'] = helper.html_to_string(response.xpath("//h1").extract()[0])
        news['content'] = helper.html_to_string(response.xpath("//p").extract()[0])

        # video.kompas.com not have author
        news['author'] = " "

        news['publish'] = self.kompas_date_from_url(response.url)

        # video.kompas.com not have location
        news['location'] = " "
        news['content'] = helper.clear_item(news['content'])
        return news

    def parse_item_universal(self, response, news):
        news['title'] = helper.html_to_string(response.xpath("//head/title").extract()[0])
        news['content'] = helper.html_to_string(response.xpath("//p").extract()[0])
        news['content'] = helper.clear_item(news['content'])
        news['author'] = " "
        news['publish'] = self.kompas_date_from_url(response.url)
        news['location'] = " "
        return news

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

        return helper.formatted_date(year,month,day,hour,minute) - timedelta(hours=-7)

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

        return helper.formatted_date(year,month,day,hour,minute) - timedelta(hours=-7)

    def kompas_date_from_url(self, url):
        if url == None:
            return None

        u = url.split("/")

        if "foto.kompas.com" in url:
            return helper.formatted_date(u[5], u[6], u[7], "00", "00") - timedelta(hours=-7)

        return helper.formatted_date(u[4], u[5], u[6], "00", "00") - timedelta(hours=-7)
=======

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
>>>>>>> spider_kompas
