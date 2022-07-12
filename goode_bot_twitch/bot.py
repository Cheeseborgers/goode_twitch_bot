"""
Created 7/7/2022 by goode_cheeseburgers.
"""
import asyncio
import json
import os
from typing import List, Union, Tuple

import aiofiles
import twitchio
from twitchio.ext import commands, routines

from goode_bot_twitch.checks import event_is_in_channels
from goode_bot_twitch.cogs.utils.thankyou_message import (
    create_raw_thank_you_message,
)
from goode_bot_twitch.database import Database
from goode_bot_twitch.logging_handler import get_bot_logger


class Bot(commands.Bot):
    """
    The Twitch bot
    """

    def __init__(self):

        self.database = Database()

        super().__init__(
            token=os.environ.get("OAUTH_TOKEN"),
            prefix=os.environ.get("PREFIX"),
            initial_channels=[os.environ.get("OWNER_NAME")],
            loop=asyncio.get_event_loop(),
        )

        self.logger = get_bot_logger(__name__)

        self.rate_limits = {}  # Sort this to handle all channels
        self.char_limit = 500  # limits the character posted to twitch
        self.channels = {}

    def load_modules(self):
        """

        :return:
        """
        initial_extensions = [
            "cogs.admin",
            "cogs.mod",
            "cogs.basic",
            "cogs.math",
            "cogs.random",
            "cogs.words",
            "cogs.units",
            "cogs.location",
            "cogs.search",
            "cogs.time",
            "cogs.twitch",
            "cogs.cakez",
        ]
        try:
            for extension in initial_extensions:
                self.load_module(extension)
        except ModuleNotFoundError as error:
            self.logger.exception("Error loading cog: %s", error)
        else:
            self.logger.debug("Loaded the following cogs: %s", [*self.cogs])

    async def join_initial_channels(self) -> None:
        """

        Parameters
        ------------
        :return: None
        """

        # Use the resource thingy here!
        async with aiofiles.open("channels.json", mode="r", encoding="UTF-8") as file:
            channels = await file.read()

        self.channels = json.loads(channels)

        initial_channels = []

        for channel, channel_metadata in self.channels.items():
            if channel_metadata.get("auto_join"):
                initial_channels.append(channel)

        await self.join_channels(channels=initial_channels)

    async def event_ready(self) -> None:
        """
        Event called when the Bot has logged in and is ready.

        Parameters
        ------------
        :return: None
        """
        await self.join_initial_channels()

        self.logger.info("Logged in as %s", self.nick)
        self.logger.info("User id is %s", self.user_id)

        # pylint: disable=no-member
        self.clear_rate_limits.start()

        owner_channel: twitchio.Channel = self.get_channel(os.environ.get("OWNER_NAME"))
        await owner_channel.send(os.environ.get("LOGIN_MESSAGE"))

    async def event_channel_joined(self, channel: twitchio.Channel) -> None:
        """
        Event called when the Bot joins a channel.

        Parameters
        ------------
        :param channel: The channel the bot joined
        :return: None
        """
        self.rate_limits[channel.name] = self.rate_limits.get(channel.name, 0)
        self.logger.debug("Joined channel: %s", channel.name)

    async def event_message(self, message: twitchio.Message) -> None:
        """
        Event called when a PRIVMSG is received from Twitch.

        Parameters
        ------------
        :param message (Message) – Message object containing relevant information.
        :return: None
        """
        if message.echo:  # Ignores any 'echoed' messages and processes commands.
            return

        await self.get_prefixes()  # <- fix this trash

        if message.channel.name in self.channels:
            channel_prefix = self.channels[message.channel.name].get("prefix", None)
            if message.content.startswith((channel_prefix,)):
                print(channel_prefix)

        await self.handle_commands(message)

    async def event_raw_data(self, data: str) -> None:
        """
        Event called with the raw data received by Twitch.

        Parameters
        ------------
        :param data: The raw data received from Twitch.
        :return: None
        """
        # self.logger.debug("Twitch message: %s", data)
        return

    async def event_raw_usernotice(self, channel: twitchio.Channel, tags: dict) -> None:

        """
        Event called when a USERNOTICE is received from Twitch.

        Parameters
        ------------
        :param channel: The TwitchIO Channel object
        :param tags: A dict of tags associated with the event
        :return: None
        """
        if await event_is_in_channels(channel.name, ("jonbams", "cakez77")):
            is_subbed = await self.is_subscribed_to_channel(channel)

            if is_subbed:
                msg = await create_raw_thank_you_message(
                    self, channel_name=channel.name, tags=tags
                )
                if msg:
                    await channel.send(msg)
            else:
                self.logger.debug("Not subbed to channel: %s", channel.name)

    async def get_prefixes(self):
        """
        All callable Prefixes for our bot.

        Parameters
        ------------
        :return: str:
        """
        prefixes = [os.environ.get("PREFIX")]

        for channel_data in self.channels.values():
            prefix = channel_data.get("prefix")
            if prefix and prefix not in prefixes:
                prefixes.append(prefix)

        return prefixes

    async def leave_channels(self, channels: Union[List[str], Tuple[str]]) -> None:
        """
        Removes any rate limits and parts bot from the listed channels.

        Parameters
        ------------
        :param channels: A List or Tuple of channels to leave by channel name.
        :return: None
        """
        for channel_name in channels:
            self.logger("Leaving channel %s and deleting it's rate_limits")
            self.rate_limits.pop(self.rate_limits.get(channel_name))

        await self.part_channels(channels=channels)

    async def is_subscribed_to_channel(self, channel: twitchio.Channel) -> bool:
        """
        Checks if the bot is subscribed to the channel in an Event.

        Parameters
        ------------
        :param channel: The channel to check.
        :return: True if subscribed, False if not.
        """
        user = channel.get_chatter(self.nick)
        if user:
            if user.is_subscriber:
                return True

        return False

    @routines.routine(seconds=20)
    async def clear_rate_limits(self) -> None:
        """
        A routine to clear rate limits every 20 secs

        Parameters
        ------------
        :return: None
        """
        for key, value in self.rate_limits.items():
            if value > 0:
                self.logger.debug(
                    "Resetting %s rate limit: %s in 20 seconds.",
                    key,
                    value,
                )
                self.rate_limits[key] = 0
