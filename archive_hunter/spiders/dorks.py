import scrapy
from urllib.parse import quote


class DorkSpider(scrapy.Spider):
    name = "dork_hunter"

    def __init__(self, query=None, *args, **kwargs):
        super(DorkSpider, self).__init__(*args, **kwargs)
        # Dork: busca por links do drive que contenham o termo
        self.dork = f'site:drive.google.com "{query}"'
        self.start_url = f"https://duckduckgo.com/html/?q={quote(self.dork)}"

    def start_requests(self):
        yield scrapy.Request(self.start_url, callback=self.parse)

    def parse(self, response):
        # Seleciona os links de resultados do DuckDuckGo
        links = response.css('.result__url::text').getall()

        for link in links:
            link = link.strip()
            if 'drive.google.com' in link:
                yield {
                    'title': 'Link Público Google Drive',
                    'category': 'Google Drive Dork',
                    'year': 'N/A',
                    'file_urls': f"https://{link}"
                }