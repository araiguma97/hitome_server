import sqlite3

import dao
import request

_DATABASE_NAME = "wikicache.db"

class AbstractRepository:
    def __init__(self):
        self._conn = sqlite3.connect(_DATABASE_NAME)
        self._create_daos()

    def _create_daos(self):
        pass

    def close(self):
        self._conn.close()

class CategoriesRepository(AbstractRepository):
    def _create_daos(self):
        self._categories_dao = dao.CategoriesDAO(self._conn)
        self._category_subcategories_dao = dao.CategorySubcategoriesDAO(self._conn)

    def update(self, root_category):
        self._categories_dao.create_tables()
        self._search_all_subcategories(root_category)

    def _search_all_subcategories(self, category):
        if self._categories_dao.exists_category(category):
            return

        print("Updating " + category["title"])
        self._categories_dao.update_category(category)

        subcategories = self._get_subcategories_from_wikipedia(category)
        for subcategory in subcategories:
            self._category_subcategories_dao.update_category_subcategory(category, subcategory)
            self._search_all_subcategories(subcategory)

    def _get_subcategories_from_wikipedia(self, category):
        params = {
            "action": "query",
            "format": "json",
            "list": "categorymembers",
            "formatversion": "2",
            "cmpageid": category["category_id"],
            "cmtype": "subcat",
        }
        for json in request.request_to_wikipedia(params):
            for query_categorymember in json["query"]["categorymembers"]:
                subcategory = {
                    "category_id": query_categorymember["pageid"],
                    "title": query_categorymember["title"],
                }
                yield subcategory

class CategoryPagesRepository(AbstractRepository):
    def _create_daos(self):
        self._categories_dao = dao.CategoriesDAO(self._conn)
        self._category_pages_dao = dao.CategoryPagesDAO(self._conn)

    def update(self):
        self._category_pages_dao.create_tables()

        for category_id in self._categories_dao.read_category_ids():
            for page_id in self.get_page_id_from_wikipedia(category_id):
                print("Updating " + str(page_id))
                self._category_pages_dao.update_category_pages(category_id, page_id)

    def get_page_id_from_wikipedia(self, category_id):
        params = {
            "action": "query",
            "format": "json",
            "list": "categorymembers",
            "formatversion": "2",
            "cmpageid": category_id,
            "cmtype": "page",
        }
        for json in request.request_to_wikipedia(params):
            for query_categorymember in json["query"]["categorymembers"]:
                yield query_categorymember["pageid"]

class PagesRepository(AbstractRepository):
    def _create_daos(self):
        self._category_pages_dao = dao.CategoryPagesDAO(self._conn)
        self._pages_dao = dao.PagesDAO(self._conn)

    def update(self):
        self._pages_dao.create_tables()

        for page_ids in self._category_pages_dao.read_page_ids(50):
            for page in self._get_pages_from_wikipedia(page_ids):
                print("Updating " + page["title"])
                self._pages_dao.update_page(page)

    def _get_pages_from_wikipedia(self, page_ids):
        params = {
            "action": "query",
            "format": "json",
            "prop": "coordinates|pageterms|pageprops",
            "formatversion": "2",
            "coprimary": "primary",
            "pageids": "|".join(map(str, page_ids)),
            "colimit": "50",
        }
        for json in request.request_to_wikipedia(params):
            for query_page in json["query"]["pages"]:
                base_url = "https://ja.wikipedia.org/wiki/"
                try:
                    page = {
                        "page_id": query_page["pageid"],
                        "title": query_page["title"],
                        "url": base_url + query_page["title"],
                    }
                except KeyError:
                    continue
                
                try:
                    page["latitude"] = query_page["coordinates"][0]["lat"]
                except KeyError:
                    pass

                try:
                    page["longitude"] = query_page["coordinates"][0]["lon"]
                except KeyError:
                    pass

                try:
                    page["description"] = query_page["terms"]["description"][0]
                except KeyError:
                    pass
                
                try:
                    page["image_title"] = query_page["pageprops"]["page_image_free"]
                except KeyError:
                    pass

                yield page

class ImageRepository(AbstractRepository):
    def _create_daos(self):
        self._pages_dao = dao.PagesDAO(self._conn)
        self._images_dao = dao.ImagesDAO(self._conn)

    def update(self):
        self._images_dao.create_tables()

        for image_titles in self._pages_dao.read_image_titles(50):
            for image in self._get_image_titles_from_wikipedia(image_titles):
                print("Updating " + image["image_title"])
                self._images_dao.update_image(image)

    def download(self):
        for image in self._images_dao.read_images():
            print("Downloading " + image["image_title"])
            request.download_image(image)

    def _get_image_titles_from_wikipedia(self, image_titles):
        params = {
            "action": "query",
            "format": "json",
            "prop": "imageinfo|pageimages",
            "titles": "|".join(["File:" + image_title for image_title in image_titles]),
            "formatversion": "2",
            "iiprop": "extmetadata",
            "pithumbsize": "50",
        }
        for json in request.request_to_wikipedia(params):
            for query_page in json["query"]["pages"]:
                try:
                    image = {
                        "image_title": query_page["pageimage"],
                        "url": query_page["thumbnail"]["source"],
                        "author": query_page["imageinfo"][0]["extmetadata"]["Artist"]["value"],
                        "license": query_page["imageinfo"][0]["extmetadata"]["LicenseShortName"]["value"],
                    }
                except KeyError:
                    continue

                yield image

