from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.crawler import CrawlerProcess
from datetime import datetime
from scrapy.utils.reactor import install_reactor
import json
# Define the spider class

class CrawlingSpider(CrawlSpider):
    name = 'CrawlingSpidery'
    #start_urls = ['http://www.example.com/']
    allowed_domains = ['security.snyk.io']#, ' nvd.nist.gov', 'security.snyk.io', 'toscrape.com']
    # custom_settings = {
    #     'CONCURRENT_REQUESTS': 1,
    #     'CONCURRENT_ITEMS' :1,
    #     'CLOSESPIDER_PAGECOUNT': 2,
    #     'CLOSESPIDER_ITEMCOUNT': 10
    # }
    # start_urls = ['https://security.snyk.io/vuln/SNYK-PYTHON-GRIPTAPE-6138264']
    start_urls = ['https://security.snyk.io/vuln']

    rules = (
        #r'^https://security.snyk.io/vuln/SNYK'
        Rule(LinkExtractor(allow=()), callback='parse_item', follow=True),
    )
    install_reactor("twisted.internet.asyncioreactor.AsyncioSelectorReactor")

    # Define the parse_item method
    def parse_item(self, response):
        if 'SNYK-' not in response.url.split('/')[-1]:
            return
        else:
            yield {
                'vulnerability': response.css('.title::text').get().strip(),
                'affecting': ' '.join(text.strip() for text in response.css('span.subheading *::text').getall()),
                'severity score': response.css('div::attr(data-snyk-test-score)').get(),
                'severity level': response.css('span.vue--badge__text::text').get().strip(),
                'id': response.url,
                'fix': ' '.join(text.strip() for text in response.css('.vuln-page__content .markdown-section .vue--prose .vue--markdown-to-html.markdown-description p *::text').getall()),
                #'overview': ' '.join(response.css('div[data-v-43af9ae8] .markdown-section .vue--prose .vue--markdown-to-html.markdown-description p *::text').getall()[3:]),
            }
        #self.items.append(item)    

# process = CrawlerProcess()
# process.crawl(CrawlingSpider)
# process.start()