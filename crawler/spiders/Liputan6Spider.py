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

        title = response.xpath("//*[contains(@class, 'entry-title')]/text()").extract()[0]
        publish = response.xpath("//*[contains(@itemprop, 'datePublished')]/text()").extract()[0].replace("at","")
        publish = publish + response.xpath("//*[contains(@itemprop, 'datePublished')]/span/text()").extract()[0].split(" ")[0]
        publish = self.liputan6_date(publish)
        body = response.xpath("//*[contains(@class,'text-detail')]/p").extract()
        body = helper.item_merge(body)
        body = helper.clear_item(body)
        body = helper.html_to_string(body)
        tmp = response.xpath("//*[contains(@class,'body-berita')]/p/strong/text()").extract()
        location = response.xpath("//*[contains(@class,'text-detail')]/p/b/text()").extract()
        author = response.xpath("//*[contains(@itemprop,'author')]/text()").extract()

        news['title'] = title
        news['author'] = author
        news['publish'] = publish
        news['timestamp'] = datetime.utcnow()
        news['provider'] = self.name
        news['content'] = body
        news['location'] = location[0].split(",")[1].replace("-","").strip()
        yield news

    def liputan6_date(self, plain_string):
        if plain_string is None:
            return None

        plain_string = helper.html_to_string(plain_string).split(" ")
        #self.log(plain_string)  
        # string_date = plain_string[0]
        # string_time = plain_string[1].split(" ")[0]
        date = plain_string
        day = date[0]
        month = helper.get_month(date[1])
        year = date[2]
        hour = date[3].split(":")[0]
        minute = date[3].split(":")[1]
        #self.log(year+" "+month+" "+day+" "+hour+" "+minute)
        return helper.formatted_date(str(year),str(month),str(day),str(hour),str(minute))