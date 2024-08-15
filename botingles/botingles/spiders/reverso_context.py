import scrapy


class ReversoContextScraperSpider(scrapy.Spider):
    # identidade
    name = 'tradutorbot'

    def start_requests(self):

        palavras = [
            "put it",
            "taken",
            "shook",
            "heartache",
            "through",
            "bullets"
        ]

        urls = []
        for palavra in palavras:
            urls.append((palavra, f'https://context.reverso.net/traducao/ingles-portugues/{palavra}'))
        for palavra, url in urls:
            yield scrapy.Request(url=url, callback=self.parse, cb_kwargs={'palavra': palavra})

    def parse(self, response, palavra, **kwargs):
        for item in response.xpath('//div[@id="translations-content"]'):
            yield {
                'Palavra': palavra,
                'Tradução': item.xpath('//div[@id="translations-content"]//'
                                       'span[@class="display-term"]/text()').getall()[0:3],
            }
