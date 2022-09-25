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

    def get_overboard(self):
        res = requests.get(f"{self.base_url}/catalog.json")

        if not res.ok:
            res.raise_for_status()

        return res.json()["threads"]

    def get_thread(self, board, id):
        res = requests.get(f"{self.base_url}/{board}/thread/{id}.json")

        if not res.ok:
            res.raise_for_status()

        return res.json()
