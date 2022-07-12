"""
Created 7/7/2022 by goode_cheeseburgers.
"""
import sys

from dotenv import load_dotenv
from goode_bot_twitch.bot import Bot

load_dotenv()

bot = Bot()


def main() -> None:
    """
    Main application
    :return: None
    """
    args = sys.argv[1:]
    args_length = len(args)

    if args_length != 0:
        # add ability to init database etc...
        if args[0] == "-c":
            if args[1] == "initdb":
                print("initdb")
            else:
                print("No command specified")
    else:
        try:
            bot.load_modules()
            bot.run()
        except KeyboardInterrupt as error:
            print(error)


if __name__ == "__main__":
    main()
