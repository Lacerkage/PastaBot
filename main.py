import os
import sys

from dotenv import load_dotenv
from src import Bot
from src import JSChan

from rich import print
from time import sleep

load_dotenv(".env.development")

jschan_website = JSChan(os.getenv("JSCHAN_WEBSITE"))

if __name__ == "__main__":
    bot = Bot(
        os.getenv("FEDIVERSE_INSTANCE"),
        os.getenv("ACCESS_TOKEN"),
        os.getenv("ACCOUNT_ID"),
        os.getenv("JSCHAN_WEBSITE"),
        allowed_boards=os.getenv("BOARDS_WHITELIST").split() if "BOARDS_WHITELIST" in os.environ else None
    )

    imageboard = JSChan(os.getenv("JSCHAN_WEBSITE"))

    if sys.argv[1] == "--purge":
        num_posts = int(sys.argv[2]) if len(sys.argv) > 2 else -1

        bot.purge(num_posts)

    elif sys.argv[1] == "--update":
        while True:
            print("Updating...")

            bot.update()

            print("Update finished.")

            sleep(int(os.getenv("UPDATE_INTERVAL")))

    elif sys.argv[1] == "--post":
        thread_board = sys.argv[2]
        thread_id = sys.argv[3]

        thread = imageboard.get_thread(thread_board, thread_id)

        bot.post_thread(thread)

    else:
        print("Usage: python main.py [--purge <num_posts>] [--update] [--post <board> <id>]")
