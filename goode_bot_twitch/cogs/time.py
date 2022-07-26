"""
Created 8/7/2022 by goode_cheeseburgers.
"""
import datetime

import pytz

import dateutil.easter
from twitchio.ext import commands


class Time(commands.Cog):
    """
    A Cog containing commands related to time.

    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="christmas")
    async def days_to_christmas(self, ctx):
        """
        Returns the day until Christmas for the current year

        # Use streamer timezone if available
        """
        now = datetime.datetime.utcnow()
        christmas = datetime.datetime(now.year, 12, 25)
        if now > christmas:
            christmas = christmas.replace(year=christmas.year + 1)
            await ctx.send(f"{(christmas - now).days + 1} until Christmas!")

    @commands.command(name="easter")
    async def days_to_easter(self, ctx):
        """
        Returns the day until Easter for the current year (Western calendar)

        # Use streamer timezone if available
        """
        now = datetime.datetime.utcnow()
        easter = datetime.datetime.combine(
            dateutil.easter.easter(now.year, 3), datetime.time.min
        )
        if now > easter:
            easter = datetime.datetime.combine(
                dateutil.easter.easter(now.year + 1, 3), datetime.time.min
            )
            await ctx.send(f"{(easter - now).days + 1} days until Easter!")

    @commands.command(name="newyear")
    async def days_to_newyear(self, ctx):
        """
        Returns the day until the next new year from the current date

        # Use streamer timezone if available
        """
        now = datetime.datetime.utcnow()
        newyear = datetime.datetime(now.year, 1, 1).replace(year=now.year + 1)
        await ctx.send(f"{(newyear - now).days + 1} days until new years day!")

    @commands.command(name="_time", aliases=("time",))
    async def _time(self, ctx):
        """
        Returns the current time for the streamer/ channel

        """

        timezone = pytz.timezone(self.bot.channels.cache[ctx.channel.name].timezone)
        print(timezone)

        now = datetime.datetime.now(timezone)
        await ctx.send(
            f"It's {now.strftime((('%Y-%m-%d %H:%M:%S.%f')[: -3]))} for {ctx.channel.name}"
        )


def prepare(bot: commands.Bot) -> None:
    """
    Module is being loaded, prepare anything you need then add the cog.

    :param bot: The commands' bot instance.
    :return: None
    """
    bot.add_cog(Time(bot))


def breakdown() -> None:
    """
    Called when the module is getting unloaded.

    :return:
    """
