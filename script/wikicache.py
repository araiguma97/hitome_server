import dao
import repository
import utils

def main():
    root_category = {
        "category_id": 1609621,
        "title": "Category:島根県の観光地",
    }

    # Categories
    with dao.CategoriesDAO() as categories_dao:
        categories_repository = repository.CategoriesRepository(categories_dao)
        #categories_repository.update(root_category)
        category_ids = categories_repository.read_category_ids()

    # Category pages
    with dao.CategoryPagesDAO() as category_pages_dao:
        category_pages_repository = repository.CategoryPagesRepository(category_pages_dao)
        #category_pages_repository.update(category_ids)
        page_ids = category_pages_repository.read_page_ids()

    # Pages
    with dao.PagesDAO() as pages_dao:
        pages_repository = repository.PagesRepository(pages_dao)
        #pages_repository.update(page_ids)
        image_titles = pages_repository.read_image_titles()

    # Images
    with dao.ImagesDAO() as images_dao:
        images_repository = repository.ImageRepository(images_dao)
        #images_repository.update(image_titles)
        images = images_repository.read_images()

    utils.download_images(images)

if __name__ == "__main__":
    main()

