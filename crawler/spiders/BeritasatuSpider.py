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


class BeritasatuSpider(CrawlSpider):
    name = "beritasatu"
    allowed_domains = [
        "beritasatu.com",
    ]
    start_urls = ["http://www.beritasatu.com/ekonomi/260085-sofyan-djalil-indonesia-harus-segera-miliki-kereta-cepat.html"]

    rules = (
        Rule(SgmlLinkExtractor(
            allow=('indeks'),
            deny=('reg', 'sso', 'login', 'utm_source=wp')),
            follow=True),
    )

    """
    if use Spider,  change function to 'parse'
    if use CrawlSpider,  change function to 'parse_item'
    """
    def parse(self,  response):
        self.log('Hi,  this is an item page! %s' % response.url)
        news = NewsItem()
        news['url'] = response.url

        if 'login' in response.url or 'utm_source=wp' in response.url or 'sso' in response.url or 'reg' in response.url:
                raise DropItem("URL not allowed")

        #title = helper.html_to_string(
        #    response.xpath("//*[@class='mtb10']").extract()[1])
        #content = helper.html_to_string(helper.item_merge(
        #    response.xpath("//*[@class='txt-detailberita']/p").extract()))
        # publish = self.berita_date(helper.html_to_string(
        #     response.xpath("//*[@class='date']").extract()[0]))
        # location = helper.clear_item(content.split('--', 1)[0].split(',')[1])
        # author = helper.clear_item(helper.html_to_string(response.xpath("//*[@class='red']").extract()[-1]))
        # author = author.split("Redaktur")[-1].split("Sumber")[0][4:]
        # content = helper.clear_item(content.split('--', 1)[1].rsplit('.', 1)[0])

        # news['title'] = title
        #news['content'] = helper.clear_item(response.xpath("//body/text()").extract())
        body = response.xpath("//body").extract()[0]
        
        body = helper.clear_item(body)
        body = helper.html_to_string(body)


        self.log(">>>>> "+ str(body))
        # news['publish'] = publish
        # news['author'] = author
        # news['location'] = location
        # news['timestamp'] = datetime.utcnow()
        news['provider'] = "tempo.co"
        yield news

    def berita_date(self, plain_string):
        if plain_string is None:
            return None

        plain_string = helper.html_to_string(plain_string)

        string_date = plain_string.split(", ")[1]
        string_time = plain_string.split("| ")[1]
        date = string_date.split(" ")
        day = date[0]
        month = helper.get_month(date[1])
        year = date[2]
        hour = string_time.split(":")[0]
        minute = string_time.split(":")[1]
        return helper.formatted_date(str(year),str(month),str(day),str(hour),str(minute))