"""
Created 8/7/2022 by goode_cheeseburgers.
"""
import random

from twitchio.ext import commands


class Basic(commands.Cog):
    """
    A Cog containing basic commands.

    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="_hello", aliases=("hello",))
    async def _hello(self, ctx: commands.Context) -> None:
        """
        Simply responds back to the sender with hello message.

        Parameters
        ------------
        @param: ctx: commands.Context
        :return: None
        """
        await ctx.send(f"Hello @{ctx.author.name}!")

    @commands.command(name="_rate", aliases=("rate",))
    async def _rate(self, ctx: commands.Context, name: str = None):
        """
        Rates A user by name out of 10.

        Parameters
        ------------
        @param: ctx: commands.Context
        @param: name: The users name to rate (If None, the ctx authors name is used)
        :return: None
        """
        if not name:
            name = ctx.author.name

        await ctx.channel.send(
            f"I rate @{name} a solid {str(random.randint(1, 10))}/10"
        )

    @commands.command(name="_lurk", aliases=("lurk",))
    async def _lurk(self, ctx: commands.Context):
        """
        Posts a message to chat that the author is leaving chat/ lurking.

        Parameters
        ------------
        @param: ctx: commands.Context
        :return: None
        """

        await ctx.channel.send(f"{ctx.author.name} is lurking")

    @commands.command(name="_unlurk", aliases=("unlurk",))
    async def _unlurk(self, ctx: commands.Context):
        """
        Posts a message to chat that the author is back in chat/ unlurking.

        Parameters
        ------------
        @param: ctx: commands.Context
        :return: None
        """

        await ctx.channel.send(f"{ctx.author.name} is back from lurking")


def prepare(bot: commands.Bot) -> None:
    """
    Module is being loaded, prepare anything you need then add the cog.

    Parameters
    ------------
    @param: bot: The commands' bot instance.
    :return: None
    """
    bot.add_cog(Basic(bot))


def breakdown() -> None:
    """
    Called when the module is getting unloaded.

    Parameters
    ------------
    :return:
    """
