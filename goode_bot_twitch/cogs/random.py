"""
Created 8/7/2022 by goode_cheeseburgers.
"""
import random

from twitchio.ext import commands


class RandomCommandsCog(commands.Cog):
    """
    A Cog for commands which produce a random result.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="_roll", aliases=("dice", "roll"))
    async def _roll(self, ctx: commands.Context, dice: str = None):
        """
        Rolls a die in NdN format.

        @param: ctx:
        @param: dice: str: NdN format dice string
        """

        if not dice:
            dice = "1d6"

        try:
            rolls, limit = map(int, dice.split("d"))
        except ValueError:
            await ctx.send(f"@{ctx.author.name}, Format has to be in NdN!")
            return

        result = ", ".join(str(random.randint(1, limit)) for _ in range(rolls))
        await ctx.send(
            f"@{ctx.author.name}, rolled {result} in {rolls} roll(s) with a {limit} sided die."
        )

    @commands.command(name="_penis", aliases=("peepee", "penis"))
    async def _penis(self, ctx: commands.Context, username: str = None):
        """
        Returns the peepee length for a user.

        @param: ctx: The message context
        @param: username: (optional) The user to include
        :return:
        """

        if not username:
            user = ctx.author
            length = get_peepee_size(int(user.id))
            return await ctx.send(f"{user.name.capitalize()} has a {length} peepee")

        if username[0] == "@":
            username = username[1:]

        user = await self.bot.fetch_users(names=[username])
        length = get_peepee_size(int(user[0].id))

        return await ctx.send(f"{user[0].name.capitalize()} has a {length} peepee")

    @commands.command(name="_color", aliases=("color", "colour"))
    async def _color(self, ctx: commands.Context):
        """
        Generates a random hex color

        @param: ctx: The message context
        :return:
        """

        color = f"#{random.randint(0, 0xFFFFFF):06X}"
        await ctx.send(f"Here is a random color: {color}")

    @commands.command(name="_rng", aliases=("rng", "randomnum"))
    async def _rng(self, ctx: commands.Context, arg1: str = "1", arg2: str = "100"):
        """
        Generates a random number within the given range

        @param: arg2:
        @param: arg1:
        @param: ctx: The message context
        :return:
        """

        if arg1.isdigit() and arg2.isdigit():
            start = int(arg1)
            end = int(arg2)
            if start > end:
                start, end = end, start
            if start == end:
                await ctx.send("Response won't be random with that range...")
            else:
                number = random.randint(start, end)
                await ctx.send(
                    f"Here is a random number between {start} and {end}: ---> {number}"
                )

    @commands.command(name="_8ball", aliases=("8ball", "8b"))
    async def _8ball(self, ctx):
        """
        Returns a random 8ball answer.
        @param: ctx:
        :return:
        """
        responses = [
            "It is certain.",
            "It is decidedly so.",
            "Without a doubt.",
            "Yes - definitely.",
            "You may rely on it.",
            "As I see it, yes.",
            "Most likely.",
            "Outlook good.",
            "Yes.",
            "Signs point to yes.",
            "Reply hazy, try again.",
            "Ask again later.",
            "Better not tell you now.",
            "Cannot predict now.",
            "Concentrate and ask again.",
            "Don't count on it.",
            "My reply is no.",
            "My sources say no.",
            "Outlook not so good.",
            "Very doubtful.",
        ]
        await ctx.send(f"@{ctx.author.name}, {random.choice(responses)}")

    @commands.command(name="_coin", aliases=("flip", "coin"))
    async def _coin(self, ctx):
        """

        @param: ctx:
        :return:
        """
        await ctx.channel.send(
            f'@{ctx.author.name}, It landed on {random.choice(["heads", "tails"])}'
        )


def prepare(bot: commands.Bot) -> None:
    """
    Module is being loaded, prepare anything you need then add the cog.

    @param: bot: The commands' bot instance
    :return: None
    """

    bot.add_cog(RandomCommandsCog(bot))


def breakdown() -> None:
    """
    Called when the module is getting unloaded

    :return: None
    """


def get_peepee_size(user_id: int) -> str:
    """
    Returns a string of the users peepee size.

    @param: user_id:
    :return: str: The returned string eg: '6cm 🍌'
    """
    length = user_id % 30

    length = max(length, 6)

    if length <= 10:
        response = f"{length}cm 🤏"
    elif length <= 15:
        response = f"{length}cm 🪱"
    elif length <= 20:
        response = f"{length}cm 🍌"
    else:
        response = f"{length}cm 🍆"

    return response
