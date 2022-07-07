"""
Created 7/7/2022 by goode_cheeseburgers.
"""
from dotenv import load_dotenv
from goode_bot_twitch.bot import Bot


load_dotenv()

bot = Bot()


if __name__ == "__main__":
    bot.run()
