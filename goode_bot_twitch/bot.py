"""
Created 7/7/2022 by goode_cheeseburgers
"""

from twitchio.ext import commands

from goode_bot_twitch.logging_handler import get_bot_logger

logger = get_bot_logger(__name__)


class Bot(commands.Bot):
    """
    The Twitch bot
    """

    def __init__(self):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        # prefix can be a callable, which returns a list of strings or a string...
        # initial_channels can also be a callable which returns a list of strings...
        super().__init__(
            token="oauth:zqi522brtfga3wwpc2c6682sph8szv",
            prefix="?",
            initial_channels=["goode_cheeseburgers"],
        )

    async def event_ready(self):
        # Notify us when everything is ready!
        # We are logged in and ready to chat and use commands...
        logger.info("Logged in as %s", self.nick)
        logger.info("User id is %s", self.user_id)

    async def event_message(self, message):
        # Messages with echo set to True are messages sent by the bot...
        # For now, we just want to ignore them...
        if message.echo:
            return

        # Print the contents of our message to console...
        print(message.content)

        # Since we have commands and are overriding the default `event_message`
        # We must let the bot know we want to handle and invoke our commands...
        await self.handle_commands(message)

    @commands.command()
    async def hello(self, ctx: commands.Context):
        """
        :param ctx:
        :return:
        """
        await ctx.send(f"Hello {ctx.author.name}!")
