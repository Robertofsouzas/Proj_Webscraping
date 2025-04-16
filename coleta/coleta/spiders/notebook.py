import scrapy
import logging


class NotebookSpider(scrapy.Spider):
    name = "notebook"
    allowed_domains = ["mercadolivre.com.br"]
    start_urls = ["https://lista.mercadolivre.com.br/notebook?sb=rb#D[A:notebook]"]

    def parse(self, response):
        # Seleciona os produtos na página
        products = response.css('div.ui-search-result__wrapper')
        logging.info(f"Produtos encontrados: {len(products)}")

        for product in products:
            yield {
                'brand': product.css('span.poly-component__brand::text').get(),  # Marca do produto
                'name': product.css('a.poly-component__title::text').get() ,  # nome do produto
                'seller': product.css('span.poly-component__seller::text').get(),
                'reviews_rating_number': product.css('span.poly-reviews__rating::text').get(),
                'reviews_amount': product.css('span.poly-reviews__total::text').get(),
                #'old_money': prices[0] if len (prices) > 0 else None,
                #'new_money': prices[1] if len (prices) > 1 else None
            }
            
        
