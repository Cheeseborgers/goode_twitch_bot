"""
Created 26/7/2022 by goode_cheeseburgers.
"""
import typing

from sqlalchemy import String, Column, Boolean, DateTime, func, select, delete
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.engine import ScalarResult
from sqlalchemy.exc import IntegrityError, NoResultFound, InvalidRequestError

from goode_bot_twitch.database import async_session
from goode_bot_twitch.logging_handler import get_logger
from goode_bot_twitch.models.abstract_base import AbstractBase
from goode_bot_twitch.models.errors import ModelNotFound, ModelAlreadyExists

logger = get_logger(__name__)


class TwitchChannel(AbstractBase):
    """
    TwitchChannel Model

    """

    __tablename__ = "twitch_channels"

    name = Column(String(36), nullable=False, unique=True)
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
        return self._repr(
            id=self.id,
            created_at=self.created_at,
            updated_at=self.updated_at,
            name=self.name,
            prefix=self.prefix,
            cmds_enabled=self.cmds_enabled,
            auto_join=self.auto_join,
            auto_thank=self.auto_thank,
            thanks_emotes=self.thanks_emotes,
            subgift_thanks_start_emote=self.subgift_thanks_start_emote,
            subgift_thanks_end_emote=self.subgift_thanks_end_emote,
            timezone=self.timezone,
            live=self.live,
            next_check=self.next_check,
        )

    def __str__(self):
        return self._str(
            id=self.id,
            created_at=self.created_at,
            updated_at=self.updated_at,
            name=self.name,
            prefix=self.prefix,
            cmds_enabled=self.cmds_enabled,
            auto_join=self.auto_join,
            auto_thank=self.auto_thank,
            thanks_emotes=self.thanks_emotes,
            subgift_thanks_start_emote=self.subgift_thanks_start_emote,
            subgift_thanks_end_emote=self.subgift_thanks_end_emote,
            timezone=self.timezone,
            live=self.live,
            next_check=self.next_check,
        )


async def add_channel(channel: TwitchChannel) -> None:
    """
    Adds a Single TwitchChannel to the database.

    Parameters
    ------------
    :param: channel: A TwitchChannel to add to the database
    :return: None

    :raise: ModelAlreadyExists: Raised if the channel already exists in the database.
    """
    try:
        async with async_session() as session:
            async with session.begin():
                session.add(channel)
                await session.commit()

    except IntegrityError as exc:
        raise ModelAlreadyExists(channel) from exc


async def add_channels(channels: typing.Union[list, tuple]) -> None:
    """
    Adds a list or tuple of TwitchChannels to the database.

    Parameters
    ------------
    :param: channels: A list or tuple of TwitchChannels to add to the database
    :return: None

    :raise: ModelAlreadyExists: Raised if the channel already exists in the database.
    """
    try:
        async with async_session() as session:
            async with session.begin():

                for channel in channels:
                    session.add(channel)

                await session.commit()

    except IntegrityError as exc:
        raise ModelAlreadyExists(channel) from exc


async def delete_channel(channel: TwitchChannel) -> None:
    """
    Deletes a Single TwitchChannel to the database.

    Parameters
    ------------
    :param: channel: A TwitchChannel to delete from the database
    :return: None

    :raise: ModelNotFound: Raised when the channel is not found in the database.
    """
    try:
        async with async_session() as session:
            async with session.begin():

                statement = (
                    delete(TwitchChannel)
                    .where(TwitchChannel.name == channel.name)
                    .execution_options(synchronize_session="fetch")
                )

                await session.execute(statement)

                await session.commit()

    except IntegrityError as exc:
        raise ModelNotFound(channel) from exc
    except InvalidRequestError as exc:
        raise ModelNotFound(channel) from exc


async def delete_channels(channels: typing.Union[list, tuple]) -> None:
    """
    Deletes a list or tuple of TwitchChannels to the database.

    Parameters
    ------------
    :param: channels: A list or tuple of TwitchChannels to delete from the database
    :return: None

    :raise: ModelNotFound: Raised when the channel is not found in the database.
    """
    try:
        async with async_session() as session:
            async with session.begin():

                for channel in channels:

                    statement = (
                        delete(TwitchChannel)
                        .where(TwitchChannel.name == channel.name)
                        .execution_options(synchronize_session="fetch")
                    )

                    await session.execute(statement)

                await session.commit()

    except IntegrityError as exc:
        raise ModelNotFound(channel) from exc
    except InvalidRequestError as exc:
        raise ModelNotFound(channel) from exc


async def get_channel(channel: TwitchChannel) -> TwitchChannel:
    """
    Fetches a TwitchChannel from database.

    Parameters
    ------------
    :param: channel: A TwitchChannel to fetch from the database.
    :return: TwitchChannel: The Twitch channel object returned from database.

    :raise: ModelNotFound: Raised when the channel is not found in the database.
    """
    try:
        async with async_session() as session:
            async with session.begin():
                # query from a class
                statement = select(TwitchChannel).filter_by(name=channel.name)

                # list of first element of each row (i.e. User objects)
                cursor = await session.execute(statement)

                # Return the TwitchChannel if found, raise if not.
                return cursor.scalars().one()

    except NoResultFound as exc:
        raise ModelNotFound(channel) from exc


async def get_channels() -> ScalarResult:
    """
    Fetches all TwitchChannels from database.

    parameters
    ----------
    :return: ScalarResult: The TwitchChannels
    """

    async with async_session() as session:
        async with session.begin():
            query = select(TwitchChannel)

            result = await session.execute(query)

            return result.scalars()
