"""
Created 8/7/2022 by goode_cheeseburgers.
"""

import json

import aiofiles
import aiohttp


async def make_request(url, params=None) -> dict:
    """
    Make an http request to the given url.

    @param: url: The request url
    @param: params: Any request params
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


async def load_json(filepath: str) -> dict:
    """
    Loads json from a file a returns the data as a python dictionary.

    @param: filepath: The filepath to the json file.
    :return:
    """
    async with aiofiles.open(filepath, mode="r", encoding="utf-8") as file:
        contents = await file.read()
        return json.loads(contents)


async def write_json(filepath: str, data: dict):
    """
    Writes json from a dict to a file.

    @param: filepath:
    @param: data:
    :return:
    """
    async with aiofiles.open(filepath, mode="w", encoding="utf-8") as file:
        await file.write(json.dumps(data, indent=3))
