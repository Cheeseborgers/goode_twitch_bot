"""
Created 8/7/2022 by goode_cheeseburgers.
"""
import os
import textwrap

from twitchio.ext import commands

from goode_bot_twitch.utils import make_request


class Words(commands.Cog):
    """
    A Cog with commands relating to words.

    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="randomword")
    async def randomword(self, ctx: commands.Context):
        """

        See https://www.wordnik.com/users/goode/API

        @param: ctx:
        :return:
        """

        url = "http://api.wordnik.com:80/v4/words.json/randomWord"
        params = {
            "hasDictionaryDef": "false",
            "minCorpusCount": 0,
            "maxCorpusCount": -1,
            "minDictionaryCount": 1,
            "maxDictionaryCount": -1,
            "minLength": 5,
            "maxLength": -1,
            "api_key": os.environ.get("WORKNIK_API_KEY"),
        }

        data = await make_request(url, params)

        if not data or not data.get("word"):
            return await ctx.send("No results found.")

        await ctx.send(data["word"].capitalize())

    @commands.command(aliases=("urband", "urban"))
    async def urbandictionary(self, ctx: commands.Context, word):
        """

        @param: ctx:
        @param: word:
        :return:
        """
        url = "http://api.urbandictionary.com/v0/define"
        params = {"term": word}

        data = await make_request(url, params)

        if not data or not data.get("list"):
            return await ctx.send("No results found.")

        definition = data["list"][0]
        message = textwrap.shorten(
            f"{definition['word']}: {definition['definition']}",
            width=500 - len(definition["permalink"]) - 1,
            placeholder="...",
        )

        await ctx.send(f"{message} {definition['permalink']}")


def prepare(bot: commands.Bot) -> None:
    """
    Module is being loaded, prepare anything you need then add the cog.

    @param: bot: The commands' bot instance.
    :return: None
    """
    bot.add_cog(Words(bot))


def breakdown() -> None:
    """
    Called when the module is getting unloaded.

    :return:
    """
