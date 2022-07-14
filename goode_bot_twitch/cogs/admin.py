"""
Created 8/7/2022 by goode_cheeseburgers.
"""
from twitchio.ext import commands

from goode_bot_twitch.checks import author_is_owner


class AdminCommandsCog(commands.Cog):
    """
    A Cog Containing all bot owner_name/ admin commands
    """

    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx: commands.Context) -> bool:
        """
        A Cog wide check to determine if the context author is the bot owner_name
        before running any commands.

        Parameters
        ------------
        :param ctx: commands.Context
        :return: bool: Whether the author is the bot owner_name or not.
        """
        return await author_is_owner(ctx)

    @commands.command(name="_join", aliases=("join",))
    async def _join(self, ctx: commands.Context, channel_name: str) -> None:
        """
        Joins a channel/ stream by channel name.

        Parameters
        ------------
        :param ctx: commands.Context
        :param channel_name: The name of the channel to join.
        :return: None
        """
        await ctx.send(f"'{channel_name}' joined")

    @commands.command(name="_leave", aliases=("leave",))
    async def _leave(self, ctx: commands.Context, channel_name: str) -> None:
        """
        Leaves a channel/ stream by channel name.

        Parameters
        ------------
        :param ctx: commands.Context
        :param channel_name: The name of the channel to leave.
        :return: None
        """
        await ctx.send(f"'{channel_name}' left")

    @commands.command(name="_unload", aliases=("unload",))
    async def _unload(self, ctx: commands.Context, module: str) -> None:
        """
        Unloads a module and it's cogs.

        Parameters
        ------------
        :param ctx: commands.Context
        :param module: The name of the module to unload in dot.path format.
        :return: None
        """
        try:
            self.bot.unload_module(module)
        except ValueError as error:
            await ctx.send(f"Could not unload '{module}'. Check log for details")
            self.bot.logger.error("Could not unload module: %s", error)
        else:
            await ctx.send(f"'{module}' unloaded")

    @commands.command(name="_load", aliases=("load",))
    async def _load(self, ctx: commands.Context, module: str) -> None:
        """
        Loads a module and it's cogs.

        Parameters
        ------------
        :param ctx: commands.Context
        :param module: The name of the module to unload in dot.path format.
        :return: None
        """
        try:
            self.bot.load_module(module)
        except ValueError as error:
            await ctx.send(f"'{module}' is already loaded")
            self.bot.logger.error("'%s' is already loaded: %s", module, error)
        except ImportError as error:
            await ctx.send(f"Could not load '{module}'. Check console for details")
            self.bot.logger.error("Module <%s> is missing a prepare method", error)
        else:
            await ctx.send(f"'{module}' loaded")

    @commands.command(name="_reload", aliases=("reload",))
    async def _reload(self, ctx: commands.Context, module) -> None:
        """
        Reloads a module and it's cogs.

        Parameters
        ------------
        :param ctx: commands.Context
        :param module: The name of the module to unload in dot.path format.
        :return: None
        """
        try:
            self.bot.unload_module(module)
            self.bot.load_module(module)
        except ValueError as error:
            await ctx.send(f"'{module}' is not loaded")
            self.bot.logger.error("'%s' is not loaded: %s", module, error)
        else:
            await ctx.send(f"'{module}' reloaded")

    async def add_channel(self) -> None:
        """
        Adds a channel to the ....

        :return None:
        """


def prepare(bot: commands.Bot) -> None:
    """
    Module is being loaded, prepare anything you need then add the cog.

    :param bot: The commands' bot instance.
    :return: None
    """
    bot.add_cog(AdminCommandsCog(bot))


def breakdown() -> None:
    """
    Called when the module is getting unloaded.

    :return:
    """
