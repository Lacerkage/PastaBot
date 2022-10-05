import os
import sys

from dotenv import load_dotenv

from rich import print
from time import sleep

from src.bot import Bot
from src.jschan import JSChan
from src.mod import Mod
from src.pleroma import Pleroma

load_dotenv(".env.development")


def new_post_handler(post_id, board_uri, status_id):
    mod.watch(post_id, board_uri, status_id)


jschan = JSChan(os.getenv("JSCHAN_WEBSITE"))
pleroma = Pleroma(os.getenv("FEDIVERSE_INSTANCE"), os.getenv("ACCESS_TOKEN"), os.getenv("ACCOUNT_ID"))

bot = Bot(pleroma, jschan,
          allowed_boards=os.getenv("BOARDS_WHITELIST").split() if "BOARDS_WHITELIST" in os.environ else None,
          on_publish=new_post_handler)
mod = Mod(jschan, pleroma)

if __name__ == "__main__":
    mod.start()

    if sys.argv[1] == "--purge":
        num_posts = int(sys.argv[2]) if len(sys.argv) > 2 else -1

        bot.purge(num_posts)

    elif sys.argv[1] == "--start":
        while True:
            print("Updating...")

            bot.update()

            print("Update finished.")

            sleep(int(os.getenv("UPDATE_INTERVAL")))

    elif sys.argv[1] == "--post":
        thread_board = str(sys.argv[2])
        thread_id = str(sys.argv[3])
        bot.post_thread(jschan.get_thread(thread_board, thread_id))

    else:
        print("Usage: python main.py [--purge <num_posts>] [--start] [--post <board> <id>]")
