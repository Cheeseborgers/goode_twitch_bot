"""
Created 8/7/2022 by goode_cheeseburgers.
"""
import functools
from typing import Union

from twitchio.ext import commands

from goode_bot_twitch.checks import (
    author_is_owner,
    author_is_mod,
    author_is_sub,
    author_is_in_channels,
)


def is_owner(func):
    """

    :param func:
    :return:
    """

    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        context: commands.Context = args[1]
        if await author_is_owner(context):
            await func(*args, **kwargs)

    return wrapper


def is_mod(func):
    """

    :param func:
    :return:
    """

    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        context: commands.Context = args[1]
        if await author_is_mod(context):
            return await func(*args, **kwargs)

    return wrapper


def is_sub(func):
    """

    :param func:
    :return:
    """

    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        context: commands.Context = args[1]
        if await author_is_sub(context):
            return await func(*args, **kwargs)

    return wrapper


def is_in_channels(channels: Union[list, tuple]):
    """

    :param channels:
    :return:
    """

    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            context: commands.Context = args[1]
            if await author_is_in_channels(context, channels):
                return await func(*args, **kwargs)

        return wrapper

    return decorator
