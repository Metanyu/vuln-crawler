from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.crawler import CrawlerProcess
from datetime import datetime
from scrapy.http import Request, Response

from scrapy.utils.reactor import install_reactor

# Define the spider class

class CrawlingSpider(CrawlSpider):
    name = 'TestCrawl'
    #start_urls = ['http://www.example.com/']
    #allowed_domains = ['cve.mitre.org', ' nvd.nist.gov', 'security.snyk.io', 'toscrape.com']
    allowed_domains = ['toscrape.com']
    start_urls = ['https://books.toscrape.com/']
    custom_settings = {
        'CONCURRENT_REQUESTS': 1,
        'CONCURRENT_ITEMS' :1,
        'CLOSESPIDER_PAGECOUNT': 1,
        'CLOSESPIDER_ITEMCOUNT': 10
    }
    rules = (
        Rule(LinkExtractor(allow='catalogue', deny='category'), callback='parse_item', follow=True),
    )
    install_reactor("twisted.internet.asyncioreactor.AsyncioSelectorReactor")
    # Define the parse_item method 
    def parse_item(self, response):
        yield {
            'title': response.css('.product_main h1::text').get(),
            'price': response.css('.price_color::text').get(), 
            'description': response.css('.product_page > p::text').get(),
        }

# process = CrawlerProcess()
# process.crawl(CrawlingSpider)
# process.start()