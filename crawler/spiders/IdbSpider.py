import scrapy
from scrapy import log
from crawler.NewsItem import NewsItem
from scrapy.contrib.spiders import CrawlSpider,  Rule
from scrapy.spider import Spider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.exceptions import DropItem
from datetime import datetime,  timedelta
import helper


class IdbSpider(CrawlSpider):
    name = "idberitasatu"
    allowed_domains = [
        "id.beritasatu.com",
    ]

    start_urls = ["http://id.beritasatu.com/"]
    #start_urls = ["http://id.beritasatu.com/home/merck-akan-stock-split/112364"]

    rules = (
        Rule(SgmlLinkExtractor(
            allow=('\w{2}[a-zA-Z0-9](/)\d[0-9]{5}'),
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

        title = response.xpath("//*/span[contains(@class,'headline')]/text()").extract()[0]
        publish = response.xpath("//*/span[contains(@class,'caption')]/text()").extract()[0]
        publish = self.berita_date(publish)
        body = response.xpath("//*[contains(@id,'bodytext')]").extract()
        body = helper.item_merge(body)
        body = helper.clear_item(body)
        #body = helper.html_to_string(body)
        try:
            location = body.split("-",1)[0]
        except Exception, e:
            location = None
        try:
            author = body.rsplit(".",1)[1]
        except Exception, e:
            author = None
        news['title'] = title
        news['author'] = author
        news['publish'] = publish
        news['timestamp'] = datetime.utcnow()
        news['provider'] = self.name
        news['content'] = body
        news['location'] = location
        yield news

    def berita_date(self, plain_string):
        if plain_string is None:
            return None

        plain_string = plain_string.split(", ")[1].split("| ")

        string_date = plain_string[0]
        string_time = plain_string[1]
        date = string_date.split(" ")
        day = int(date[0])
        month = helper.get_month(date[1])
        year = date[2]
        hour = string_time.split(":")[0]
        minute = string_time.split(":")[1]
        #self.log(year+" "+month+" "+day+" "+hour+" "+minute)
        return helper.formatted_date(str(year),str(month),str(day),str(hour),str(minute))