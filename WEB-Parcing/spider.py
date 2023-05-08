# -*- coding: utf-8 -*-

import scrapy
import time

class ProSyrSpider(scrapy.Spider):
    name = 'pro_syr'
    start_urls = ['https://pro-syr.ru/zakvaski-dlya-syra/mezofilnye/']

    def parse(self, response):
        # Get the links to each product page on the current page
        cards = response.css('div.nameproduct a::attr(href)')
        for next_page in cards:
            time.sleep(3) # Wait for 3 seconds before visiting the next page
            yield response.follow(next_page, self.parse_card)

        # Go to the next page
        next_page = response.css("div.col-sm-12 a::attr(href)")[-1].get()
        yield response.follow(next_page, self.parse)

    def parse_card(self, response):
        # Get data from the product page
        yield {
            "name": response.css("div.col-md-9 h1::text").get(),
            "price": response.css("div.col-sm-6 span.autocalc-product-price::text").get(),
            "actuality": response.css("div.product-description b.outstock::text").get()
        }
