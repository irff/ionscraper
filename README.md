# ionscraper
Online Media Scraper

## Online Media List
List of media

### Indonesian Media
- X http://www.antaranews.com/
- X http://www.bbc.co.uk/indonesia
- X http://www.beritasatu.com/
- X http://www.bijaks.net/
- X http://www.bisnis.com/
- X http://www.cnnindonesia.com/
- http://www.detik.com/
- X http://www.inilah.com/
- http://id.beritasatu.com/home/
- http://thejakartaglobe.beritasatu.com/
- X http://www.jawapos.com/
- X http://www.kompas.com/
- X http://kontan.co.id/
- X http://www.liputan6.com/
- X http://mediaindonesia.com/
- X http://www.merdeka.com/
- http://www.metrotvnews.com/
- X http://okezone.com/
- X http://www.pikiran-rakyat.com/
- X http://www.rmol.co/
- X http://www.republika.co.id/
- X http://www.suara.com/
- X http://swa.co.id/
- X http://www.tempo.co/
- http://www.viva.co.id/

### English Media
- http://www.thejakartapost.com/
- http://edition.cnn.com/
- http://www.bbc.co.uk/
- http://www.nytimes.com/
- http://www.huffingtonpost.com/
- http://www.reuters.com/
- http://www.aljazeera.com/
- http://www.washingtonpost.com/
- http://time.com/
- http://news.nationalgeographic.com/
- http://www.smh.com.au/

## Metadata

Here's the required metadata for each article:

- title
- date_published
- content
- url
- author (if any)
- editor (if any)

## Instruction
For testing a single page
Go to spiders directory
`$ cd crawler/spiders`

List all avaliable spiders

```bash
$ ls | grep "Spider.py$"
KompasSpider.py
RepublikaSpider.py
TempoSpider.py
```

Run `scrapy crawl [spider_name]`

```bash
$ scrapy crawl republika
2015-03-24 01:06:24+0700 [republika] ERROR: Error processing 
{    'author': news's author,
	 'content': news's content,
	 'location': news's location,
	 'provider': news's provider,
	 'publish': news's published time,
	 'timestamp': news's scrapped time,
	 'title': news's title,
	 'url': 'news's url
}
```
The `ERROR` message above was produced because we didn't setup the Elasticsearch server(for testing purpose), so we don't have to worry about that.

