"""
Created 8/7/2022 by goode_cheeseburgers.
"""
import datetime

from twitchio.ext import commands, routines

from goode_bot_twitch.checks import author_is_in_channels
from goode_bot_twitch.cogs.utils.command_decorators import is_owner


class Cakez(commands.Cog):
    """
    A Cog for commands used in cakez77 stream.
    """

    def __init__(self, bot):
        self.bot = bot
        self.malding_counters = {"today": 0, "all_time": 0}

    @commands.command(name="_malding", aliases=["malding"])
    @is_owner
    async def _malding(self, ctx: commands.Context) -> None:
        """
        Increments and returns the times cakez77 has gotten angry on stream.

        :param ctx:
        :return: None
        """
        if await author_is_in_channels(ctx, ["cakez77", "goode_cheeseburgers"]):
            _today_count: int = self.malding_counters.get("today", 0) + 1
            _all_time_count: int = self.malding_counters.get("all_time", 0) + 1

            self.malding_counters["today"] = _today_count
            self.malding_counters["all_time"] = _all_time_count

            msg = (
                f"@cakez77 has malded {_today_count} times today. ({_all_time_count} "
                f"times since counting)"
            )

            if await self.bot.is_subscribed_to_channel(ctx.channel):
                await ctx.send(f"{msg} cakez7Rg")
            else:
                await ctx.send(msg)


def prepare(bot: commands.Bot) -> None:
    """
    Module is being loaded, prepare anything you need then add the cog.

    :param bot: The commands' bot instance.
    :return: None
    """
    cog = Cakez(bot)
    clear_daily_counters.start(cog.malding_counters)
    bot.add_cog(cog)


def breakdown() -> None:
    """
    Called when the module is getting unloaded.

    :return:
    """
    clear_daily_counters.stop()


@routines.routine(time=datetime.datetime(year=2022, month=7, day=1, hour=20, minute=44))
async def clear_daily_counters(counters: dict):
    """
    Clears the daily counters at a set time.

    :param counters:
    :return:
    """
    if counters.get("today"):
        print("clearing mald counter")
        counters["today"] = 0
