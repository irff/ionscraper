# ionscraper
Online Media Scraper

## Online Media List
List of media

### Indonesian Media
- http://www.antaranews.com/
- http://www.bbc.co.uk/indonesia
- http://www.beritasatu.com/
- http://www.bijaks.net/
- http://www.bisnis.com/
- http://www.cnnindonesia.com/
- http://www.detik.com/
- http://www.inilah.com/
- http://id.beritasatu.com/home/
- http://thejakartaglobe.beritasatu.com/
- http://www.jawapos.com/
- http://www.kompas.com/
- http://kontan.co.id/
- http://www.liputan6.com/
- http://mediaindonesia.com/
- http://www.merdeka.com/
- http://www.metrotvnews.com/
- http://okezone.com/
- http://www.pikiran-rakyat.com/
- http://www.rmol.co/
- http://www.republika.co.id/
- http://www.suara.com/
- http://swa.co.id/
- http://www.tempo.co/
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

