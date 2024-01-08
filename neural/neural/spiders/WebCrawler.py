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
def find_file_in_subfolders(filename, directory = 'data'):
    for root, dirs, files in os.walk(directory):
        if filename in files:
            return True
    return None

class CrawlingSpider(CrawlSpider):
    name = 'CrawlingSpidery'
    allowed_domains = ['security.snyk.io']
    start_urls = ['https://security.snyk.io/vuln']
    
    rules = (
        Rule(LinkExtractor(allow=()), callback='parse_item', process_links='process_links'), #follow = True),
    )
    install_reactor("twisted.internet.asyncioreactor.AsyncioSelectorReactor")

    # Define the parse_item method
    def parse_item(self, response):
        if 'SNYK-' not in response.url.split('/')[-1]:
            return
        else:
            yield get_data(response.url)
    def process_links(self, links):
        for link in links:
        #1
            if find_file_in_subfolders(str(link.split('/')[-1] + '.json')):# or link.split('/')[-4] == 'package':
                continue  # skip all links that already existed
            yield link 