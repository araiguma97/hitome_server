import requests
import time
import os
import re
from contextlib import closing
from typing import Generator, Optional

import utils
import config
from categories.categories_repository import CategoriesRepository
from pages.page import Page
from pages.pages_repository import PagesRepository
from images.images_repository import ImagesRepository


def main():
    with closing(TourismInfoRetriever()) as tourism_info_retriever:
        tourism_info_retriever.retrieve(should_update = False)

class TourismInfoRetriever:
    def __init__(self) -> None:
        self._categories_repository = CategoriesRepository()
        self._pages_repository      = PagesRepository()
        self._images_repository     = ImagesRepository()

    def close(self) -> None:
        self._categories_repository.close()
        self._pages_repository.close()
        self._images_repository.close()

    def retrieve(self, should_update: bool = True) -> None:
        if should_update:
            self._categories_repository.update()
            self._pages_repository.update()
            self._images_repository.update()
        self._dump_tourism_info()        

    def _dump_tourism_info(self):
        spots           = []
        spot_categories = []
        images          = []

        for page in self._pages_repository.get():
            if page.latitude is None or page.longitude is None:
                continue

            spots.append(self._extract_spot(page))
            
            spot_categories.extend(self._extract_spot_categories(page))

            image = self._extract_image(page)
            if image is not None:
                images.append(image)

        utils.dump_json("output", spots,           "spots.json")
        utils.dump_json("output", spot_categories, "spot_categories.json")
        utils.dump_json("output", images,          "images.json")
        self._save_images(images)

    def _extract_spot(self, page: Page) -> dict:
        return {
            "spot_id": page.page_id,
            "name": re.sub(" \(.*\)", "", page.title),
            "source": page.source,
            "latitude": page.latitude,
            "longitude": page.longitude,
            "image_title": page.image_title,
            "description": page.description
        }
    
    def _extract_spot_categories(self, page: Page) -> Generator[dict, None, None]:
        for category in self._categories_repository.get_categories(page):
            yield {
                "spot_id": page.page_id,
                "category_name": re.sub("Category:", "", category.title),
            }
    
    def _extract_image(self, page: Page) -> Optional[dict]:
        image = self._images_repository.get_page_image(page)
        if image is None:
            return None

        return {
            "image_title": image.image_title,
            "source": image.source,
            "author": image.author,
            "license": image.license 
        }

    def _save_images(self, images: list[dict]):
        image_dir_path = "./img/"
        sleep_sec = 10

        for image in images:
            image_file_path = image_dir_path + image["image_title"]

            if os.path.isfile(image_file_path):
                print("Canceled downloading image \"" + image["image_title"] + "\"")
                continue

            print("Downloading image \"" + image["image_title"] + "\"")

            response = requests.get(image["source"], headers = config.headers)
            response.raise_for_status()
            time.sleep(sleep_sec)

            if not os.path.isdir(image_dir_path):
                os.mkdir(image_dir_path)
            with open(image_file_path, "wb") as f:
                f.write(response.content)

if __name__ == "__main__":
    main()
