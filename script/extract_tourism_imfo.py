import wiki_ext.images
import wiki_ext.pages
import wiki_ext.search
import wiki_ext.utils

_file_names = {
    "category_pageids": "category_pageids.json",
    "pageids":          "pageids.json",
    "pages":            "pages.json",
    "images":           "images.json",
}

def main():
    root_pageid = 364779

    # Category pageids
    category_pageids = []
    if wiki_ext.utils.exists_json(_file_names["category_pageids"]):
        category_pageids = wiki_ext.utils.load_json(_file_names["category_pageids"])
    else:
        category_pageids = wiki_ext.search.search_categories(root_pageid)
        wiki_ext.utils.dump_json(category_pageids, _file_names["category_pageids"])

    # pageids
    pageids = []
    if wiki_ext.utils.exists_json(_file_names["pageids"]):
        pageids = wiki_ext.utils.load_json(_file_names["pageids"])
    else:
        pageids = wiki_ext.search.search_pages(category_pageids)
        wiki_ext.utils.dump_json(pageids, _file_names["pageids"])

    # Pages
    pages = []
    if wiki_ext.utils.exists_json(_file_names["pages"]):
        pages = wiki_ext.utils.load_json(_file_names["pages"])
    else:
        pages = wiki_ext.pages.extract(pageids)
        wiki_ext.utils.dump_json(pages, _file_names["pages"])

    # Images
    images = []
    if wiki_ext.utils.exists_json(_file_names["images"]):
        images = wiki_ext.utils.load_json(_file_names["images"])
    else:
        images = wiki_ext.images.extract(wiki_ext.pages.get_image_titles(pages))
        wiki_ext.utils.dump_json(images, _file_names["images"])
    
    # Download images
    wiki_ext.utils.download_images(images)

if __name__ == "__main__":
    main()

