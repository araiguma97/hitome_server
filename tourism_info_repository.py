from contextlib import closing
import sqlite3
from enum import Enum
import os
import re
import shutil
import json

import dao
import repository

_json_dir_path = "./json/"

class Genre(Enum):
    HOT_SPRING=1
    THEATER=2
    PARK=3
    CASTLE=4
    SHRINE=5
    TEMPLE=6
    MUSEUM=7
    ART_MUSEUM=8
    AMUSEMENT_PARK=9
    SCENIC_SPOT=10

def main():
    with closing(TourismInfoRepository()) as tourism_info_repository:
        tourism_info_repository.update()

class TourismInfoRepository(repository.AbstractRepository):

    def _create_daos(self):
        self._category_dao = dao.CategoriesDAO(self._conn)
        self._category_pages_dao = dao.CategoryPagesDAO(self._conn)
        self._pages_dao = dao.PagesDAO(self._conn)
        self._images_dao = dao.ImagesDAO(self._conn)

    def update(self):
        tourism_info_list = []
        tourism_info_categories_list = []
        image_list = []

        for place_page in self._pages_dao.read_place_pages():
            tourism_info_list.append(self.extract_tourism_info(place_page))
            tourism_info_categories_list.append(self.extract_tourism_info_categories(place_page))
            if "image_title" in place_page:
                image = self._images_dao.find_image_by_title(place_page["image_title"])
                if image:
                    shutil.copy("./img/" + image["image_title"], "./tourism_info_img/" + image["image_title"])
                    image_list.append(image)

        self.dump_json(tourism_info_list, "tourism_info.json")
        self.dump_json(tourism_info_categories_list, "tourism_info_categories.json")
        self.dump_json(image_list, "images.json")
    
    def dump_json(self, d, file_name):
        if not os.path.isdir(_json_dir_path):
            os.mkdir(_json_dir_path)
        with open(_json_dir_path + file_name, "w") as f:
            json.dump(d, f, ensure_ascii=False, indent=4)

    def extract_tourism_info(self, place_page):
        tourism_info = {
            "tourism_info_id": place_page["page_id"],
            "name": re.sub(" \(.*\)", "", place_page["title"]),
            "url": place_page["url"],
            "latitude": place_page["latitude"],
            "longitude": place_page["longitude"],
        }
        
        if "image_title" in place_page:
            tourism_info["image_title"] = place_page["image_title"]

        if "description" in place_page:
            tourism_info["description"] = place_page["description"]

        return tourism_info
    
    def extract_tourism_info_categories(self, place_page):
        tourism_info_categories = []
        for category_id in self._category_pages_dao.find_category_id_by_page_id(place_page["page_id"]):
            category = self._category_dao.find_category_by_id(category_id)
            tourism_info_category = {
                "tourism_info_id": place_page["page_id"],
                "category_name": re.sub("Category:", "", category["title"]),
            }
            tourism_info_categories.append(tourism_info_category)
        return tourism_info_categories

if __name__ == "__main__":
    main()


