"""
Created 8/7/2022 by goode_cheeseburgers.
"""
from twitchio.ext import commands


class SocialsCog(commands.Cog):
    """
    A Module containing Twitch channel social commands
    """

    def __init__(self, bot):
        self.bot = bot


def prepare(bot: commands.Bot) -> None:
    """
    Module is being loaded, prepare anything you need then add the cog.

    :param bot: The commands' bot instance
    :return: None
    """

    bot.add_cog(SocialsCog(bot))


def breakdown() -> None:
    """
    Called when the module is getting unloaded

    :return:
    """
