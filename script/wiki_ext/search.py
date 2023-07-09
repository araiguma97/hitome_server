from tqdm import tqdm

from . import utils

_category_pageids = []

def search_categories(category_pageid):
    _search_all_subcategories(category_pageid)
    return _category_pageids

def _search_all_subcategories(category_pageid):
    if category_pageid in _category_pageids:
        return

    _category_pageids.append(category_pageid)
    print("[wiki_search] Appended category (pageid=" + str(category_pageid) + ")")

    for subcategory_pageid in _get_subcategory_pageids(category_pageid):
        _search_all_subcategories(subcategory_pageid)

    return _category_pageids

def _get_subcategory_pageids(category_pageid):
    params = {
        "action": "query",
        "format": "json",
        "list": "categorymembers",
        "formatversion": "2",
        "cmpageid": category_pageid,
        "cmtype": "subcat",
    }
    for json in utils.request_to_wikipedia_api(params):
        for query_categorymember in json["query"]["categorymembers"]:
            yield query_categorymember["pageid"]

def search_pages(category_pageids):
    pageids = []

    for category_pageid in tqdm(category_pageids, desc="Searching pages"):
        params = {
            "action": "query",
            "format": "json",
            "list": "categorymembers",
            "formatversion": "2",
            "cmpageid": str(category_pageid),
            "cmtype": "page",
        }
        for json in utils.request_to_wikipedia_api(params):
            for query_categorymember in json["query"]["categorymembers"]:
                pageids.append(query_categorymember["pageid"])

    return pageids

