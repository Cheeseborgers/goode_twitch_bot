"""
Created 17/7/2022 by goode_cheeseburgers.
"""

import os
import typing

from goode_bot_twitch.errors import OwnerNotFound, ChannelNotFound
from goode_bot_twitch.models.twitch_channel import TwitchChannel, get_channels


class ChannelCache:
    """
    Channel cache (Update this docstring)
    """

    def __init__(self):

        self._cache: typing.Dict = {}

    async def load_cache(self) -> None:
        """
        Loads the users into the model cache.

        Parameters
        ----------
        :return: None

        :raise OwnerNotFound: Raised if owners model now found in the cache.
        :raise ChannelNotFound: Raised if no users are found in the cache.
        """

        # Fetch the users from the database.
        channels = await get_channels()

        # Load the users into the users cache.
        self._cache = {channel.name: channel for channel in channels}

        # Check the model cache has items in it.
        if self._cache:

            # Check that the owners model is present in the cache / database
            if self._cache.get(os.environ.get("OWNER_CHANNEL_NAME")):
                return

            raise OwnerNotFound

        raise ChannelNotFound

    async def update(self, channel_name: str, channel: TwitchChannel):
        """
        Updates a Channel in the model cache, Adds a new one if it does not exist.

        :return: None
        """
        self._cache[channel_name] = channel

    async def remove(self, channel_name: str) -> None:
        """
        Removes a model from the cache if exists.

        :return: None
        """
        if self._cache.get(channel_name, None):
            del self._cache[channel_name]
        else:
            raise ChannelNotFound

    @property
    def cache(self) -> dict:
        """
        Returns the caches' dict instance

        :return: dict: the caches' dict instance (self._cache).
        """
        return self._cache
