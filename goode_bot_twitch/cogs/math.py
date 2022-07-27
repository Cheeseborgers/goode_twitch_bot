"""
Created 8/7/2022 by goode_cheeseburgers.
"""
from twitchio.ext import commands


class Math(commands.Cog):
    """
    A Cog with commands related to math.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="_add", aliases=("add",))
    async def _add(self, ctx: commands.Context, left: int, right: int) -> None:
        """
        Adds two numbers

        Parameters
        ------------
        @param: ctx: commands.Context
        @param: left: The first number to add.
        @param: right: The second number to add.
        :return: None
        """
        await ctx.send(left + right)

    @commands.command(name="_pi", aliases=("pi",))
    async def _pi(self, ctx: commands.Context) -> None:
        """
        Returns the value of pi to 499 digits if mod, 3 if not.

        Parameters
        ------------
        @param: ctx: commands.Context
        :return: None
        """
        if ctx.message.author.is_mod:
            await ctx.send(
                """3.14159265358979323846264338327950288419716939937510582097494459230781
                6406286208998628034825342117067982148086513282306647093844609550582231
                7253594081284811174502841027019385211055596446229489549303819644288109
                7566593344612847564823378678316527120190914564856692346034861045432664
                8213393607260249141273724587006606315588174881520920962829254091715364
                3678925903600113305305488204665213841469519415116094330572703657595919
                5309218611738193261179310511854807446237996274956735188575272489122793
                8183011949"""
            )
        else:
            await ctx.send("3.14")


def prepare(bot: commands.Bot) -> None:
    """
    Module is being loaded, prepare anything you need then add the cog.

    Parameters
    ------------
    @param: bot: The commands' bot instance.
    :return: None
    """
    bot.add_cog(Math(bot))


def breakdown() -> None:
    """
    Called when the module is getting unloaded.

    Parameters
    ------------
    :return: None
    """
