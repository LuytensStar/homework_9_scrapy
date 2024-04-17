import scrapy


class AuthorsSpider(scrapy.Spider):
    name = "authors"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com"]

    def to_json_author(self, response):
        yield {
            "fullname": response.meta['author_name'],
            "born_date": response.xpath("//span[@class = 'author-born-date']/text()").get(),
            "born_location": response.xpath("//span[@class = 'author-born-location']/text()").get(),
            "description": response.xpath("//div[@class = 'author-description']/text()").get()
        }

    def parse(self, response):
        for quote in response.xpath("//div[@class='quote']"):
            author_name = quote.xpath("span/small/text()").get()
            author_info = quote.xpath("span/a/@href").get()
            yield response.follow(author_info, self.to_json_author, meta={'author_name': author_name})
        next_page = response.xpath("//li[@class='next']/a/@href").get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)



class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = ['http://quotes.toscrape.com']

    def parse(self, response):
        for quote in response.xpath("//div[@class='quote']"):
            yield {
                'quote': quote.xpath("span[@class='text']/text()").get(),
                'author': quote.xpath("span/small/text()").get(),
                'tags': quote.xpath("div[@class='tags']/a/text()").getall(),
            }
        next_page = response.xpath("//li[@class='next']/a/@href").get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)