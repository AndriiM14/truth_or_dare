from python_core.consts import SCRAPER_UUID_PATH, DB_URL_PATH


def get_scrpaer_uuid() -> str:
    with open(SCRAPER_UUID_PATH, "r") as uuid:
        return uuid.readline().strip("\n")


def get_firebasedb_url() -> str:
    with open(DB_URL_PATH, "r") as db_url:
        return db_url.readline().strip("\n")


class SingletonMeta(type):
    _instances = {}

    def __call__(self, *args, **kwargs):
        if self not in self._instances:
            self._instances[self] = super().__call__(*args, **kwargs)
        return self._instances[self]
