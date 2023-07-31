from contextlib import closing

from categories.categories_repository import CategoriesRepository
from pages.pages_repository import PagesRepository
from images.images_repository import ImagesRepository


def main():
    with closing(TourismInfoRetriever()) as tourism_info_retriever:
        tourism_info_retriever.retrieve()

class TourismInfoRetriever:
    def __init__(self) -> None:
        self._categories_repository = CategoriesRepository()
        self._pages_repository      = PagesRepository()
        self._images_repository     = ImagesRepository()

    def close(self) -> None:
        self._categories_repository.close()
        self._pages_repository.close()
        self._images_repository.close()

    def retrieve(self) -> None:
        self._categories_repository.update()
        self._pages_repository.update()
        self._images_repository.update()


if __name__ == "__main__":
    main()
