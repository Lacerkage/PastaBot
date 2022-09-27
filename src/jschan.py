import requests

from rich import print


class JSChan():
    def __init__(self, base_url):
        self.base_url = base_url

    def get_board_catalog(self, board):
        res = requests.get(f"{self.base_url}/{board}/catalog.json")

        if not res.ok:
            res.raise_for_status()

        return res.json()

    def get_overboard_catalog(self, boards=None):
        catalog_url = f"{self.base_url}/catalog.json?include_default=false&add={','.join(boards)}" if boards \
            else f"{self.base_url}/catalog.json"

        res = requests.get(catalog_url)
        if not res.ok:
            res.raise_for_status()

        return res.json()["threads"]

    def get_thread(self, board, id):
        res = requests.get(f"{self.base_url}/{board}/thread/{id}.json")

        if not res.ok:
            res.raise_for_status()

        return res.json()
