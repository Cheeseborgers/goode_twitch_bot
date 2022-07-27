"""
Created 7/7/2022 by goode_cheeseburgers.
"""
import asyncio
import copy
import datetime
import os
import typing
from asyncio import sleep
from random import randint

import pytz
import twitchio
from twitchio.ext import commands, routines

from goode_bot_twitch.channel_cache import ChannelCache
from goode_bot_twitch.checks import event_is_in_channels
from goode_bot_twitch.cogs.utils.thankyou_message import (
    create_thank_you_message,
)
from goode_bot_twitch.errors import OwnerNotFound, ChannelNotFound
from utilities.time import seconds_to_hms


class TwitchBot(commands.Bot):
    """
    The Twitch bot
    """

    def __init__(self, channels: ChannelCache, logger):

        self.channels = channels
        self.logger = logger

        self.owner_channel_name = os.environ.get("OWNER_CHANNEL_NAME")
        self.rate_limits = {}
        self.rate_limit_max = int(os.environ.get("CHANNEL_RATE_LIMIT_MAX"))
        self.message_counters = {}
        self.recurrent_counters = {}

        super().__init__(
            token=os.environ.get("TWITCH_OAUTH_TOKEN"),
            prefix=self.get_bot_prefixes(),
            initial_channels=[self.owner_channel_name],
            heartbeat=int(os.environ.get("TWITCH_HEARTBEAT_INTERVAL")),
            loop=asyncio.get_event_loop(),
        )

        # disable linting on this as it's a twitchio routine, and we have
        # no control of this other than its functionality.
        # pylint: disable=no-member
        self.clear_rate_limits.start()
        self.clear_recurrent_counters.start()
        self.update_live_channels.start()
        self.post_socials.start()

    def load_modules(self) -> None:
        """
        Loads the Initial cogs/ extensions.

        Parameters
        ------------
        :return: None
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
            self.logger.info("Loaded the following cogs: %s", [*self.cogs])

    async def join_initial_channels(self) -> None:
        """
        Joins initial channels on starting the bot.

        Parameters
        ------------
        :return: None
        """

        initial_channels = []
        for channel_name, channel in self.channels.cache.items():
            if channel_name != self.owner_channel_name:
                if channel.auto_join:
                    initial_channels.append(channel_name)

        # Join the list of channels
        await self.join_channels(channels=initial_channels)

    async def event_ready(self) -> None:
        """
        Event called when the TwitchBot has logged in and is ready.

        Parameters
        ------------
        :return: None
        """

        # Load the Channel data from the database into the cache.
        try:
            await self.channels.load_cache()
            # TESTING
            # chan = TwitchChannel("test_channel", "?", False, False, False, [], "", "")
            # await delete_channel(chan)

        except ChannelNotFound:
            self.logger.error("No users found in the cache.")
        except OwnerNotFound:
            self.logger.error("Owner not found in model cache.")

        # Create the recurrent and message counters.
        await self.create_channel_counters()

        # Join the channels from the channel cache.
        await self.join_initial_channels()

        self.logger.info(
            "Twitch client connected, Logged in as %s - %s", self.nick, self.user_id
        )

        # Send bot login message to the bot owners channel?
        if os.environ.get("SEND_TWITCH_LOGIN_MESSAGE"):
            owner_channel: twitchio.Channel = self.get_channel(self.owner_channel_name)
            await owner_channel.send(os.environ.get("TWITCH_LOGIN_MESSAGE"))

    async def event_channel_joined(self, channel: twitchio.Channel) -> None:
        """
        Event called when the TwitchBot joins a channel.

        Parameters
        ------------
        @param: channel: The channel the bot joined
        :return: None
        """
        self.rate_limits[channel.name] = self.rate_limits.get(channel.name, 0)
        self.logger.info("Joined channel: %s", channel.name)

    async def event_command_error(self, context, error: Exception) -> None:
        self.logger.error("Error in context: %s, error: %s", context, error)

    async def event_message(self, message: twitchio.Message) -> None:
        """
        Event called when a PRIVMSG is received from Twitch.

        Parameters
        ------------
        @param: message (Message) – Message object containing relevant information.
        :return: None
        """
        if message.echo:  # Ignore any 'echoed' messages.
            return

        # Check this channel is in the channel cache
        if message.channel.name in self.channels.cache:

            # Increment the channels message count.
            self.message_counters[message.channel.name] = (
                self.message_counters[message.channel.name] + 1
            )

            # Check this channel has commands enabled or is rather
            # the owner_channel_name, streamer or mod
            if (
                self.channels.cache[message.channel.name].cmds_enabled
                or message.author.name == self.owner_channel_name
                or message.author.is_broadcaster
                or message.author.is_mod
            ):

                # Get the channels prefix if any
                channel_prefix = self.channels.cache[message.channel.name].prefix

                # If we have a prefix, check if the message contents starts with the
                # channels prefix.
                if channel_prefix:
                    if message.content.startswith(channel_prefix):
                        # Handle the command.
                        await self.handle_commands(message)
                else:
                    self.logger.info("s% has no prefix", message.channel)

    async def event_raw_data(self, data: str) -> None:
        """
        Event called with the raw data received by Twitch.

        Parameters
        ------------
        @param: data: The raw data received from Twitch.
        :return: None
        """
        # self.logger.debug("Twitch message: %s", data)
        return

    async def event_raw_usernotice(
        self, channel: twitchio.Channel, tags: typing.Dict
    ) -> None:
        """
        Event called when a USERNOTICE is received from Twitch.

        Parameters
        ------------
        @param: channel: The TwitchIO Channel object
        @param: tags: A dict of tags associated with the event
        :return: None
        """

        if await event_is_in_channels(channel.name, ("jonbams", "cakez77")):

            if tags["msg-id"] == "announcement":
                return

            if (
                tags["msg-id"] == "submysterygift"
                or tags["msg-id"] == "subgift"
                or tags["msg-id"] == "resub"
                or tags["msg-id"] == "sub"
            ):

                # Check if the bot is subbed to the channel.
                is_subbed = await self.is_subscribed_to_channel(channel)

                if is_subbed:
                    # Check that the channels rate is less than 5, log and return if not.
                    if self.rate_limits.get(channel.name) >= self.rate_limit_max:
                        self.logger.debug("Rate limit exceeded!!")
                        return

                    # Increase the channels rate_limit by 1
                    self.rate_limits[channel.name] = (
                        self.rate_limits.get(channel.name) + 1
                    )

                    message = await create_thank_you_message(
                        self, channel_name=channel.name, tags=tags
                    )

                    if message:
                        # Sleep for a random time between 9 and 16 seconds
                        # to prevent immediate sending of the message.
                        sleep_time = randint(9, 16)
                        self.logger.debug("Sleeping %s seconds...", sleep_time)
                        await sleep(sleep_time)

                        # Send the thankyou message
                        self.logger.debug("Sending thankyou message: %s", message)
                        await channel.send(message)

                    else:
                        self.logger.debug("Thankyou message creation error.")
                else:
                    self.logger.debug("Not subbed to model: %s", channel.name)

            elif tags["msg-id"] == "bitsbadgetier":
                self.logger.debug(
                    "Bitsbadgetier - Name: %s, Bits threshold: %s",
                    tags["display-name"],
                    tags["msg-param-threshold"],
                )

            elif tags["msg-id"] == "raid":
                self.logger.debug("Raid - tags: %s", tags)

            return

    async def create_channel_counters(self) -> None:
        """
        Creates any counters for the channels

        :return: None
        """
        for channel in self.channels.cache:
            self.recurrent_counters[channel] = {}
            self.message_counters[channel] = 0

    def get_bot_prefixes(self) -> list:
        """
        All callable Prefixes for our bot.
        NOTE: This can change as channels are added/ removed.

        Parameters
        ------------
        :return: list:
        """
        prefixes = [os.environ.get("OWNER_CHANNEL_PREFIX")]

        for channel in self.channels.cache.values():
            if channel.prefix and channel.prefix not in prefixes:
                prefixes.append(channel.prefix)

        return prefixes

    async def leave_channels(
        self, channels: typing.Union[typing.List[str], typing.Tuple[str]]
    ) -> None:
        """
        Removes any rate limits and parts bot from the listed channels.

        Parameters
        ------------
        @param: channels: A List or Tuple of channels to leave by channel name.
        :return: None
        """
        for channel_name in channels:
            self.logger("Leaving model %s and deleting it's rate_limits")
            self.rate_limits.pop(self.rate_limits.get(channel_name))

        await self.part_channels(channels=channels)

    async def is_subscribed_to_channel(self, channel: twitchio.Channel) -> bool:
        """
        Checks if the bot is subscribed to the channel in an Event.

        Parameters
        ------------
        @param: channel: The channel to check.
        :return: True if subscribed, False if not.
        """
        user = channel.get_chatter(name=self.owner_channel_name)

        if user:
            if user.is_subscriber:
                return True

        return False

    async def fetch_live_channels(self, channels: typing.List) -> list:
        """
        Fetches all live channels in the channel cache and returns
        the live channel names in a list.


        -----------
        @param: users: A list of channel names to check.
        :return: list: A list of live channel
        """

        # Split the list into lists of channel names, max 99 per list.
        split_channel_lists = [
            channels[x : x + 99] for x in range(0, len(channels), 99)
        ]

        # Maintain a list of the currently live channels.
        live_channels = []

        # Iterate the lists.
        for channel_list in split_channel_lists:

            # Fetch the live streams.
            response = await self.fetch_streams(user_logins=channel_list)

            # Iterate the live channels
            for channel in response:
                # Fetch the twitchio.User for the twitchio.PartialUser
                user = await channel.user.fetch()

                # Append it to the live channels list.
                live_channels.append(user.name)

        return live_channels

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

    @routines.routine(seconds=60)
    async def update_live_channels(self) -> None:
        """
        A routine to get and update current live channels.

        Parameters
        ------------
        :return: None
        """

        # Create a list of channel names form the channel cache dict keys.
        channels = [*self.channels.cache]

        # Fetch any live channels
        live_channels = await self.fetch_live_channels(channels=channels)

        for channel_name in channels:
            if channel_name not in live_channels:
                # Mark the channel not live and next check time to None.
                self.channels.cache[channel_name].live = False
                self.channels.cache[channel_name].next_check = None
            else:
                # Mark the channel as live.
                self.channels.cache[channel_name].live = True

    @routines.routine(seconds=30, wait_first=True)
    async def post_socials(self) -> None:
        """
        A routine to post social updates to a channel

        Parameters
        ------------
        :return: None
        """

        # Create a deep copy of the message counters
        message_counter_copy = copy.deepcopy(self.message_counters)

        # Set all values of the message counter to zero.
        new_message_counters = {item: 0 for item in message_counter_copy.keys()}

        # Set the bots message counters to the new/ reset message counters.
        self.message_counters = new_message_counters

    @routines.routine(hours=1)
    async def clear_recurrent_counters(self) -> None:
        """
        Runs hourly and clears the recurrent counters at midnight
        dependent on channels' timezone.

        Parameters
        ------------
        :return: None
        """

        for channel_name in self.recurrent_counters:

            timezone = pytz.timezone(self.channels.cache[channel_name].timezone)

            now = datetime.datetime.now(timezone)

            seconds_since_midnight = (
                now - now.replace(hour=0, minute=0, second=0, microsecond=0)
            ).total_seconds()

            hours_mins_secs = await seconds_to_hms(seconds_since_midnight)

            print(
                f"Seconds since midnight for {channel_name}: "
                f"{seconds_since_midnight} : "
                f"({hours_mins_secs[0]}:{hours_mins_secs[1]}:{hours_mins_secs[2]})"
            )

            if 0 <= seconds_since_midnight <= 3540:  # 3540 = 59 minutes in seconds
                print("Doing the thing")
