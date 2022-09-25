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
    bot.update()
