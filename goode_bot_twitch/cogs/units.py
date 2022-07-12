"""
Created 8/7/2022 by goode_cheeseburgers.
"""
from twitchio.ext import commands


class Units(commands.Cog):
    """
    A Cog containing all commands related to units and conversion.

    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ctof")
    async def celsius_to_fahrenheit(self, ctx, celsius: str = None) -> None:
        """
        Converts

        :param ctx:
        :param celsius:
        :return: None
        """
        if not celsius:
            celsius = 1
        await ctx.send(f"{celsius} °C = {int(celsius) * 9 / 5 + 32} °F")

    @commands.command(name="ftoc")
    async def fahrenheit_to_celsius(self, ctx, fahrenheit: str = None) -> None:
        """
        Converts

        :param ctx:
        :param fahrenheit:
        :return: None
        """
        if not fahrenheit:
            fahrenheit = 1
        await ctx.send(f"{fahrenheit} °F = {(int(fahrenheit) - 32) * 5 / 9} °C")

    @commands.command(name="lbtokg")
    async def lb_to_kg(self, ctx, pounds: str = None) -> None:
        """
        Converts

        :param ctx:
        :param pounds:
        :return: None
        """
        if not pounds:
            pounds = 1
        await ctx.send(f"{pounds} lb = {int(pounds) * 0.45359237} kg")

    @commands.command(name="kgtolb")
    async def kg_to_lb(self, ctx, kilos: str = None) -> None:
        """
        Converts

        :param ctx:
        :param kilos:
        :return: None
        """
        if not kilos:
            kilos = 1
        await ctx.send(f"{kilos} kg = {int(kilos) * 2.2046} lb")

    @commands.command(name="fttom")
    async def feet_to_metres(self, ctx, feet: str = None) -> None:
        """
        Converts

        :param ctx:
        :param feet:
        :return: None
        """
        if not feet:
            feet = 1
        await ctx.send(f"{feet} ft = {int(feet) * 0.3048} m")

    @commands.command(name="mtoft")
    async def metres_to_feet(self, ctx, metres: str = None) -> None:
        """
        Converts

        :param ctx:
        :param metres:
        :return: None
        """
        if not metres:
            metres = 1
        await ctx.send(f"{metres} m = {int(metres) * 3.2808} ft")

    @commands.command(name="fitom")
    async def feet_and_inches_to_metres(
        self, ctx, feet: str = None, inches: str = None
    ) -> None:
        """
        Converts

        :param ctx:
        :param feet:
        :param inches:
        :return: None
        """
        if not feet:
            feet = 1
        if not inches:
            inches = 0

        await ctx.send(
            f"{feet} ft {inches} in = {(int(feet) + int(inches) / 12) * 0.3048} m"
        )

    @commands.command(name="mtofi")
    async def metres_to_feet_and_inches(self, ctx, metres: str = None) -> None:
        """
        Converts

        :param ctx:
        :param metres:
        :return: None
        """

        if not metres:
            metres = 1

        await ctx.send(
            f"{metres} m = {int(metres) * 39.37 // 12} ft "
            f"{int(metres) * 39.37 - (int(metres) * 39.37 // 12) * 12} in"
        )

    @commands.command(name="gtooz")
    async def grams_to_oz(self, ctx, grams: str = None) -> None:
        """
        Converts

        :param ctx:
        :param grams:
        :return: None
        """
        if not grams:
            grams = 1
        await ctx.send(f"{grams} g = {int(grams) * 0.035274} ounces")

    @commands.command(name="oztog")
    async def oz_to_grams(self, ctx, ounces: str = None) -> None:
        """
        Converts

        :param ctx:
        :param ounces:
        :return: None
        """
        if not ounces:
            ounces = 1
        await ctx.send(f"{ounces} ounces = {int(ounces) / 0.035274} g")

    @commands.command(name="mitokm")
    async def miles_to_km(self, ctx, miles: str = None) -> None:
        """
        Converts

        :param ctx:
        :param miles:
        :return: None
        """
        if not miles:
            miles = 1
        await ctx.send(f"{miles} mi = {int(miles) / 0.62137} kilometres")

    @commands.command(name="kmtomi")
    async def km_to_miles(self, ctx, kilometres: str = None) -> None:
        """
        Converts

        :param ctx:
        :param kilometres:
        :return: None
        """
        if not kilometres:
            kilometres = 1
        await ctx.send(f"{kilometres} kilometres = {int(kilometres) * 0.62137} mi")

    @commands.command(name="ozttog")
    async def oz_troy_to_grams(self, ctx, ounce_troy: str = None) -> None:
        """
        Converts

        :param ctx:
        :param ounce_troy:
        :return: None
        """
        if not ounce_troy:
            ounce_troy = 1
        await ctx.send(f"{ounce_troy} ounces t = {int(ounce_troy) / 0.032151} g")

    @commands.command(name="gtoozt")
    async def grams_to_oz_troy(self, ctx, grams: str = None) -> None:
        """
        Converts

        :param ctx:
        :param grams:
        :return: None
        """
        if not grams:
            grams = 1
        await ctx.send(f"{grams} g = {int(grams) * 0.032151} ounces t")

    @commands.command(name="ozttooz")
    async def oz_troy_to_oz(self, ctx, ounce_troy: str = None) -> None:
        """
        Converts

        :param ctx:
        :param ounce_troy:
        :return: None
        """
        if not ounce_troy:
            ounce_troy = 1
        await ctx.send(
            f"{ounce_troy} ounces t = {int(ounce_troy) * 1.09714996656} ounces"
        )

    @commands.command(name="oztoozt")
    async def oz_to_oz_troy(self, ctx, ounces: str = None) -> None:
        """
        Converts

        :param ctx:
        :param ounces:
        :return: None
        """
        if not ounces:
            ounces = 1
        await ctx.send(f"{ounces} ounces = {int(ounces) * 0.911452427176} ounces t")


def prepare(bot: commands.Bot) -> None:
    """
    Module is being loaded, prepare anything you need then add the cog.

    :param bot: The commands' bot instance.
    :return: None
    """
    bot.add_cog(Units(bot))


def breakdown() -> None:
    """
    Called when the module is getting unloaded.

    :return:
    """
