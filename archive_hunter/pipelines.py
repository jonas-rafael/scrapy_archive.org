import os
import re

import scrapy
from scrapy.pipelines.files import FilesPipeline

class ArchiveDownloadPipeline(FilesPipeline):
    def file_path(self, request, response=None, info=None, *, item=None):
        # Limpa o título para ser um nome de arquivo válido
        clean_title = re.sub(r'[^\w\s-]', '', item['title']).strip().replace(' ', '_')
        identifier = item['identifier']
        # Retorna o caminho: data/python_books/nome_do_livro_ID.pdf
        return f"full/{clean_title}_{identifier}.pdf"

    def get_media_requests(self, item, info):
        # Envia as URLs para o motor de download do Scrapy
        for file_url in item.get('file_urls', []):
            yield scrapy.Request(file_url, meta={'item': item})