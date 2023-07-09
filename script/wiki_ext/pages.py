from tqdm import tqdm

from . import utils

_pages = []

def extract(pageids):
    # Create empty page
    for pageid in pageids:
        page = {
            "pageid": pageid
        } 
        _pages.append(page)

    # Extract by Wikipedia api
    for wikipedia_json in _get_jsons_by_wikipedia_api(pageids):
        _extract_from_wikipedia(wikipedia_json)

    return _pages

def _get_jsons_by_wikipedia_api(pageids):
    jsons = []

    for splited_pageids in tqdm(utils.split_list(pageids, 50), desc="Extracting pages"):
        params = {
            "action": "query",
            "format": "json",
            "prop": "coordinates|pageimages|pageterms",
            "formatversion": "2",
            "coprimary": "primary",
            "pageids": "|".join(map(str, splited_pageids)),
            "colimit": "50",
        }
        json = utils.request_to_wikipedia_api(params)
        jsons.extend(json)

    return jsons

def _extract_from_wikipedia(wikipedia_json):
    for query_page in wikipedia_json["query"]["pages"]:
        target_page = _find_page_by_pageid(query_page["pageid"], _pages)
        try: # Title
            target_page["title"] = str(query_page["title"])
        except KeyError:
            pass
        
        try: # Coordinates
            coordinates = {
                "latitude": query_page["coordinates"][0]["lat"],
                "longitude": query_page["coordinates"][0]["lon"],
            }
            target_page["cordinates"] = coordinates
        except KeyError:
            pass

        try: # Image title
            target_page["image_title"] = str(query_page["pageimage"])
        except KeyError:
            pass

        try: # Description
            target_page["description"] = str(query_page["terms"]["description"][0])
        except KeyError:
            pass

def _find_page_by_pageid(pageid, pages):
    for page in pages:
        if page["pageid"] == pageid:
            return page

def get_image_titles(pages):
    image_titles = []

    for page in pages:
        if "image_title" not in page:
            continue
        image_titles.append(page["image_title"])

    return image_titles

