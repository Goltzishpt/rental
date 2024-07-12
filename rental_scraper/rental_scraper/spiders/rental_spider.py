import os
import scrapy
import asyncio

from rental_scraper.items import RentalScraperItem

from dotenv import load_dotenv
load_dotenv()


class RentalSpider(scrapy.Spider):
    name = 'rental'
    allowed_domains = [os.getenv("START_URL")]
    page_quantity = 99999
    start_urls = [
        f'https://{os.getenv("START_URL")}/immobilien/page/{page_quantity}'
    ]

    def parse(self, response) -> scrapy.Request:
        for rental in response.xpath(
                '//div[@class="properties"]'
                '//div[@class="property col-sm-6 col-md-4"]'
        ):
            rental_url = response.urljoin(rental.xpath(
                './/div[@class="property-thumbnail col-sm-12 vertical"]'
                '/a/@href'
            ).get())

            yield scrapy.Request(
                rental_url, callback=self.parse_rental_details
            )

    @staticmethod
    def parse_rental_details(
            response: scrapy.http.Response
    ) -> RentalScraperItem:
        item = RentalScraperItem()
        item['url'] = response.url
        # ---------------------------------------------------------------------
        item['title'] = response.xpath(
            '//h1[@class="property-title"]/text()'
        ).get()
        # ---------------------------------------------------------------------
        item['status'] = response.xpath(
            '//li[@class="list-group-item data-zustand"]'
            '//div[@class="dd col-sm-7"]/text()'
        ).get()
        # ---------------------------------------------------------------------
        item['pictures'] = response.xpath(
            '//meta[@property="og:image"]/@content').getall()
        # ---------------------------------------------------------------------
        item['rent_price'] = response.xpath(
            '//li[@class="list-group-item data-kaufpreis"]'
            '//div[@class="dd col-sm-7"]/text()'
        ).re_first(r'\d+\.\d+')

        if item['rent_price']:
            item['rent_price'] = float(item['rent_price'].replace('.', ''))
        # ---------------------------------------------------------------------
        item['description'] = response.xpath(
            '//div[contains(@class, "property-description")]'
            '//div[@class="panel-body"]//text()'
        ).getall()
        # ---------------------------------------------------------------------
        item['phone_number'] = response.xpath(
            '//div[@class="dd col-sm-7 p-tel value"]//text()'
        ).get()
        # ---------------------------------------------------------------------
        item['email'] = response.xpath(
            '//div[@class="dd col-sm-7 u-email value"]//text()'
        ).get()

        yield item
