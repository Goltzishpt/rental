import os
import scrapy
import pandas as pd

from typing import List, NoReturn


class RentalScraperPipeline:

    def open_spider(self) -> NoReturn:
        self.items = []

    def close_spider(self, spider: scrapy.Spider) -> NoReturn:
        if self.items:
            df = pd.DataFrame(self.items)
            country = "Germany"
            domain = spider.allowed_domains[0]
            directory = os.path.join(country, domain)
            os.makedirs(directory, exist_ok=True)
            file_path = os.path.join(directory, 'rental_object.csv')
            df.to_csv(file_path, index=False)

    def process_item(self, item: List) -> List:
        self.items.append(dict(item))
        return item
