import os
import requests

from dotenv import load_dotenv
from src import Bot
from src import JSChan

from rich import print
from time import sleep

load_dotenv()

if __name__ == "__main__":
    bot = Bot("https://pasta.wtf", os.getenv("ACCESS_TOKEN"))

    # DEVELOPMENT PURPOSES: Delete very post
    bot.purge()

    while True:
        print("Updating...")
        
        bot.update()

        print("Update finished.")

        sleep(60)
