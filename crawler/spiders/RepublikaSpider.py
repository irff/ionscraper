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


class RepublikaSpider(CrawlSpider):
    name = "republika"
    allowed_domains = [
        "republika.co.id",
        "blog.republika.co.id",
        "nasional.republika.co.id",
        "bola.republika.co.id",
        "gayahidup.republika.co.id",
    ]
    start_urls = ["http://republika.co.id"]

    rules = (
        Rule(SgmlLinkExtractor(
            allow=('indeks'),
            deny=('reg', 'sso', 'login', 'utm_source=wp')),
            follow=True),
        Rule(SgmlLinkExtractor(
            allow=('berita/'),
            deny=('reg', 'sso', 'login', 'utm_source=wp')),
            follow=True,
            callback='parse_item'),
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

        title = helper.html_to_string(
            response.xpath("//*[@class='jdl-detail']").extract()[0])
        content = helper.html_to_string(helper.item_merge(
            response.xpath("//*[@class='txt-detailberita']/p").extract()))
        publish = self.republika_date(helper.html_to_string(
            response.xpath("//*[@class='date']").extract()[0]))
        location = helper.clear_item(content.split('--', 1)[0].split(',')[1])
        author = helper.clear_item(helper.html_to_string(response.xpath("//*[@class='red']").extract()[-1]))
        author = author.split("Redaktur")[-1].split("Sumber")[0][4:]
        content = helper.clear_item(content.split('--', 1)[1].rsplit('.', 1)[0])

        news['title'] = title
        news['content'] = content
        news['publish'] = publish
        news['author'] = author
        news['location'] = location
        news['timestamp'] = datetime.utcnow()
        news['provider'] = "tempo.co"
        yield news

    def republika_date(self, plain_string):
        if plain_string is None:
            return None

        plain_string = helper.html_to_string(plain_string)

        string_date = plain_string.split(", ")[1]
        string_time = plain_string.split(", ")[2].split(" ")[0]
        date = string_date.split(" ")
        day = date[0]
        month = helper.get_month(date[1])
        year = date[2]
        hour = string_time.split(":")[0]
        minute = string_time.split(":")[1]
        return helper.formatted_date(str(year),str(month),str(day),str(hour),str(minute))