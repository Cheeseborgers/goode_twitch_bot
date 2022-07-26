"""
Created 8/7/2022 by goode_cheeseburgers.
"""
import datetime
import os

import aiohttp
import dateutil.parser
from twitchio.ext import commands

from utilities.time import duration_to_string


class Twitch(commands.Cog):
    """
    A Cog containing all none mod/admin Twitch commands
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="fps")
    async def averagefps(self, ctx: commands.Context, channel_name: str = None):
        """

        :param ctx: The command context
        :param channel_name: The name of the channel to check
        :return: None
        """

        if not channel_name:
            channel_name = ctx.channel.name

        users = await self.bot.fetch_users(names=[channel_name])

        url = f"https://api.twitch.tv/helix/channels?broadcaster_id={str(users[0].id)}"

        print(url)

        headers = {
            "Authorization": "Bearer oauth:1510f8y1n2wk4enq1b5rwd7w825ii3",  # This is a fake token
            "Client-Id": os.environ.get("CLIENT_ID"),
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as resp:
                print(await resp.json())
                if resp.status == 200:
                    data = await resp.json()
                    stream = data.cache("stream")
                    if not stream:
                        return await ctx.send("Average FPS not found.")
                    await ctx.send(f"Average FPS: {stream['average_fps']}")

    @commands.command(aliases=("followed", "howlong"))
    async def followage(self, ctx: commands.Context) -> None:
        """
        Sends how long a person has been following the channel.

        :param ctx: The command context
        :return: None
        """

        streamer = await ctx.channel.user()
        streamer_user = self.bot.create_user(
            user_name=streamer.name, user_id=streamer.id
        )

        streamer_followers = await streamer_user.fetch_followers()

        for follow in streamer_followers:
            if str(follow.from_user.id) == ctx.message.author.id:
                followed_at = follow.followed_at
                ago = duration_to_string(
                    datetime.datetime.now(datetime.timezone.utc) - followed_at
                )

                return await ctx.send(
                    f"{ctx.author.name.capitalize()} followed on "
                    f"{followed_at.strftime('%B %#d %Y')}, {ago} ago"
                )

        await ctx.send(f"{ctx.author.name.capitalize()}, you haven't followed yet!")

    @commands.command()
    async def followers(self, ctx: commands.Context) -> None:
        """
        Sends the current follower count to Twitch

        :param ctx: The command context
        :return: None
        """

        streamer = await ctx.channel.user()
        streamer_user = self.bot.create_user(
            user_name=streamer.name, user_id=streamer.id
        )
        streamer_followers = await streamer_user.fetch_followers()

        await ctx.send(
            f"There are currently {len(streamer_followers)} people following "
            f"{ctx.channel.name.capitalize()}."
        )

    @commands.command(aliases=("shout",))
    async def shoutout(self, ctx: commands.Context, channel: str = None) -> None:
        """
        Sends a shoutout for a channel/user

        :param ctx: The command context
        :param channel: The Streamer/Channel to shoutout.
        :return: None
        """

        if not channel:
            return await ctx.send("\N{SPEAKING HEAD IN SILHOUETTE}")
        await ctx.send(f"Check out {channel} @ https://www.twitch.tv/{channel}")

    @commands.command()
    async def title(self, ctx: commands.Context) -> None:
        """
        Sends the current stream title to Twitch

        :param ctx: The command context
        :return: None
        """
        streamer = await ctx.channel.user()
        stream = await self.bot.fetch_streams(user_ids=[streamer.id])

        if not stream or not stream.cache("title"):
            return await ctx.send("Title not found.")

        await ctx.send(stream["title"])

    @commands.command()
    async def uptime(self, ctx: commands.Context) -> None:
        """
        Sends the uptime of the Twitch stream.

        :param ctx: The command context
        :return: None
        """

        streamer = await ctx.channel.user()
        stream = await self.bot.fetch_streams(user_ids=[streamer.id])

        if not stream:
            return await ctx.send("Uptime not found.")

        duration = datetime.datetime.now(datetime.timezone.utc) - dateutil.parser.parse(
            stream["started_at"]
        )
        await ctx.send(duration_to_string(duration))

    @commands.command()
    async def viewers(self, ctx: commands.Context) -> None:
        """
        Sends the current view count for the stream
        :param ctx: The command context
        :return: None
        """
        streamer = await ctx.channel.user()
        stream = await self.bot.fetch_streams(user_ids=[streamer.id])

        if not stream:
            return await ctx.send("Stream is offline.")

        if stream["viewer_count"] == 1:
            return await ctx.send(f"{stream['viewer_count']} viewer watching now.")

        await ctx.send(f"{stream['viewer_count']} viewers watching now.")


def prepare(bot: commands.Bot) -> None:
    """
    Module is being loaded, prepare anything you need then add the cog.

    :param bot: The commands' bot instance.
    :return: None
    """
    bot.add_cog(Twitch(bot))


def breakdown() -> None:
    """
    Called when the module is getting unloaded.

    :return:
    """
