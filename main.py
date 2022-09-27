import os
import sys

from dotenv import load_dotenv
from src import Bot
from src import JSChan

from rich import print
from time import sleep

load_dotenv()

if __name__ == "__main__":
    if "BOARDS_WHITELIST" in os.environ:  # checks if whitelist exists
        bot = Bot(os.getenv("FEDIVERSE_INSTANCE"), os.getenv("ACCESS_TOKEN"),
                  allowed_boards=os.getenv("BOARDS_WHITELIST").split())
    else:
        bot = Bot(os.getenv("FEDIVERSE_INSTANCE"), os.getenv("ACCESS_TOKEN"))

    ptchan = JSChan(os.getenv("JSCHAN_WEBSITE"))

    if sys.argv[1] == "--purge":
        bot.purge()

    elif sys.argv[1] == "--update":
        while True:
            print("Updating...")

            bot.update()

            print("Update finished.")

            sleep(os.getenv("UPDATE_INTERVAL"))

    elif sys.argv[1] == "--post":
        thread_board = sys.argv[2]
        thread_id = sys.argv[3]

        thread = ptchan.get_thread(thread_board, thread_id)

        bot.post_thread(thread)

    else:
        print("Usage: python main.py [--purge] [--update] [--post <board> <id>]")
