"""
Created 8/7/2022 by goode_cheeseburgers.
"""
import twitchio
from twitchio.ext import commands

from goode_bot_twitch.checks import author_is_mod


class ModCommandsCog(commands.Cog):
    """
    A Module containing Twitch channel mod only commands
    """

    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx: commands.Context):
        """
        A Cog wide check to determine if the context author is a channel moderator
        before running any commands.

        :param ctx: commands.Context
        :return: bool: Whether the author is a channel moderator or not.
        """
        return await author_is_mod(ctx)

    @commands.command(aliases=["to"])
    async def timeout(
        self,
        ctx: commands.Context,
        user: twitchio.User,
        duration: str,
        *,
        reason: str = "",
    ) -> None:
        """
        !timeout (!to) command
        """

        if reason != "":
            await ctx.send(f"/timeout {user.name} {duration} {reason}")
        else:
            await ctx.send(f"/timeout {user.name} {duration}")

    @commands.command()
    async def ban(
        self, ctx: commands.Context, user: twitchio.User, *, reason: str = ""
    ) -> None:
        """
        !ban command
        """

        if reason != "":
            await ctx.send(f"/ban {user.name} {reason}")
        else:
            await ctx.send(f"/ban {user.name}")

    @commands.command()
    async def unban(self, ctx: commands.Context, user: twitchio.User) -> None:
        """
        !unban command
        """

        await ctx.send(f"/unban {user.name}")

    @commands.command(name="_getid", aliases=("getid",))
    async def _getid(self, ctx, username: str = None):
        """

        :param ctx: commands.Context
        :param username:
        :return:
        """

        if not username:
            username = ctx.author.name

        users = await self.bot.fetch_users(names=username)

        print(type(users))

        if len(users) == 0:
            await ctx.send(
                f"@{ctx.author.name}, no users found with username '{username}'"
            )
        else:
            user = users[0]
            await ctx.send(f"@{ctx.author.name}, ID = {user.id}!")


def prepare(bot: commands.Bot) -> None:
    """
    Module is being loaded, prepare anything you need then add the cog.

    :param bot: The commands' bot instance
    :return: None
    """

    bot.add_cog(ModCommandsCog(bot))


def breakdown() -> None:
    """
    Called when the module is getting unloaded

    :return:
    """
