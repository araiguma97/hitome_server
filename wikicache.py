from contextlib import closing

import repository

def main():
    root_category = {
        "category_id": 1609593,
        "title": "Category:群馬県の観光地",
    }

    """
    with closing(repository.CategoriesRepository()) as categories_repository:
        categories_repository.update(root_category)

    with closing(repository.CategoryPagesRepository()) as category_pages_repository:
        category_pages_repository.update()
    """

    with closing(repository.PagesRepository()) as pages_repository:
        pages_repository.update()

    """
    with closing(repository.ImageRepository()) as images_repository:
        images_repository.update()
        images_repository.download()
    """

if __name__ == "__main__":
    main()

