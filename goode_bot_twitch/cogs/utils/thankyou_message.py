"""
Created 8/7/2022 by goode_cheeseburgers.
"""
from random import randint, choices, choice

import twitchio


def get_author_prefix(self, message: twitchio.Message) -> str:
    """
    Returns the Twitch user prefix as a string.

    @param: self:
    @param: message: The Twitch message.
    :return: str: The message authors prefix (ie: [Subscriber])
    """
    user_prefix = ""
    if message.author.is_subscriber:
        user_prefix = "[Subscriber]"
    elif message.author.is_mod:
        user_prefix = "[Moderator]"
    # Notice!! the following two can get a little confusing
    # when using this as a channel Self bot.
    elif message.tags["room-id"] == message.author.id:
        user_prefix = "[Streamer]"
    elif message.author.name.lower() == self.bot.nick.lower():
        user_prefix = "[TwitchBot]"
    return user_prefix


def get_sub_tier(data) -> int:
    """
    Returns the Twitch Sub tier.

    @param: data:
    :return: int: The Twitch sub tier level.
    """
    if data == 2000:
        return 2
    if data == 3000:
        return 3

    return 1


def generate_emotes(emote_list) -> str:
    """
    Generates a string of random emotes from a given list.

    @param: emote_list:
    :return: str:  A string of random channel emotes
    """

    return " ".join(choices(emote_list, k=randint(10, 20)))


async def create_thank_you_message(bot, channel_name: str, tags: dict) -> str:
    """
    Creates a thankyou message for subs and gift subs.

    @param: bot:
    @param: channel_name:
    @param: tags:
    :return:
    """

    # Sub gift bomb
    if tags["msg-id"] == "submysterygift":

        bot.logger.debug(
            "[Gift-Sub] - Gifter: %s ----- Quantity: %s",
            tags["display-name"],
            tags["msg-param-mass-gift-count"],
        )

        end_emote = " " + bot.channels.cache[channel_name].subgift_thanks_end_emote

        thank_you_msg = (
            f"GG {bot.channels.cache[channel_name].subgift_thanks_start_emote} "
            f'@{tags["login"]} {randint(10, 20) * end_emote}'
        )

        return thank_you_msg

    # Handle and an individual gift sub
    if tags["msg-id"] == "subgift":

        bot.logger.debug(
            "[Gift-Sub] - Gifted Subscriber: %s", tags["msg-param-recipient-user-name"]
        )

        thank_you_msg = generate_emotes(bot.channels.cache[channel_name].thanks_emotes)

        return thank_you_msg

    if tags["msg-id"] == "resub" or tags["msg-id"] == "sub":
        bot.logger.debug(
            "[%s] - Subscriber: %s", tags["msg-id"].capitalize(), tags["display-name"]
        )
        thank_you_msg = generate_emotes(bot.channels.cache[channel_name].thanks_emotes)

        if int(tags["msg-param-cumulative-months"]) > 80:

            over_sub_month_threshold_msgs = ["do you have any idea how long that is?"]

            thank_you_msg = (
                f"{thank_you_msg} GG {tags['display-name']}, "
                f"{tags['msg-param-cumulative-months']}, "
                f"{choice(over_sub_month_threshold_msgs)}"
            )

        return thank_you_msg
