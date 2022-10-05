import datetime
import os
import requests


class Bot:
    def __init__(self, pleroma, jschan, allowed_boards=None, on_publish=None):
        self.jschan = jschan
        self.pleroma = pleroma

        self.allowed_boards = allowed_boards
        self.on_publish = on_publish

        # Tries to load last update
        self.last_update = None
        if os.path.isfile("last_update.txt"):
            with open("last_update.txt", "r") as f:
                self.last_update = datetime.datetime.strptime(f.read(), "%Y-%m-%dT%H:%M:%S.%fZ")

    def post_thread(self, thread):
        post_id = thread['postId']
        board_uri = thread["board"]
        subject = thread["subject"] or "Fio"
        message = thread["message"].replace("\n", "  \n")  # Add two spaces for Markdown parsing
        sensitive = thread["spoiler"]

        # TODO board list only returns listed boards, an expection is thrown if a unlisted board
        #  is provided in the whitelist... which is a problem. See how can we deal with this in a sensible manner

        # Check if board is NSFW
        # boards = self.imageboard.get_board_list()["boards"]
        # board = list(filter(lambda x: x["_id"] == board_uri, boards))[0]
        # if not board["settings"]["sfw"]:
        # sensitive = True

        body = f"**{subject}:** [/{board_uri}/{post_id}]({self.jschan.base_url}/{board_uri}/thread/{post_id}.html)  \n\n"
        body += message

        media = []
        # Retrieve thread files
        for file in thread["files"]:
            res = requests.get(f"{self.jschan.base_url}/file/{file['filename']}")
            # Skips file if something happened
            if not res.ok:
                continue
            media.append(res.content)

        status_id = self.pleroma.post_status(body, sensitive=sensitive, media=media)
        print(f"Post /{board_uri}/{post_id} made with success, id:{status_id}")

        self.on_publish(post_id, board_uri, status_id)

    def update(self):
        threads = self.jschan.get_overboard_catalog(boards=self.allowed_boards)

        for thread in threads:
            thread_date = datetime.datetime.strptime(thread["date"], "%Y-%m-%dT%H:%M:%S.%fZ")

            if self.last_update and thread_date > self.last_update:
                try:
                    print(thread)
                    self.post_thread(thread)
                    print(f"Thread {thread['board']}/{thread['postId']} uploaded")

                except Exception as e:
                    print(e)

        self.last_update = datetime.datetime.now()

        with open("last_update.txt", "w") as f:
            f.write(self.last_update.strftime("%Y-%m-%dT%H:%M:%S.%fZ"))

    def purge(self, num_posts=-1):
        statuses = self.pleroma.get_statuses()

        for status in statuses[:num_posts]:
            self.pleroma.delete_status(status["id"])

        if len(statuses) == 0:
            print("No posts were deleted.")
