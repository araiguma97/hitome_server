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
        spots = []
        spot_categories = []
        images = []

        for spot_page in self._pages_dao.read_spot_pages():
            spots.append(self.extract_spot(spot_page))
            spot_categories.extend(self.extract_spot_categories(spot_page))
            if "image_title" in spot_page:
                image = self._images_dao.find_image_by_title(spot_page["image_title"])
                if image:
                    shutil.copy("./img/" + image["image_title"], "./spot_img/" + image["image_title"])
                    images.append(image)

        self.dump_json(spots, "spots.json")
        self.dump_json(spot_categories, "spot_categories.json")
        self.dump_json(images, "images.json")
    
    def dump_json(self, d, file_name):
        if not os.path.isdir(_json_dir_path):
            os.mkdir(_json_dir_path)
        with open(_json_dir_path + file_name, "w") as f:
            json.dump(d, f, ensure_ascii=False, indent=4)

    def extract_spot(self, spot_page):
        spot = {
            "spot_id": spot_page["page_id"],
            "name": re.sub(" \(.*\)", "", spot_page["title"]),
            "url": spot_page["url"],
            "latitude": spot_page["latitude"],
            "longitude": spot_page["longitude"],
        }
        
        if "image_title" in spot_page:
            spot["image_title"] = spot_page["image_title"]

        if "description" in spot_page:
            spot["description"] = spot_page["description"]

        return spot
    
    def extract_spot_categories(self, spot_page):
        spot_categories = []
        for category_id in self._category_pages_dao.find_category_id_by_page_id(spot_page["page_id"]):
            category = self._category_dao.find_category_by_id(category_id)
            spot_category = {
                "spot_id": spot_page["page_id"],
                "category_name": re.sub("Category:", "", category["title"]),
            }
            spot_categories.append(spot_category)
        return spot_categories

if __name__ == "__main__":
    main()


