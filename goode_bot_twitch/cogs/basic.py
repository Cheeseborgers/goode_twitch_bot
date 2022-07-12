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

        :param ctx: commands.Context
        :return: None
        """
        await ctx.send(f"Hello @{ctx.author.name}!")

    @commands.command(name="_rate", aliases=("rate",))
    async def _rate(self, ctx: commands.Context, name: str = None):
        """
        Rates A user by name out of 10, if no name is present the sender is rated.

        :param ctx: commands.Context
        :param name:
        :return: None
        """
        if not name:
            name = ctx.author.name

        await ctx.channel.send(
            f"I rate @{name} a solid {str(random.randint(1, 10))}/10"
        )


def prepare(bot: commands.Bot) -> None:
    """
    Module is being loaded, prepare anything you need then add the cog.

    :param bot: The commands' bot instance.
    :return: None
    """
    bot.add_cog(Basic(bot))


def breakdown() -> None:
    """
    Called when the module is getting unloaded.

    :return:
    """
