"""
Created 8/7/2022 by goode_cheeseburgers.
"""
import os
import typing

import twitchio
from twitchio.ext import commands


async def author_is_mod(ctx: commands.Context) -> bool:
    """
    Returns whether the context author is mod or not.

    @param: ctx:
    :return: bool
    """
    return ctx.author.is_mod


async def author_is_sub(ctx: commands.Context) -> bool:
    """
    Returns whether the context author is subscribed or not.

    @param: ctx:
    :return: bool
    """
    return ctx.author.is_subscriber


async def author_is_owner(ctx: commands.Context) -> bool:
    """
    Returns whether the context author is bot owner_channel_name or not.
    This is compared to the 'OWNER_ID' set in the bots .env file.

    @param: ctx:
    :return: bool
    """
    return ctx.author.id == os.environ.get("OWNER_ID")


async def author_is_in_channels(
    ctx: commands.Context, channels: typing.Union[typing.List, typing.Tuple]
) -> bool:
    """
    Returns whether the context author is certain model or not.

    @param: ctx:
    @param: channels:
    :return: bool
    """
    return ctx.channel.name in channels


async def event_is_in_channels(
    channel_name: twitchio.Channel.name,
    channels: typing.Union[typing.List, typing.Tuple],
) -> bool:
    """
    Returns whether an event originated in the listed users.

    @param: channel_name:
    @param: channels:
    :return: bool
    """
    return channel_name in channels
