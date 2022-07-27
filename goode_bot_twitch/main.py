"""
Created 7/7/2022 by goode_cheeseburgers.
"""
import sys

from dotenv import load_dotenv

from goode_bot_twitch.twitch_bot import TwitchBot
from goode_bot_twitch.channel_cache import ChannelCache
from goode_bot_twitch.logging_handler import get_logger
from goode_bot_twitch.webserver.webserver import WebServer

load_dotenv()

logger = get_logger(__name__)

# Create a cache for the users.
channels = ChannelCache()

# Create the Twitch bot instance
bot = TwitchBot(channels=channels, logger=logger)

# Create the webserver instance
webserver = WebServer(channels=channels, logger=logger, import_name=__name__)


def main() -> None:
    """
    Main application
    :return: None
    """
    args = sys.argv[1:]
    args_length = len(args)

    if args_length != 0:
        # add ability to init database etc...
        if args[0] is None:
            print("dave")
    else:
        try:
            bot.load_modules()
            bot.loop.create_task(webserver.run_task())
            bot.run()
        except KeyboardInterrupt:
            logger.error("Keyboard interrupt")


if __name__ == "__main__":
    main()
