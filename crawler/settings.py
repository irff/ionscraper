# -*- coding: utf-8 -*-

# Scrapy settings for crawler project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#
import logging

BOT_NAME = 'crawler'

SPIDER_MODULES = ['crawler.spiders']
NEWSPIDER_MODULE = 'crawler.spiders'


SPIDER_MIDDLEWARES = {
    'scrapylib.deltafetch.DeltaFetch': 100,
}
DELTAFETCH_ENABLED = True

ITEM_PIPELINES = [
  'scrapyelasticsearch.scrapyelasticsearch.ElasticSearchPipeline',
]
ELASTICSEARCH_SERVER = 'http://52.25.206.143'
ELASTICSEARCH_PORT = 9200
ELASTICSEARCH_INDEX = 'langgar'
ELASTICSEARCH_TYPE = 'news'
ELASTICSEARCH_UNIQ_KEY = 'title'
ELASTICSEARCH_LOG_LEVEL = logging.DEBUG

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'crawler (+http://www.yourdomain.com)'

#DESABLE REDIRECT
#REDIRECT_ENABLED = False

#DELAY DOWNLOAD
DOWNLOAD_DELAY = 0.05

# LOG_LEVEL='INFO'

