"""
Created 26/7/2022 by goode_cheeseburgers.
"""
import datetime
import os
import typing

from sqlalchemy import String, Column, Boolean, DateTime, func
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.engine import ScalarResult

from goode_bot_twitch.logging_handler import get_logger
from goode_bot_twitch.models.abstract_base import AbstractBase
from goode_bot_twitch.models.base_model_functions import (
    add_model,
    add_models,
    delete_model,
    delete_models,
    get_model,
    get_models,
)

logger = get_logger(__name__)


class TwitchChannel(AbstractBase):
    """
    TwitchChannel Model

    """

    # pylint: disable=too-many-instance-attributes
    __tablename__ = "twitch_channels"

    prefix = Column(String(3))
    cmds_enabled = Column(Boolean, nullable=False)
    auto_join = Column(Boolean, nullable=False)
    auto_thank = Column(Boolean, nullable=False)
    thanks_emotes = Column(ARRAY(item_type=String))
    subgift_thanks_start_emote = Column(String(20))
    subgift_thanks_end_emote = Column(String(20))
    timezone = Column(String(20), nullable=False)
    live = Column(Boolean, nullable=False)
    next_check = Column(DateTime, server_default=func.now())

    def __repr__(self):
        return self._repr()

    def __str__(self):
        return self._str()

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        name,
        prefix,
        cmds_enabled=False,
        auto_join=False,
        auto_thank=False,
        thanks_emotes=None,
        subgift_thanks_start_emote=None,
        subgift_thanks_end_emote=None,
        timezone=None,
    ):
        self.name = name
        self.prefix = prefix
        self.cmds_enabled = cmds_enabled
        self.auto_join = auto_join
        self.auto_thank = auto_thank
        self.thanks_emotes = thanks_emotes or list(str)
        self.subgift_thanks_start_emote = subgift_thanks_start_emote or ""
        self.subgift_thanks_end_emote = subgift_thanks_end_emote or ""
        self.timezone = timezone or os.environ.get("OWNER_TIME_ZONE")
        self.live = False
        self.next_check = datetime.datetime.now()


async def add_channel(channel: TwitchChannel) -> None:
    """
    Adds a Single TwitchChannel to the database.

    Parameters
    ------------
    @param: model: A TwitchChannel to add to the database
    :return: None
    """
    await add_model(channel)


async def add_channels(channels: typing.Union[list, tuple]) -> None:
    """
    Adds a list or tuple of TwitchChannels to the database.

    Parameters
    ------------
    @param: users: A list or tuple of TwitchChannels to add to the database
    :return: None
    """
    await add_models(channels)


async def delete_channel(channel: TwitchChannel) -> None:
    """
    Deletes a Single TwitchChannel to the database.

    Parameters
    ------------
    @param: model: A TwitchChannel to delete from the database
    :return: None
    """
    await delete_model(channel)


async def delete_channels(channels: typing.Union[list, tuple]) -> None:
    """
    Deletes a list or tuple of TwitchChannels to the database.

    Parameters
    ------------
    @param: users: A list or tuple of TwitchChannels to delete from the database
    :return: None
    """
    await delete_models(channels)


async def get_channel(channel: TwitchChannel) -> TwitchChannel:
    """
    Fetches a TwitchChannel from database.

    Parameters
    ------------
    @param: model: A TwitchChannel to fetch from the database.
    :return: TwitchChannel: The Twitch model object returned from database.
    """
    return await get_model(channel)


async def get_channels() -> ScalarResult:
    """
    Fetches all TwitchChannels from database.

    parameters
    ----------
    :return: ScalarResult: The TwitchChannels
    """
    return await get_models(TwitchChannel)
