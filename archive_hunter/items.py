import scrapy

class ArchiveItem(scrapy.Item):
    identifier = scrapy.Field()
    title = scrapy.Field()
    category = scrapy.Field()
    year = scrapy.Field()
    language = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field() # Necessário para metadados internos do Scrapy