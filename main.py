from hmw_8.hmw_8.spiders.authandquot import AuthorsSpider, QuotesSpider
from scrapy.crawler import CrawlerProcess

process = CrawlerProcess(settings={"FEED_FORMAT": 'json',
                                   "FEED_URI": 'authors.json'})
process.crawl(AuthorsSpider)

process = CrawlerProcess(settings={'FEED_FORMAT': 'json',
                                   'FEED_URI': 'quotes.json'})

process.crawl(QuotesSpider)
process.start()