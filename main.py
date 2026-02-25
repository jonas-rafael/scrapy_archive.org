import os
import sys
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from tqdm import tqdm
from scrapy import signals
from pydispatch import dispatcher

from archive_hunter.spiders.librarian import LibrarianSpider
from archive_hunter.spiders.dorks import DorkSpider


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def run_interactive():
    clear_screen()
    print("═" * 60)
    print("busca")
    print("═" * 60)

    print("\n[1] Archive.org (Biblioteca Oficial)")
    print("[2] Google Drive (Via Dorks no DuckDuckGo - Público)")
    fonte = input("\nEscolha a fonte de busca (1-2): ")

    termo = input("\n O que você deseja caçar hoje? ")

    query_final = ""
    if fonte == "1":
        print("\nCategorias:")
        print("[1] Manga | [2] Quadrinho | [3] Livro | [4] ✨ TUDO")
        cat_idx = input("Escolha (1-4): ")

        mapa_cats = {
            "1": "mediatype:texts AND (subject:manga OR subject:mangá)",
            "2": "mediatype:texts AND (subject:comics OR subject:quadrinhos)",
            "3": "mediatype:texts",
            "4": ""
        }
        cat_part = mapa_cats.get(cat_idx, "")
        query_final = f'title:({termo}*)'
        if cat_part: query_final += f' AND {cat_part}'
        query_final += ' AND (language:por OR language:Portuguese)'
    else:
        # Para Dorks, o termo vai limpo ou com extensões
        query_final = termo

    filename = f"captura_{termo.replace(' ', '_')}.csv"
    settings = get_project_settings()
    settings.set('FEEDS', {
        filename: {
            'format': 'csv',
            'encoding': 'utf8',
            'store_empty': False,
            'fields': ['title', 'category', 'year', 'file_urls'],
        }
    })

    settings.set('USER_AGENT',
                 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    settings.set('ITEM_PIPELINES', {})  # Desativado para focar no CSV

    pbar = tqdm(desc=" Capturando Dados", unit=" item")

    def update_pbar(item, response, spider):
        pbar.update(1)

    dispatcher.connect(update_pbar, signal=signals.item_scraped)

    process = CrawlerProcess(settings)

    if fonte == "1":
        print(f"\n Iniciando varredura no Archive.org...")
        process.crawl(LibrarianSpider, query=query_final)
    else:
        print(f"\n Lançando Dorks para Google Drive...")
        process.crawl(DorkSpider, query=query_final)

    process.start()
    pbar.close()

    if os.path.exists(filename):
        print(f"\nconcluido")
        print(f"📊 Relatório gerado: {os.path.abspath(filename)}")
    else:
        print("\nNenhum link válido foi encontrado.")


if __name__ == "__main__":
    try:
        run_interactive()
    except KeyboardInterrupt:
        print("\n\n⚓ saindo...")
        sys.exit()