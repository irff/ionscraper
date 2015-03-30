import scrapy
from scrapy import log
from crawler.NewsItem import NewsItem
from scrapy.contrib.spiders import CrawlSpider,  Rule
from scrapy.spider import Spider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.exceptions import DropItem
from datetime import datetime,  timedelta
import helper

"""
If you want to debug for a page,
    Change RepublikaSpider Class extends 'Spider' class
    Change start_urls with a url that you want to debug
    Change 'parse_item' method to 'parse'
If you want to crawl and follow all links ,
    Change RepublikaSpider Class extends 'CrawlSpider' class
    Change start_urls with 'http://republika.co.id'
    Change 'parse' method to 'parse_item'
"""


class KontanSpider(CrawlSpider):
    name = "kontan"
    allowed_domains = [
        "kontan.co.id",
    ]
    start_urls = ["http://kontan.co.id"]

    rules = (
        Rule(SgmlLinkExtractor(
            allow=('news'),
            deny=('reg', 'sso', 'login', 'utm_source=wp')),
            follow=True),
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

        title = response.xpath("//*/h1[contains(@class, 'cleanprint-title')]/text()").extract()[0]
        author = response.xpath("//*/*[contains(@class, 'cleanprint-byline')]/text()").extract()[0].strip()
        author = author.split("Oleh")[1].replace("-","").strip()
        publish = response.xpath("//*/*[contains(@class, 'cleanprint-dateline')]/text()").extract()[0]
        #author = tmp.split("-")[0].split("Oleh")[1]
        body = response.xpath("//*[contains(@class,'content_news')]").extract()
        body = helper.item_merge(body)
        body = helper.clear_item(body).strip().split("Editor:",1)[0]
        location = body.split(".",1)[0]
        body = body.split(".",1)[1]

        news['title'] = title
        news['author'] = helper.clear_item(author)
        news['publish'] = self.kontan_date(helper.clear_item(publish))
        news['timestamp'] = datetime.utcnow()
        news['provider'] = "kontan"
        news['content'] = body
        news['location'] = location
        yield news


    def kontan_date(self, plain_string):
        if plain_string is None:
            return None
        plain_string = plain_string.split(", ")[1]
        string_date = plain_string.split(" | ")[0]
        string_time = plain_string.split(" | ")[1]
        date = string_date.split(" ")
        day = date[0]
        month = helper.get_month(date[1])
        year = date[2]
        hour = string_time[0:2]
        minute = string_time[3:5]
        return helper.formatted_date(year,month,day,hour,minute)