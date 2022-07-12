"""
Created 8/7/2022 by goode_cheeseburgers.
"""
from twitchio.ext import commands


class Search(commands.Cog):
    """
    A Cog to generate search links for various search engines/ websites/ services.

    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def google(self, ctx, *search) -> None:
        """
        Generates a Google search link.

        :param ctx:
        :param search: The search term.
        :return: None
        """
        await ctx.send("https://google.com/search?q=" + "+".join(search))

    @commands.command()
    async def imfeelinglucky(self, ctx, *search) -> None:
        """
        Generates a Google 'im feeling lucky' search link.

        :param ctx:
        :param search: The search term.
        :return: None
        """
        await ctx.send("https://google.com/search?btnI&q=" + "+".join(search))

    @commands.command()
    async def lmgtfy(self, ctx, *search) -> None:
        """
        Generates a lmgtfy link.

        :param ctx:
        :param search: The search term.
        :return: None
        """
        await ctx.send("https://lmgtfy.com/?q=" + "+".join(search))

    @commands.command(aliases=("wiki",))
    async def wikipedia(self, ctx, *search) -> None:
        """
        Generates a wikipedia link.

        :param ctx:
        :param search: The search term.
        :return: None
        """
        await ctx.send("https://wikipedia.org/wiki/" + "_".join(search))


def prepare(bot: commands.Bot) -> None:
    """
    Module is being loaded, prepare anything you need then add the cog.

    :param bot: The commands' bot instance.
    :return: None
    """
    bot.add_cog(Search(bot))


def breakdown() -> None:
    """
    Called when the module is getting unloaded.

    :return:
    """
