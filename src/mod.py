from datetime import date, datetime, timedelta
from threading import Thread, Event, Lock
import os
import json

from src.jschan import JSChan
from src.pleroma import Pleroma


class Mod(Thread):
    def __init__(self, imageboard: JSChan, social: Pleroma, fetch_interval: int = 10):
        Thread.__init__(self)
        self.daemon = True
        self.__stp = Event()  # __stop is reserved or something

        self.imageboard = imageboard
        self.pleroma = social

        self.fetch_interval = fetch_interval

        self.watchlist_lock = Lock()
        # Tries to load posted status
        self.watchlist = dict()
        if os.path.isfile("watchlist.json"):
            with open("watchlist.json", "r") as f:
                self.watchlist = json.load(f)

        self.logs = dict()

        # Tries to load the date of the last fetch
        self.last_watched = None
        if os.path.isfile("watch_day.txt"):  # TODO change this silly name
            with open("watch_day.txt", "r") as f:
                self.last_watched = datetime.strptime(f.read(), "%Y-%m-%d")
        else:
            self.last_watched = date.today() - timedelta(days=15)  # TODO change this interval to be configurable

    @staticmethod
    def __split_date(d: date) -> (int, int, int):
        return d.day, d.month, d.year

    @staticmethod
    def __parse_log_entries(entries: list) -> dict:
        return {date(*entry["date"].values()): entry["count"] for entry in entries}

    def __has_logs(self, board: str, d: date) -> bool:
        # Lazely fetches logs for new boards
        if board not in self.logs.keys():
            self.logs[board] = self.__parse_log_entries(self.imageboard.get_board_log_count(board))
        # Current day is always subject to changes, we must try to update the last entry before answering
        elif d is date.today() and d not in self.logs[board].keys():
            last = self.imageboard.get_board_log_count(board)[0]
            last_date = date(*last["date"])
            if last_date not in self.logs.keys():
                self.logs[last_date] = last["count"]

        return d in self.logs[board].keys()

    def stop(self):
        self.__stp.set()

    def watch(self, post_id, board_uri, status_id):
        with self.watchlist_lock:
            if board_uri not in self.watchlist.keys():
                self.watchlist[board_uri] = dict()
            self.watchlist[board_uri][post_id] = status_id

        # TODO update the watchlist.txt

    def run(self):
        while True:
            # Check new logs of each board that has at least one entry in the watchlist
            # TODO move this lock to somewhere more sensible, this whole operation takes a lot of time
            with self.watchlist_lock:
                for board in self.watchlist.keys():
                    while self.last_watched <= date.today():

                        if self.__has_logs(board, self.last_watched):
                            entries = self.imageboard.get_board_log_day(board, *self.__split_date(self.last_watched))
                            # TODO do somethintg after filtering, probably we can do something smart and
                            #  check only the last entries with the last_watch

                    self.last_watched += timedelta(days=1)
                    # TODO update the watch_day.txt and watchlist.txt

                # TODO check and clean the watchlist to keep the posts fresh

            if self.__stp.wait(self.fetch_interval):
                break
