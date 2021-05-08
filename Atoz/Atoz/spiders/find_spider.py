import scrapy
import re


class FindSpider(scrapy.Spider):
    name = 'find_spider'
    allowed_domains = ['https://www.amazon.com.br/gp/movers-and-shakers/grocery']
    start_urls = ['https://www.amazon.com.br/gp/movers-and-shakers/grocery']

    def parse(self, response, **kwargs):
        for gp in response.css('li.zg-item-immersion'):
            name = gp.css('div.p13n-sc-truncate-desktop-type2::text').get().strip()
            link = gp.css('a.a-link-normal::attr(href)').get()
            image_link = gp.css('img::attr(src)').get()
            thermometer_rank = gp.css('span.zg-badge-text::text').get()
            recent_category_rank = gp.css('span.zg-sales-movement::text').get()
            past_category_rank = gp.css('span.zg-sales-movement::text').get()
            rank_percent_change = gp.css('span.zg-percent-change::text').get()
            average_rate = gp.css('span.a-icon-alt::text').get()
            rate_qty = gp.css('a.a-size-small.a-link-normal::text').get()
            offers_qty = gp.css('span.a-color-secondary::text').get()
            price_min = gp.css('span.a-size-base.a-color-price').get()

            yield {
                'name': name,
                'link': link,
                'image_link': image_link,
                'thermometer_rank': normalize_int(thermometer_rank),
                'recent_category_rank': category_recent_and_past(recent_category_rank)[0],
                'past_category_rank': category_recent_and_past(past_category_rank)[1],
                'rank_percent_change': normalize_int(rank_percent_change),
                'average_rate': normalize_float(average_rate),
                'rate_qty': normalize_int(rate_qty),
                'offers_qty': normalize_int(offers_qty),
                'price_min': normalize_float(price_min),
            }


def normalize_int(texto):
    """
    Normaliza os numeros inteiros extraido da web
    :param texto:
    :return: int:
    """
    if texto is not None:
        texto = re.sub(r'[^ 0-9]', '', texto).strip()
        return int(texto)


def category_recent_and_past(texto):
    texto = re.sub(r'[^ 0-9]', '', texto).lstrip().rstrip()
    texto = texto.split(' ')
    while '' in texto:
        texto.remove('')
    lista_int = [int(val) for val in texto]
    return lista_int


def normalize_float(texto):
    if texto is not None:
        texto = re.split(r'(\d+,\d+)', texto)
        texto = float(texto[1].replace(',', '.'))
    return texto
