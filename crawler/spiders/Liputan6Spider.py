import scrapy
from scrapy import log
from crawler.NewsItem import NewsItem
from scrapy.contrib.spiders import CrawlSpider,  Rule
from scrapy.spider import Spider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.exceptions import DropItem
from datetime import datetime,  timedelta
import helper


class Liputan6Spider(CrawlSpider):
    name = "liputan6"
    allowed_domains = [
        "liputan6.com",
    ]

    start_urls = ["http://bola.liputan6.com/read/2206687/gaji-ditunggak-pemain-ini-pinjam-uang-ke-orang-tua"]

    rules = (
        Rule(SgmlLinkExtractor(
            allow=('read','\w{2}[a-zA-Z0-9](/)\d[0-9]{5}'),
            deny=('facebook.com','twitter.com')),follow=True, callback='parse_item'),
        Rule(SgmlLinkExtractor(
            allow=('indeks','\w{2}[a-zA-Z0-9](/)\w[a-zA-Z0-9]{2}'),
            deny=('m.liputan6.com','twitter.com')),follow=True),
    )

    """
    if use Spider,  change function to 'parse'
    if use CrawlSpider,  change function to 'parse_item'
    """
    def parse_item(self,  response):
        self.log('Hi,  this is an item page! %s' % response.url)
        news = NewsItem()
        news['url'] = response.url

        if 'login' in response.url or 'utm_source=wp' in response.url or 'sso' in response.url or 'reg' in response.url:
                raise DropItem("URL not allowed")

        title = response.xpath("//h1/text()").extract()[0]
        date = date = response.css(".updated::attr(datetime)").extract()
        if len(date) > 0:
            date = self.liputan6_date(date[0])
        else:
            date = news['timestamp']

        body = response.xpath("//*[contains(@class,'text-detail')]/p").extract()
        body = helper.item_merge(body)
        body = helper.clear_item(body)
        body = helper.html_to_string(body)
        tmp = response.xpath("//*[contains(@class,'body-berita')]/p/strong/text()").extract()
        location = response.xpath("//*[contains(@class,'text-detail')]/p/b/text()").extract()
        author = response.xpath("//*[contains(@itemprop,'author')]/text()").extract()

        news['title'] = title
        news['author'] = author
        news['publish'] = date
        news['timestamp'] = datetime.utcnow()
        news['provider'] = self.name
        news['content'] = body
        news['location'] = location[0].split(",")[1].replace("-","").strip()
        yield news

    def liputan6_date(self, plain_string):
        dt = plain_string.split(" ")


        date = dt[0].split("-")
        year = date[0]
        month = date[1]
        day = date[2]

        time = dt[1].split(":")
        hour = time[0]
        minute = time[1]
        return helper.formatted_date(year,month,day,hour,minute) + timedelta(hours=-7)

