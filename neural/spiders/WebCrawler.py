from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.crawler import CrawlerProcess
from datetime import datetime
from scrapy.utils.reactor import install_reactor
import sys
sys.path.insert(-1, 'spiders')
from Test_BE import *
# Define the spider class
import os
def find_file_in_subfolders(filename, directory = 'vuln'):
    for root, dirs, files in os.walk(directory):
        if filename in files:
            return True
    return None

class CrawlingSpider(CrawlSpider):
    name = 'CrawlingSpidery'
    allowed_domains = ['security.snyk.io']
    start_urls = ['https://security.snyk.io/vuln/']
    # for i in range(2, 31):
    #     start_urls.append(start_urls[0] + str(i))
    
    rules = (
        Rule(LinkExtractor(allow=()), callback='parse_item', follow = True),
    )
    install_reactor("twisted.internet.asyncioreactor.AsyncioSelectorReactor")
    # Define the parse_item method
    # def parse(self, response):
    #     yield self.parse_item(response)

    #     next_page = 'https://security.snyk.io/vuln/' + str(CrawlingSpider.page_number)
    #     if CrawlingSpider.page_number < 30:
    #         CrawlingSpider.page_number += 1
    #         yield response.follow(next_page, callback=self.parse)

    def parse_item(self, response):
        if 'SNYK-' not in response.url.split('/')[-1]:
            return
        else:
            yield get_data(response.url)
    def process_links(self, links):
        for link in links:
            if find_file_in_subfolders(str(link).split('/')[-1] + '.json'):# or link.split('/')[-4] == 'package':
                print('DUPLICATE FOUND FOUND')
                continue  # skip all links that already existed
            
            yield link 