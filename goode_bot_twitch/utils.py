"""
Created 8/7/2022 by goode_cheeseburgers.
"""
import asyncio

import aiohttp


def initdb():
    """
    Command line function to initialize the database

    :returns: None
    """
    asyncio.get_event_loop().run_until_complete(_initdb())


async def _initdb():
    """
    Create an empty database, Adds the admin user

    :return: None
    """
    print("Database initialized")


async def make_request(url, params=None) -> dict:
    """
    Make an http request to the given url.

    :param url: The request url
    :param params: Any request params
    :return: dict
    """
    if params is None:
        params = {}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            if resp.status == 200:
                data = await resp.json()
            else:
                data = None

        return data
