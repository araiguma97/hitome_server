from contextlib import closing

import repository
import utils

def main():
    root_category = {
        "category_id": 1609621,
        "title": "Category:島根県の観光地",
    }

    # Categories
    #with closing(repository.CategoriesRepository()) as categories_repository:
        #categories_repository.update(root_category)

    # Category pages
    #with closing(repository.CategoryPagesRepository()) as category_pages_repository:
        #category_pages_repository.update()

    # Pages
    #with closing(repository.PagesRepository()) as pages_repository:
        #pages_repository.update()

    # Images
    with closing(repository.ImagesRepository()) as images_repository:
        #images_repository.update()
        images_repository.download()

if __name__ == "__main__":
    main()

