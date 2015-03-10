import scrapy
from crawler.NewsItem import NewsItem
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.exceptions import DropItem
import datetime
import lxml.etree
import lxml.html

class NewsSpider(CrawlSpider):
    name = "news"
    allowed_domains = [
    "nasional.kompas.com",
    "regional.kompas.com",
    "megapolitan.kompas.com",
    "internasional.kompas.com",
    "olahraga.kompas.com",
    "sains.kompas.com",
    "edukasi.kompas.com",
    "bisniskeuangan.kompas.com",
    ]
    start_urls = ["http://kompas.com"]
    rules = (
        # Extract links matching 'read' and parse them with the spider's method parse_item
		# Rule(SgmlLinkExtractor(allow=('', )), follow=True),
        Rule(SgmlLinkExtractor(allow=('/index/', ), deny=('/reg/','/sso/','/login/'))),
        Rule(SgmlLinkExtractor(allow=('/read/', )),follow=True, callback='parse_item'),

    )

    def parse_item(self, response):
        self.log('Hi, this is an item page! %s' % response.url)
        news = NewsItem()
        news['url'] = response.url
		
        if 'login' in response.url:
		    raise DropItem("URL not allowed")
			
        news['title'] = response.xpath('//h2/text()').extract()
        content = lxml.html.fromstring(response.xpath('//span[@class="kcmread1114"]').extract()[0])
        news['content'] = lxml.html.tostring(content, method="text", encoding=unicode)
        publish = lxml.html.fromstring(response.xpath('//div[@class="grey small mb2"]/text()').extract()[0])
        news['publish'] = lxml.html.tostring(publish, method="text", encoding=unicode)
        news['timestamp']= datetime.datetime.utcnow()
        yield news