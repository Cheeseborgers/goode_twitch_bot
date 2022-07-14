"""
Created 8/7/2022 by goode_cheeseburgers.
"""
from twitchio.ext import commands

from utilities import unit_conversion


class Units(commands.Cog):
    """
    A Cog containing all commands related to units and conversion.

    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ctof")
    async def celsius_to_fahrenheit(
        self, ctx: commands.Context, celsius: str = None
    ) -> None:
        """
        Converts Celsius to Fahrenheit.

        :param ctx: The command context.
        :param celsius: Degrees Celsius to convert.
        :return: None
        """
        if not celsius:
            celsius = 1

        fahrenheit = await unit_conversion.celsius_to_fahrenheit(celsius=celsius)

        await ctx.send(f"{fahrenheit} °F")

    @commands.command(name="ftoc")
    async def fahrenheit_to_celsius(
        self, ctx: commands.Context, fahrenheit: str = None
    ) -> None:
        """
        Converts Fahrenheit to Celsius

        :param ctx: The command context.
        :param fahrenheit: Degrees Fahrenheit to convert.
        :return: None
        """
        if not fahrenheit:
            fahrenheit = 1

        celsius = await unit_conversion.fahrenheit_to_celsius(fahrenheit=fahrenheit)

        await ctx.send(f"{celsius} °C")

    @commands.command(name="lbtokg")
    async def lb_to_kg(self, ctx: commands.Context, pounds: str = None) -> None:
        """
        Converts Pounds to Kilograms.

        :param ctx: The command context.
        :param pounds: Quantity of Pounds to convert.
        :return: None
        """
        if not pounds:
            pounds = 1

        kilos = await unit_conversion.lb_to_kg(pounds=pounds)

        await ctx.send(f"{kilos} kg")

    @commands.command(name="kgtolb")
    async def kg_to_lb(self, ctx: commands.Context, kilos: str = None) -> None:
        """
        Converts Kilograms to Pounds.

        :param ctx: The command context.
        :param kilos: Quantity of Kilograms to convert.
        :return: None
        """
        if not kilos:
            kilos = 1

        pounds = await unit_conversion.kg_to_lb(kilos=kilos)

        await ctx.send(f"{pounds} lb")

    @commands.command(name="fttom")
    async def feet_to_metres(self, ctx: commands.Context, feet: str = None) -> None:
        """
        Converts Feet to Metres.

        :param ctx: The command context.
        :param feet: Quantity of Feet to convert.
        :return: None
        """
        if not feet:
            feet = 1

        metres = await unit_conversion.feet_to_metres(feet=feet)

        await ctx.send(f"{metres} metres")

    @commands.command(name="mtoft")
    async def metres_to_feet(self, ctx: commands.Context, metres: str = None) -> None:
        """
        Converts Metres to Feet

        :param ctx: The command context.
        :param metres: Quantity of Metres to convert.
        :return: None
        """
        if not metres:
            metres = 1

        feet = await unit_conversion.metres_to_feet(metres=metres)

        await ctx.send(f"{feet} ft")

    @commands.command(name="fitom")
    async def feet_and_inches_to_metres(
        self, ctx: commands.Context, feet: str = None, inches: str = None
    ) -> None:
        """
        Converts Feet and Inches to Metres.

        :param ctx: The command context.
        :param feet: The Quantity of Feet to convert.
        :param inches: The Quantity of Inches to convert.
        :return: None
        """
        if not feet:
            feet = 1
        if not inches:
            inches = 0

        metres = await unit_conversion.feet_and_inches_to_metres(
            feet=feet, inches=inches
        )

        await ctx.send(f"{metres} metres")

    @commands.command(name="mtofi")
    async def metres_to_feet_and_inches(
        self, ctx: commands.Context, metres: str = None
    ) -> None:
        """
        Converts Metres to Feet-Inches.

        :param ctx: The command context.
        :param metres: The Quantity of Metres to convert.
        :return: None
        """
        if not metres:
            metres = 1

        feet_inches = await unit_conversion.metres_to_feet_and_inches(metres=metres)

        await ctx.send(f"{feet_inches[0]} ft, {feet_inches[1]} inches")

    @commands.command(name="gtooz")
    async def grams_to_oz(self, ctx: commands.Context, grams: str = None) -> None:
        """
        Converts Grams to Ounces.

        :param ctx: The command context.
        :param grams: The quantity of Grams to convert.
        :return: None
        """
        if not grams:
            grams = 1

        ounces = await unit_conversion.grams_to_oz(grams=grams)

        await ctx.send(f"{ounces} ounces")

    @commands.command(name="oztog")
    async def oz_to_grams(self, ctx: commands.Context, ounces: str = None) -> None:
        """
        Converts Ounces to Grams.

        :param ctx: The command context.
        :param ounces: The quantity of Ounces to convert.
        :return: None
        """
        if not ounces:
            ounces = 1

        grams = await unit_conversion.oz_to_grams(ounces=ounces)

        await ctx.send(f"{grams}g")

    @commands.command(name="mitokm")
    async def miles_to_km(self, ctx: commands.Context, miles: str = None) -> None:
        """
        Converts Miles to Kilometres.

        :param ctx: The command context.
        :param miles: The quantity of Miles to convert.
        :return: None
        """
        if not miles:
            miles = 1

        kilometres = await unit_conversion.miles_to_km(miles=miles)

        await ctx.send(f"{kilometres} kilometres")

    @commands.command(name="kmtomi")
    async def km_to_miles(self, ctx: commands.Context, kilometres: str = None) -> None:
        """
        Converts Kilometres to Miles.

        :param ctx: The command context.
        :param kilometres: The quantity of Kilometres to convert.
        :return: None
        """
        if not kilometres:
            kilometres = 1

        miles = await unit_conversion.km_to_miles(kilometres=kilometres)

        await ctx.send(f"{miles} miles")

    @commands.command(name="ozttog")
    async def oz_troy_to_grams(
        self, ctx: commands.Context, ounce_troy: str = None
    ) -> None:
        """
        Converts Ounce Troy to Grams.

        :param ctx: The command context.
        :param ounce_troy: Quantity of Ounce Troy to convert.
        :return: None
        """
        if not ounce_troy:
            ounce_troy = 1

        grams = await unit_conversion.oz_troy_to_grams(ounce_troy=ounce_troy)

        await ctx.send(f"{grams}g")

    @commands.command(name="gtoozt")
    async def grams_to_oz_troy(self, ctx: commands.Context, grams: str = None) -> None:
        """
        Converts Grams to Ounce Troy.

        :param ctx: The command context.
        :param grams: Quantity of Grams to convert.
        :return: None
        """
        if not grams:
            grams = 1

        oz_troy = await unit_conversion.grams_to_oz_troy(grams=grams)

        await ctx.send(f"{oz_troy} ounces t")

    @commands.command(name="ozttooz")
    async def oz_troy_to_oz(
        self, ctx: commands.Context, ounce_troy: str = None
    ) -> None:
        """
        Converts Ounce Troy to Ounces.

        :param ctx: The command context.
        :param ounce_troy: Quantity of Ounce Troy to convert to ounces.
        :return: None
        """
        if not ounce_troy:
            ounce_troy = 1

        ounces = await unit_conversion.oz_troy_to_oz(ounce_troy=ounce_troy)

        await ctx.send(f"{ounces} ounces")

    @commands.command(name="oztoozt")
    async def oz_to_oz_troy(self, ctx: commands.Context, ounces: str = None) -> None:
        """
        Converts Ounces to Ounce Troy.

        :param ctx: The command context.
        :param ounces: Quantity of Ounces to convert
        :return: None
        """
        if not ounces:
            ounces = 1

        oz_troy = await unit_conversion.oz_to_oz_troy(ounces=ounces)

        await ctx.send(f"{oz_troy} ounces t")


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
