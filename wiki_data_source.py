from typing import Any, Generator, Optional
import requests
import time

import config
from categories.category import Category
from images.image import Image
from pages.page import Page


class WikiDataSource:
    def get_category_by_title(self, title: str) -> Optional[Category]:
        params = {
            "action": "query",
            "format": "json",
            "titles": title,
            "formatversion": "2"
        }
        json = self._request_to_wikipedia(params).__next__()
        try:
            return Category(
                category_id = json["query"]["pages"][0]["pageid"],
                title       = json["query"]["pages"][0]["title"],
            )
        except KeyError:
            return None
        except ValueError:
            return None

    def get_subcategories(self, category: Category) -> Generator[Category, None, None]:
        params = {
            "action": "query",
            "format": "json",
            "list": "categorymembers",
            "formatversion": "2",
            "cmpageid": category.category_id,
            "cmtype": "subcat",
        }
        for json in self._request_to_wikipedia(params):
            for query_categorymember in json["query"]["categorymembers"]:
                yield Category(
                    category_id = query_categorymember["pageid"],
                    title       = query_categorymember["title"]
                )

    def get_page_id(self, category_id: int) -> Generator[int, None, None]:
            params = {
                "action": "query",
                "format": "json",
                "list": "categorymembers",
                "formatversion": "2",
                "cmpageid": category_id,
                "cmtype": "page",
            }
            for json in self._request_to_wikipedia(params):
                for query_categorymember in json["query"]["categorymembers"]:
                    yield query_categorymember["pageid"]

    def get_page(self, page_ids: list[int]) -> Generator[Page, None, None]:
        params = {
            "action": "query",
            "format": "json",
            "prop": "coordinates|pageterms|pageprops",
            "pageids": "|".join(map(str, page_ids)),
            "formatversion": "2",
            "coprimary": "primary",
            "colimit": "50",
        }
        for json in self._request_to_wikipedia(params):
            for query_page in json["query"]["pages"]:
                base_url = "https://ja.wikipedia.org/?curid="
                try:
                    page = Page(
                        page_id = query_page["pageid"],
                        title = query_page["title"],
                        source = base_url + str(query_page["pageid"]),
                        latitude = query_page.get("coordinates", [{}])[0].get("lat"),
                        longitude = query_page.get("coordinates", [{}])[0].get("lon"),
                        description = query_page.get("terms", {}).get("description", [""])[0],
                        image_title = query_page.get("pageprops", {}).get("page_image_free")
                    )
                except KeyError:
                    continue

                yield page

    def get_image_titles(self, image_titles: list[str]) -> Generator[Image, None, None]:
        params = {
            "action": "query",
            "format": "json",
            "prop": "imageinfo|pageimages",
            "titles": "|".join(["File:" + image_title for image_title in image_titles]),
            "formatversion": "2",
            "iiprop": "extmetadata",
            "pithumbsize": "50",
        }
        for json in self._request_to_wikipedia(params):
            for query_page in json["query"]["pages"]:
                try:
                    yield Image(
                        image_title = query_page["pageimage"],
                        source = query_page["thumbnail"]["source"],
                        author = query_page["imageinfo"][0]["extmetadata"]["Artist"]["value"],
                        license = query_page["imageinfo"][0]["extmetadata"]["LicenseShortName"]["value"]
                    )
                except KeyError:
                    continue

    def get_text(self, page_id: int) -> str:
        params = {
            "action": "query",
            "format": "json",
            "prop": "extracts",
            "pageids": page_id,
            "formatversion": "2",
            "exlimit": "1",
            "explaintext": 1,
        }
        json = self._request_to_wikipedia(params).__next__()
        try:
            return json["query"]["pages"][0]["extract"]
        except KeyError:
            return ""
        except ValueError:
            return ""

    def _request_to_wikipedia(self, params: dict[Any, Any]) -> Generator[Any, None, None]:
        wikipedia_url = "https://ja.wikipedia.org/w/api.php"
        sleep_sec = 1

        while True: 
            response = requests.get(wikipedia_url, params = params, headers = config.headers)
            response.raise_for_status()
            time.sleep(sleep_sec)

            json = response.json()
            yield json

            try:
                params["cmcontinue"] = json["continue"]["cmcontinue"]
            except KeyError:
                break
