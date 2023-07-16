import utils

from tqdm import tqdm

class CategoriesRepository:
    def __init__(self, dao):
        self._dao = dao

    def update(self, root_category):
        self._dao.create_tables()
        self._search_all_subcategories(root_category)

    def read_category_ids(self):
        return self._dao.read_category_ids()

    def _search_all_subcategories(self, category):
        if self._dao.exists_category(category):
            return

        print("Updating " + category["title"])
        self._dao.update_category(category)

        subcategories = self._get_subcategories(category)
        for subcategory in subcategories:
            self._dao.update_category_subcategory(category, subcategory)
            self._search_all_subcategories(subcategory)

    def _get_subcategories(self, category):
        params = {
            "action": "query",
            "format": "json",
            "list": "categorymembers",
            "formatversion": "2",
            "cmpageid": category["category_id"],
            "cmtype": "subcat",
        }
        for json in utils.request_to_wikipedia_api(params):
            for query_categorymember in json["query"]["categorymembers"]:
                category = {
                    "category_id": query_categorymember["pageid"],
                    "title": query_categorymember["title"],
                }
                yield category

class CategoryPagesRepository:
    def __init__(self, dao):
        self._dao = dao

    def update(self, category_ids):
        self._dao.create_tables()

        for category_id in tqdm(category_ids, desc="Updating category pages"):
            params = {
                "action": "query",
                "format": "json",
                "list": "categorymembers",
                "formatversion": "2",
                "cmpageid": category_id,
                "cmtype": "page",
            }
            for json in utils.request_to_wikipedia_api(params):
                for query_categorymember in json["query"]["categorymembers"]:
                    self._dao.update_category_pages(category_id, query_categorymember["pageid"])

    def read_page_ids(self):
        return self._dao.read_page_ids()

class PagesRepository:
    def __init__(self, dao):
        self._dao = dao

    def update(self, page_ids):
        self._dao.create_tables()

        for json in self._get_jsons(page_ids):
            self._update_pages(json)

    def read_image_titles(self):
        return self._dao.read_image_titles()

    def _get_jsons(self, page_ids):
        jsons = []

        for splited_pageids in tqdm(utils.split_list(page_ids, 50), desc="Updating pages"):
            params = {
                "action": "query",
                "format": "json",
                "prop": "coordinates|pageterms|pageprops",
                "formatversion": "2",
                "coprimary": "primary",
                "pageids": "|".join(map(str, splited_pageids)),
                "colimit": "50",
            }
            json = utils.request_to_wikipedia_api(params)
            jsons.extend(json)

        return jsons

    def _update_pages(self, json):
        for query_page in json["query"]["pages"]:
            base_url = "https://ja.wikipedia.org/wiki/"
            try:
                page = {
                    "page_id": query_page["pageid"],
                    "title": query_page["title"],
                    "latitude": query_page["coordinates"][0]["lat"],
                    "longitude": query_page["coordinates"][0]["lon"],
                    "url": base_url + query_page["title"],
                }
            except KeyError:
                continue

            try:
                page["description"] = query_page["terms"]["description"][0]
            except KeyError:
                pass

            self._dao.update_page(page)

            try:
                image_title = query_page["pageprops"]["page_image_free"]
            except KeyError:
                continue

            self._dao.update_page_image(page, image_title)

class ImageRepository:
    def __init__(self, dao):
        self._dao = dao

    def update(self, image_titles):
        self._dao.create_tables()

        for json in self._get_jsons(image_titles):
            self._update_images(json)

    def read_images(self):
        return self._dao.read_images()

    def _get_jsons(self, image_titles):
        jsons = []

        for splited_image_titles in tqdm(utils.split_list(image_titles, 50), desc="Updating images"):
            image_page_titles = ["File:" + image_title for image_title in splited_image_titles]
            params = {
                "action": "query",
                "format": "json",
                "prop": "imageinfo|pageimages",
                "titles": "|".join(map(str, image_page_titles)),
                "formatversion": "2",
                "iiprop": "extmetadata",
                "pithumbsize": "50",
            }
            json = utils.request_to_wikipedia_api(params)
            jsons.extend(json)

        return jsons

    def _update_images(self, json):
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

            self._dao.update_image(image)

