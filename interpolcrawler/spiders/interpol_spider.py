import scrapy


class DataSpider(scrapy.Spider):
    name = "interpol_spider"
    start_urls = [
        'https://www.interpol.int/How-we-work/Notices/View-Red-Notices',
    ]

    def parse(self, response):

        for item in response.css('div.content div.theme div.containerMarginRight '
                                 'div.twoColumns div.twoColumns__rightColumn div.redNoticesList '
                                 'div.redNoticesList__ajaxContainer div.redNoticesList__list '
                                 'div.redNoticesList__listWrapper'):
            yield {
                'item': item.css('div.redNoticeItem').get()
            }
