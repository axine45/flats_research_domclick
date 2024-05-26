import json
import requests
from types import SimpleNamespace
from get_info_from_websites import GetInfoFromWebsites
from flat_dto import FlatDto


class FlatDomClickMapperDto:
    def __init__(self, get_flats_info_from_web: GetInfoFromWebsites):
        self.get_flats_info_from_web = get_flats_info_from_web

    def flat_domclick_mapper_dto(self, offers_info: list, deadline: tuple) -> list[FlatDto]:
        flat_info = []
        flats_info = []
        total_area = 0
        floor_number = 0
        rooms_count = 0
        deadline_year = 0
        deadline_quarter_int = 0
        jk = ""
        similar_status = False
        similar_count = 0
        for offer_info in offers_info:
            if offer_info.sstype == "LayoutSnippet":
                jk = offer_info.complex.name
                total_area = offer_info.generalInfo.area
                floor_number = offer_info.generalInfo.maxFloor
                rooms_count = offer_info.generalInfo.rooms
                deadline_year = offer_info.complex.building.endBuildYear
                deadline_quarter_int = offer_info.complex.building.endBuildQuarter
                developer_jk_id = offer_info.complex.id
            elif offer_info.sstype == "ProductSnippet":
                jk = offer_info.flatComplex.name
                total_area = offer_info.objectInfo.area
                floor_number = offer_info.objectInfo.floor
                rooms_count = offer_info.objectInfo.rooms
                deadline_year = deadline[0]
                deadline_quarter_int = deadline[1]
                developer_jk_id = offer_info.flatComplex.id
            address = offer_info.address.displayName
            coordinates_lng = offer_info.location.lon
            coordinates_lat = offer_info.location.lat
            price = offer_info.price
            price_per_area = price/total_area
            decoration = "without"
            sale_from_developer = True
            offer_id = offer_info.id
            if hasattr(offer_info, "offersCount"):
                if offer_info.offersCount > 1:
                    similar_status = True
                    similar_count = offer_info.offersCount - 1
                else:
                    similar_status = False
                    similar_count = 0

            flat_info = FlatDto([jk, address, coordinates_lng, coordinates_lat, price, total_area, price_per_area, floor_number,
                                 rooms_count, decoration, deadline_year, deadline_quarter_int, developer_jk_id, sale_from_developer,
                                 offer_id, similar_status, similar_count])
            flats_info.append(flat_info)
        return flats_info



