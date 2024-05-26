import requests
import json
from types import SimpleNamespace
import time


class GetInfoFromWebsites:
    def __init__(self):
        self.map1 = {}

    def get_domclick_complex_ids_info(self, offset: int, price_range: tuple) -> list:
        complex_total = 0
        url = "https://bff-search-web.domclick.ru/api/offers/v1"
        headers = {"Content-Type": "application/json",
                   "Origin": "https://spb.domclick.ru"}

        data = {"offset": offset,
                "limit": 30,
                "sort": "price",
                "sort_dir": "asc",
                "deal_type": "sale",
                "category": "living",
                "offer_type": "complex",
                "aids": 597,
                "sale_price__gte": price_range[0],
                "sale_price__lte": price_range[1],
                "rooms": [1,2,3],
                "is_apartment": 0
                }
        response = requests.get(url, params=data, headers=headers)
        if response.status_code == 200:
            response_string = response.text
            x = json.loads(response_string, object_hook=lambda d: SimpleNamespace(**d))
            complex_total = x.result.pagination.total
            # print(complex_total)
            complexes_info = x.result.items
            return complexes_info
        else:
            print("Ошибка: ", response.status_code)


    def get_domclick_offers_info(self, offset: int, price_range: tuple, complex_id: int) -> list:
        url = "https://bff-search-web.domclick.ru/api/offers/v1"
        headers = {"Content-Type": "application/json",
                   "Origin": "https://spb.domclick.ru"}

        data = {"offset": offset,
                "limit": 30,
                "sort": "price",
                "sort_dir": "asc",
                "deal_type": "sale",
                "category": "living",
                "offer_type": "layout",
                "complex_ids": complex_id,
                "sale_price__gte": price_range[0],
                "sale_price__lte": price_range[1],
                "rooms": [1,2,3],
                "is_apartment": 0
                }
        response = requests.get(url, params=data, headers=headers)
        if response.status_code == 200:
            response_string = response.text
            response_string = response_string.replace("$", "s")
            x = json.loads(response_string, object_hook=lambda d: SimpleNamespace(**d))
            offers_info = x.result.items
            return offers_info
        else:
            print("Ошибка: ", response.status_code)