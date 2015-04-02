import scrapy
from scrapy import log
from crawler.NewsItem import NewsItem
from scrapy.contrib.spiders import CrawlSpider,  Rule
from scrapy.spider import Spider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.exceptions import DropItem
from datetime import datetime,  timedelta
import helper


class JawaposSpider(CrawlSpider):
    name = "jawapos"
    allowed_domains = [
        "www.jawapos.com",
    ]

    start_urls = ["http://www.jawapos.com"]

    rules = (
        Rule(SgmlLinkExtractor(
            allow=('baca','\w{2}[a-zA-Z0-9](/)\d[0-9]{5}'),
            deny=('facebook.com','twitter.com')),follow=True, callback='parse_item'),
        Rule(SgmlLinkExtractor(
            allow=('indeks','\w{2}[a-zA-Z0-9](/)\w[a-zA-Z0-9]{2}'),
            deny=('facebook.com','twitter.com')),follow=True),
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

        title = response.xpath("//*/h1[contains(@class, 'judul-headline')]/text()").extract()[0]
        publish = response.xpath("//*[contains(@class, 'tanggal')]/text()").extract()[0]
        publish = self.jawapos_date(publish)
        body = response.xpath("//*[contains(@class,'body-berita')]/p").extract()
        body = helper.item_merge(body)
        body = helper.clear_item(body)
        body = helper.html_to_string(body)
        tmp = response.xpath("//*[contains(@class,'body-berita')]/p/strong/text()").extract()
        location = tmp[0]
        author = tmp[1]

        news['title'] = title
        news['author'] = author
        news['publish'] = publish
        news['timestamp'] = datetime.utcnow()
        news['provider'] = self.name
        news['content'] = body
        news['location'] = location
        yield news

    def jawapos_date(self, plain_string):
        if plain_string is None:
            return None

        plain_string = helper.html_to_string(plain_string).split(", ")

        string_date = plain_string[0]
        string_time = plain_string[1].split(" ")[0]
        date = string_date.split("/")
        day = int(date[0])
        month = int(date[1])
        year = date[2]
        if len(year) < 4:
            year = "20"+str(year)
        hour = string_time.split(":")[0]
        minute = string_time.split(":")[1]
        #self.log(year+" "+month+" "+day+" "+hour+" "+minute)
        return helper.formatted_date(str(year),str(month),str(day),str(hour),str(minute))