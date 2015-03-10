# -*- coding: utf-8 -*-

# Scrapy settings for crawler project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'crawler'

SPIDER_MODULES = ['crawler.spiders']
NEWSPIDER_MODULE = 'crawler.spiders'

ITEM_PIPELINES = [
  'scrapyelasticsearch.scrapyelasticsearch.ElasticSearchPipeline',
]

ELASTICSEARCH_SERVER = 'localhost' 
ELASTICSEARCH_PORT = 9200 
ELASTICSEARCH_INDEX = 'news'
ELASTICSEARCH_TYPE = 'kompas'
ELASTICSEARCH_UNIQ_KEY = 'url'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'crawler (+http://www.yourdomain.com)'

#DESABLE REDIRECT
REDIRECT_ENABLED = False