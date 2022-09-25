import datetime
import requests

from .pleroma import Pleroma
from .jschan import JSChan

ptchan = JSChan("https://ptchan.org")


class Bot(Pleroma):
    def __init__(self, instance_url, access_token):
        Pleroma.__init__(self, instance_url, access_token)

        self.last_update = None

    def _post_thread(self, thread):
        post_id = thread['postId']
        board = thread["board"]
        subject = thread["subject"] or "Fio"
        message = thread["message"].replace("\n", "  \n")  # Add two spaces for Markdown parsing
        sensitive = thread["spoiler"]

        body = f"**{subject}:** [/{board}/{post_id}](https://ptchan.org/{board}/thread/{post_id}.html)  \n\n{message}"

        media = []

        for file in thread["files"]:
            response = requests.get(f"https://ptchan.org/file/{file['filename']}")
            data = response.content

            media.append(data)

        self.post_status(body, sensitive=sensitive, media=media)

    def update(self):
        threads = ptchan.get_overboard()

        for thread in threads:      
            thread_date = datetime.datetime.strptime(thread["date"], "%Y-%m-%dT%H:%M:%S.%fZ")

            if self.last_update == None or thread_date > self.last_update:
                self._post_thread(thread)
