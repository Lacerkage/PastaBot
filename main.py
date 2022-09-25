import os
import requests

from dotenv import load_dotenv
from src import Bot
from src import JSChan

from rich import print

load_dotenv()

if __name__ == "__main__":
    bot = Bot("https://pasta.wtf", os.getenv("ACCESS_TOKEN"))

    # DEVELOPMENT PURPOSES: Delete very post
    bot.purge()

    ptchan = JSChan("https://ptchan.org")

    # for thread in ptchan.get_overboard()["threads"][:1]:
    #     bot.post_thread(thread)

    thread = ptchan.get_thread("cyb", "8396")

    bot.post_thread(thread)
