"""
Created 27/7/2022 by goode_cheeseburgers.
"""
import typing

from sqlalchemy import String, Column
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.engine import ScalarResult


from goode_bot_twitch.logging_handler import get_logger
from goode_bot_twitch.models.abstract_base import AbstractBase
from goode_bot_twitch.models.base_model_functions import (
    add_model,
    add_models,
    delete_model,
    get_model,
    delete_models,
    get_models,
)


logger = get_logger(__name__)


class TwitchBotUser(AbstractBase):
    """
    TwitchChannel Model

    """

    __tablename__ = "twitch_bot_user_accounts"

    email = Column(String(320))
    password_hash = Column(String(100), nullable=False)
    roles = Column(ARRAY(item_type=String(10)))

    def __repr__(self):
        return self._repr()

    def __str__(self):
        return self._str()

    def __init__(self, name, email, password_hash, roles):
        self.name = name
        self.email = email
        self.password_hash = password_hash
        self.roles = roles

        super().__init__()


async def add_user(user: TwitchBotUser) -> None:
    """
    Adds a Single TwitchBotUser to the database.

    Parameters
    ------------
    @param: user: A TwitchBotUser to add to the database
    :return: None
    """
    await add_model(user)


async def add_users(users: typing.Union[list, tuple]) -> None:
    """
    Adds a list or tuple of TwitchBotUsers to the database.

    Parameters
    ------------
    @param: users: A list or tuple of TwitchBotUsers to add to the database
    :return: None
    """
    await add_models(users)


async def delete_user(user: TwitchBotUser) -> None:
    """
    Deletes a Single TwitchBotUser to the database.

    Parameters
    ------------
    @param: user: A TwitchBotUser to delete from the database
    :return: None
    """
    await delete_model(user)


async def delete_users(users: typing.Union[list, tuple]) -> None:
    """
    Deletes a list or tuple of TwitchBotUser to the database.

    Parameters
    ------------
    @param: users: A list or tuple of TwitchBotUser to delete from the database
    :return: None
    """
    await delete_models(users)


async def get_user(user: TwitchBotUser) -> TwitchBotUser:
    """
    Fetches a TwitchBotUser from database.

    Parameters
    ------------
    @param: model: A TwitchBotUser to fetch from the database.
    :return: TwitchBotUser: The Twitch bot user object returned from database.
    """
    return await get_model(user)


async def get_users() -> ScalarResult:
    """
    Fetches all TwitchChannels from database.

    parameters
    ----------
    :return: ScalarResult: The TwitchChannels
    """

    return await get_models(TwitchBotUser)
