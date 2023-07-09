from tqdm import tqdm

from . import utils

_images = []

def extract(titles):
    # Create empty images
    for title in titles:
        image = {
            "title": title
        } 
        _images.append(image)

    # Extract by Wikipedia api
    for wikipedia_json in _get_jsons_by_wikipedia_api(titles):
        _extract_from_wikipedia(wikipedia_json)

    return _images

def _get_jsons_by_wikipedia_api(titles):
    jsons = []

    for splited_titles in tqdm(utils.split_list(titles, 50), desc="Extracting images"):
        page_titles = ["File:" + title for title in splited_titles]
        params = {
            "action": "query",
            "format": "json",
            "prop": "imageinfo|pageimages",
            "titles": "|".join(map(str, page_titles)),
            "formatversion": "2",
            "iiprop": "extmetadata",
            "pithumbsize": "1280",
        }
        json = utils.request_to_wikipedia_api(params)
        jsons.extend(json)

    return jsons

def _extract_from_wikipedia(wikipedia_json):
    for query_page in wikipedia_json["query"]["pages"]:
        target_image = _find_image_by_title(query_page["pageimage"], _images)
        try:
            target_image["url"] = str(query_page["thumbnail"]["source"])
            target_image["author"] = str(query_page["imageinfo"][0]["extmetadata"]["Artist"]["value"])
            target_image["license"] = str(query_page["imageinfo"][0]["extmetadata"]["LicenseShortName"]["value"])
        except KeyError:
            pass

def _find_image_by_title(title, images):
    for image in images:
        if image["title"] == title:
            return image

