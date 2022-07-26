"""
Created 8/7/2022 by goode_cheeseburgers.
"""
from twitchio.ext import commands

from goode_bot_twitch.checks import author_is_in_channels
from goode_bot_twitch.cogs.utils.command_decorators import is_owner


class Cakez(commands.Cog):
    """
    A Cog for commands used in cakez77 stream.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="_malding", aliases=["malding"])
    @is_owner
    async def _malding(self, ctx: commands.Context) -> None:
        """
        Increments and returns the times cakez77 has gotten angry on stream.

        Parameters
        ------------
        :param ctx: commands.Context
        :return: None
        """
        if await author_is_in_channels(ctx, ["cakez77", "goode_cheeseburgers"]):

            print(self.bot.recurrent_counters)

            _today_count: int = (
                self.bot.recurrent_counters.cache("cakez77")
                .cache("malding")
                .cache("today", 0)
                + 1
            )
            _all_time_count: int = (
                self.bot.recurrent_counters.cache("cakez77")
                .cache("malding")
                .cache("all_time", 0)
                + 1
            )

            self.bot.recurrent_counters["cakez77"]["malding"]["today"] = _today_count
            self.bot.recurrent_counters["cakez77"]["malding"][
                "all_time"
            ] = _all_time_count

            msg = (
                f"@cakez77 has malded {_today_count} times today. ({_all_time_count} "
                f"times since counting)"
            )

            if await self.bot.is_subscribed_to_channel(ctx.channel):
                await ctx.send(f"{msg} cakez7Rg")
            else:
                await ctx.send(msg)

    def init_counters(self):
        """
        Initializes all counters for this cog
        :return:
        """
        self.bot.recurrent_counters["cakez77"] = {}
        self.bot.recurrent_counters["cakez77"]["malding"] = {"today": 0, "all_time": 0}

        print(self.bot.recurrent_counters)


def prepare(bot: commands.Bot) -> None:
    """
    Module is being loaded, prepare anything you need then add the cog.

    Parameters
    ------------
    :param bot: The commands' bot instance.
    :return: None
    """
    cog = Cakez(bot)
    # cog.init_counters()
    bot.add_cog(cog)


def breakdown() -> None:
    """
    Called when the module is getting unloaded.

    Parameters
    ------------
    :return: None
    """
