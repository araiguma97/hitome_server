import sqlite3
from abc import ABCMeta, abstractmethod

_DATABASE_NAME = "wiki.db"

class Repository(metaclass=ABCMeta):
    def __init__(self) -> None:
        self._conn = sqlite3.connect(_DATABASE_NAME)
        self._create_daos()

    @abstractmethod
    def _create_daos(self) -> None:
        pass

    def close(self) -> None:
        self._conn.close()
