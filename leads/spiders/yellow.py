from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

class Yellow(CrawlSpider):
    allowed_domain = ['yellowpage.com']
    start_urls = ['https://www.yellowpages.com/search?search_terms=Air+Conditioning+Contractors+%26+Systems&geo_location_terms=New+York%2C+NY']

    le_items = LinkExtractor(restrict_css='.search-results > .result > .srp-listing > .v-card > .media-thumbnail > a')
    items_rule = Rule(le_items, callback='parse_item', follow=True)

    le_pagination = LinkExtractor(restrict_css='.pagination > ul > li > a.next')
    page_rule = Rule(le_pagination, follow=True)

    rules = [items_rule, page_rule]
    name = 'leads'

    def parse_item(self, response):
        lead = {}
        lead['name'] = response.css('h1.dockable::text').get()
        print(lead['name'])
        lead['phone'] = response.xpath("//*[@id='details-card']/p[@class='phone']/text()").get()
        lead['address'] = response.xpath("//*[@id='details-card']/p[2]/text()").get()
        lead['website'] = response.css('#details-card > .website > a::attr(href)').get()
        try:
            lead['email'] = response.css('.more-info-block > dl > dd > a.email-business::attr(href)').get()
            lead['email'] = lead['email'].split(':')[-1]
        except:
            lead['email'] = ''
        lead['payment'] = response.css('.more-info-block > dl > dd.payment::text').get()
        lead['link'] = response.url
        yield lead





