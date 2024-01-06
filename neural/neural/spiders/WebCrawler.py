from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.crawler import CrawlerProcess
from datetime import datetime
from scrapy.utils.reactor import install_reactor
import sys
sys.path.insert(0, r'E:\Programming\Python practice\RISE\WebCrawler\neural\neural\spiders')
from Test_BE import *
# Define the spider class

class CrawlingSpider(CrawlSpider):
    name = 'CrawlingSpidery'
    allowed_domains = ['security.snyk.io']
    start_urls = ['https://security.snyk.io/vuln']
    # custom_settings = {
    #     'CONCURRENT_REQUESTS': 1,
    #     'CONCURRENT_ITEMS' :1,
    #     'CLOSESPIDER_PAGECOUNT': 2,
    #     'CLOSESPIDER_ITEMCOUNT': 10
    # }
    
    rules = (
        Rule(LinkExtractor(allow=()), callback='parse_item', follow=True),
    )
    install_reactor("twisted.internet.asyncioreactor.AsyncioSelectorReactor")

    # Define the parse_item method
    def parse_item(self, response):
        if 'SNYK-' not in response.url.split('/')[-1]:
            return
        else:
            yield get_data(response.url)