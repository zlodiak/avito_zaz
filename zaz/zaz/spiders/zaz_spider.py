from scrapy.loader import ItemLoader
import scrapy
from urllib.parse import urljoin

from zaz.items import ZazItem


class ZazSpider(scrapy.Spider):
    name = "zaz"
    start_urls = ['https://www.avito.ru/rossiya/avtomobili?q=%D0%B7%D0%B0%D0%BF%D0%BE%D1%80%D0%BE%D0%B6%D0%B5%D1%86']
    host = 'https://www.avito.ru'
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'
    proxy = '83.149.70.159:13011'    

    def parse(self, response):
        for details_page_link in response.css('div.item_table .item__line .snippet-title .snippet-link::attr(href)').getall():
            url = urljoin(self.host, details_page_link)
            yield response.follow(
                url, 
                callback=self.parse_details_page, 
                headers={"User-Agent": self.user_agent},
                cookies=None,
                meta={"proxy": self.proxy}
            )

    def parse_details_page(self, response):
        loader = ItemLoader(item=ZazItem(), selector=response)

        loader.add_css('title', 'h1 span.title-info-title-text::text')
        loader.add_css('address', 'div.item-address span.item-address__string::text')
        loader.add_css('price', 'div.item-price span.js-item-price::text')

        yield loader.load_item()