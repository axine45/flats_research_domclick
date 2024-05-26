import time
from get_info_from_websites import GetInfoFromWebsites
from flat_domclick_mapper_dto import FlatDomClickMapperDto
from work_with_csv import WorkWithCSV
import json
from types import SimpleNamespace


class FlatCianExportService:
    price_range = (10000000, 22000000)
    rooms = [1, 2, 3]

    def export_flat_info_from_domclick(self):
        complex_info = GetInfoFromWebsites()
        complex_ids = set()
        offer_info = GetInfoFromWebsites()
        mapper_dto = FlatDomClickMapperDto(offer_info)
        writer_to_csv = WorkWithCSV()
        domclick_csv = "domclick"
        complex_all = self.get_complex_ids_dict(complex_info)
        print((complex_all))
        for complex_id, deadline in complex_all.items():
            offset = 0
            offers_info = offer_info.get_domclick_offers_info(offset, self.price_range, complex_id)
            flats_info = mapper_dto.flat_domclick_mapper_dto(offers_info, deadline)
            while offers_info != []:
                print(flats_info)
                writer_to_csv.write_info_to_csv_file(domclick_csv, flats_info)
                print(offset)
                offset = offset + 30
                offers_info = offer_info.get_domclick_offers_info(offset, self.price_range, complex_id)
                flats_info = mapper_dto.flat_domclick_mapper_dto(offers_info, deadline)
        print(flats_info)
        writer_to_csv.write_info_to_csv_file(domclick_csv, flats_info)

    def get_complex_ids_dict(self, complex_info) -> dict:
        offset = 0
        complex_dict = {}
        complexes_info = complex_info.get_domclick_complex_ids_info(offset, self.price_range)
        while complexes_info != []:
            for complex in complexes_info:
                complex_id = complex.id
                if hasattr(complex.buildingsInfo, "endBuildYear") and hasattr(complex.buildingsInfo, "endBuildQuarter"):
                    complex_deadline_year = complex.buildingsInfo.endBuildYear
                    complex_deadline_quarter = complex.buildingsInfo.endBuildQuarter
                else:
                    complex_deadline_year = complex.buildingsInfo.firstEndBuildYear
                    complex_deadline_quarter = complex.buildingsInfo.firstEndBuildQuarter
                # print(complex_id)
                complex_dict[complex_id] = (complex_deadline_year, complex_deadline_quarter)
            offset = offset + 30
            complexes_info = complex_info.get_domclick_complex_ids_info(offset, self.price_range)
        print(len(complex_dict))
        return complex_dict

    # def get_complex_ids_set(self, complex_ids, complex_info) -> set:
    #     offset = 0
    #     complexes_info = complex_info.get_domclick_complex_ids_info(offset, self.price_range)
    #     while complexes_info != []:
    #         for complex in complexes_info:
    #             complex_id = complex.id
    #             # print(complex_id)
    #             complex_ids.add(complex_id)
    #         offset = offset + 30
    #         complexes_info = complex_info.get_domclick_complex_ids_info(offset, self.price_range)
    #     print(len(complex_ids))
    #     return complex_ids

# n = FlatCianExportService()
# n.export_flat_info_from_domclick()
    #     for key, values in self.rooms_area.items():
    #         for value in values:
    #             offset = 0
    #             flats_info = self.get_domclick_data(key, mapper_dto, offer_info, offset, value, error_pages_list)
    #             while flats_info != []:
    #                 writer_to_csv.write_info_to_csv_file(cian_csv, flats_info)
    #                 print(offset/30)
    #                 time.sleep(5)
    #                 offset = offset + 30
    #                 flats_info = self.get_domclick_data(key, mapper_dto, offer_info, offset, value, error_pages_list)
    #     writer_to_csv.write_info_to_txt_file("domclick_error_pages", error_pages_list)
    #
    #
    # def get_domclick_data(self, key, mapper_dto, offer_info, offset, value, error_pages_list):
    #     try:
    #         offer_page_info = offer_info.get_cian_offers_info(offset, self.price_range, key, value)
    #         flats_info = mapper_dto.flat_cian_mapper_dto(offer_page_info)
    #     except Exception as err:
    #         time.sleep(60)
    #         error_pages_list.append(page)
    #         print(err)
    #         offer_page_info = offer_info.get_cian_offers_info(page, self.price_range, key, value)
    #         flats_info = mapper_dto.flat_cian_mapper_dto(offer_page_info)
    #     return flats_info
    #
    #
    # def get_domclick_complex_ids(self, complex_info, offset: int, price_range: tuple, complex_ids: list[int]) -> list[int]:
    #     try:
    #         complex_info_string = complex_info.get_domclick_complex_ids(offset, price_range)
    #         x = json.loads(complex_info_string, object_hook=lambda d: SimpleNamespace(**d))
    #         complexes_info = x.result.items
    #         for complex_info in complexes_info:
    #             complex_id = complex_info.id
    #             complex_ids.append(complex_id)
    #     except Exception as err:
    #         time.sleep(60)
    #         print(err)
    #     return complex_ids
