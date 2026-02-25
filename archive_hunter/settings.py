BOT_NAME = 'archive_hunter'
SPIDER_MODULES = ['archive_hunter.spiders']
NEWSPIDER_MODULE = 'archive_hunter.spiders'

# Identificação (Seja honesto com o site)
USER_AGENT = 'ArchiveDataBot/1.0 (+http://meusite.com)'

# Obedecer robots.txt
ROBOTSTXT_OBEY = True

# Habilitar o Pipeline de Download que criamos
ITEM_PIPELINES = {
    'archive_hunter.pipelines.ArchiveDownloadPipeline': 1,
}

# Onde os arquivos serão salvos localmente
FILES_STORE = 'downloads/archive_data'

# Autothrottle: Ajusta a velocidade baseado na carga do servidor (Essencial!)
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 2.0
AUTOTHROTTLE_MAX_DELAY = 10.0

# Formato de saída dos metadados (para análise em Data Science)
FEEDS = {
    'metadata_results.json': {'format': 'json', 'overwrite': True},
}