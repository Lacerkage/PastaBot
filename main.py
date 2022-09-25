import os
import requests

from dotenv import load_dotenv
from bot.jschan import JSChan
from bot.pleroma import Pleroma

from rich import print

load_dotenv()

pleroma = Pleroma("https://pasta.wtf", os.getenv("ACCESS_TOKEN"))

def post_thread(thread):
    post_id = thread['postId']
    board = thread["board"]
    message = thread["message"]

    body = f"[/{board}/{post_id}](https://ptchan.org/{board}/thread/{post_id}.html)  \n\n{message}"

    media = []

    for file in thread["files"]:
        response = requests.get(f"https://ptchan.org/file/{file['filename']}")
        data = response.content

        media.append(data)

    pleroma.post_status(body, sensitive=True    , media=media)


if __name__ == "__main__":
    # DEVELOPMENT PURPOSES: Delete very post 
    pleroma.purge()

    ptchan = JSChan("https://ptchan.org")

    for thread in ptchan.get_overboard()["threads"][:1]:
        post_thread(thread)
