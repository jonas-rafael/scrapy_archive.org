import scrapy
import json
from ..items import ArchiveItem


class LibrarianSpider(scrapy.Spider):
    name = "librarian"

    def __init__(self, query=None, *args, **kwargs):
        super(LibrarianSpider, self).__init__(*args, **kwargs)
        self.query = query
        # Buscamos metadados básicos na API
        self.search_url = f"https://archive.org/advancedsearch.php?q={self.query}&fl[]=identifier,title,year,subject,language,mediatype&rows=50&output=json"

    def start_requests(self):
        yield scrapy.Request(self.search_url, callback=self.parse_search)

    def parse_search(self, response):
        data = json.loads(response.text)
        docs = data.get('response', {}).get('docs', [])

        for doc in docs:
            item = ArchiveItem()
            item['identifier'] = doc.get('identifier')
            item['title'] = doc.get('title', 'Sem Título')
            item['year'] = doc.get('year', 'N/A')
            item['language'] = str(doc.get('language', 'N/A'))

            # Classificação Flexível
            subjects = str(doc.get('subject', [])).lower()
            mtype = str(doc.get('mediatype', '')).lower()

            if 'manga' in subjects:
                item['category'] = 'Manga'
            elif 'comic' in subjects or 'quadrinho' in subjects:
                item['category'] = 'Quadrinho'
            elif mtype == 'texts':
                item['category'] = 'Livro/Texto'
            else:
                item['category'] = f'Geral ({mtype})'

            # Consultar arquivos disponíveis
            meta_api = f"https://archive.org/metadata/{item['identifier']}"
            yield scrapy.Request(meta_api, callback=self.parse_metadata, meta={'item': item})

    def parse_metadata(self, response):
        item = response.meta['item']
        data = json.loads(response.text)
        files = data.get('files', [])

        # Lista de extensões que aceitamos (expandida para o modo livre)
        extensoes_alvo = ('.pdf', '.epub', '.cbz', '.cbr', '.mp4', '.mp3')

        links = []
        for f in files:
            name = f['name']
            if name.lower().endswith(extensoes_alvo):
                download_url = f"https://archive.org/download/{item['identifier']}/{name}"
                links.append(download_url)

        if links:
            item['file_urls'] = links
            yield item