import json

import scrapy


class DataSpider(scrapy.Spider):
    name = "interpol_spider"
    start_urls = [
        'https://ws-public.interpol.int/notices/v1/red?&resultPerPage=20&page=1',
    ]

    def parse(self, response):
        data = json.loads(response.text)

        if '_embedded' in data and 'notices' in data['_embedded']:
            for person in data['_embedded']['notices']:
                yield person
            if '_links' in data and 'next' in data['_links'] and 'href' in data['_links']['next']:
                url = data['_links']['next']['href']
                yield scrapy.Request(url=url, callback=self.parse)
        else:
            raise Exception('No data found at target url')
