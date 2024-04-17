import scrapy


class AuthorsSpider(scrapy.Spider):
    name = "authors"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com"]

    def parse_author(self, response):
        yield {
            "fullname": response.xpath("//div[@class = 'author-title']/text()").get(),
            "born_date": response.xpath("//span[@class = 'author-born-date']/text()").get(),
            "born_location": response.xpath("//span[@class = 'author-born-location']/text()").get(),
            "description": response.xpath("//div[@class = 'author-description']/text()").get()
        }

    def parse(self, response):
        for quote in response.xpath("//div[@class='quote']"):
            author_info = quote.xpath("span/a/@href").get()
            yield response.follow(author_info, self.parse_author)
        next_page = response.xpath("//li[@class='next']/a/@href").get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)



