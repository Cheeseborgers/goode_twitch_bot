"""
Created 13/7/2022 by goode_cheeseburgers.
"""
import typing
from dataclasses import dataclass

# pylint: disable-all


@dataclass
class TwitchChannel:
    """
    A Dataclass to hold information about a twitch channel
    """

    __slots__ = [
        "channel_name",
        "prefix",
        "cmds_enabled_users",
        "auto_join",
        "auto_thank",
        "thanks_emotes",
        "time_zone",
    ]

    channel_name: str
    prefix: str
    cmds_enabled_users: bool
    auto_join: bool
    auto_thank: bool
    thanks_emotes: list
    time_zone: str


class TwitchChannelModel:
    """
    Handles all functionality for a twitch channels
    """

    @classmethod
    async def add_channel(cls, twitch_channel: TwitchChannel):
        """

        :param twitch_channel:
        :return:
        """
        print("")

    @classmethod
    async def remove_channel(cls, twitch_channel: TwitchChannel):
        """

        :param twitch_channel:
        :return:
        """
        print("")

    @classmethod
    async def get_channel(cls, channel_name: str):
        """

        :param channel_name:
        :return:
        """
        print("")

    @classmethod
    async def add_channels(
        cls,
        twitch_channels: typing.Union[
            typing.List[TwitchChannel], typing.Tuple[TwitchChannel]
        ],
    ):
        """

        :param twitch_channels:
        :return:
        """
        print("")

    @classmethod
    async def remove_channels(
        cls,
        twitch_channels: typing.Union[
            typing.List[TwitchChannel], typing.Tuple[TwitchChannel]
        ],
    ):
        """

        :param twitch_channels:
        :return:
        """
        print("")

    @classmethod
    async def get_channels(
        cls, channel_names: typing.Union[typing.List, typing.Tuple] = None
    ):
        """

        :param channel_names:
        :return:
        """
        print("")

    @staticmethod
    async def create_table():
        """

        :return:
        """
        # query =
        # await execute()
        print("")
