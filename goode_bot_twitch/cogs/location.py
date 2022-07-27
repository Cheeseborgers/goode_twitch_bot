"""
Created 8/7/2022 by goode_cheeseburgers.
"""
from twitchio.ext import commands


class Location(commands.Cog):
    """
    A Cog containing commands related to location.

    """

    def __init__(self, bot):
        self.bot = bot


def prepare(bot: commands.Bot) -> None:
    """
    Module is being loaded, prepare anything you need then add the cog.

    Parameters
    ------------
    @param: bot: The commands' bot instance.
    :return: None
    """
    bot.add_cog(Location(bot))


def breakdown() -> None:
    """
    Called when the module is getting unloaded.

    Parameters
    ------------
    :return: None
    """
