"""
Created 8/7/2022 by goode_cheeseburgers.
"""
from asyncio import sleep
from random import randint, choice

import twitchio


def get_author_prefix(self, message: twitchio.Message) -> str:
    """
    Returns the Twitch user prefix as a string.

    :param self:
    :param message: The Twitch message.
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
        user_prefix = "[Bot]"
    return user_prefix


def get_sub_tier(data) -> int:
    """
    Returns the Twitch Sub tier.

    :param data:
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

    :param emote_list:
    :return: str:  A string of random channel emotes
    """
    return " ".join([choice(emote_list) for _ in range(randint(10, 20))])


async def create_raw_thank_you_message(bot, channel_name: str, tags: dict):
    """
    Creates a thankyou message for subs and gift subs.

    :param bot:
    :param channel_name:
    :param tags:
    :return:
    """

    bot.logger.debug("%s <--- type", tags["msg-id"])

    if tags["msg-id"] == "submysterygift" or tags["msg-id"] == "subgift":

        if bot.rate_limits.get(channel_name) > 5:
            bot.logger.debug("Rate limit exceeded!!")
            return

        # Increase the rate_limit by 1
        bot.rate_limits[channel_name] = bot.rate_limits.get(channel_name) + 1

        # Sleep for a random time to prevent immediate sending of the message
        await sleep(randint(9, 16))

        # Sub gift bomb
        if tags["msg-id"] == "submysterygift":

            print(
                f'Gifter\'s name is: {tags["display-name"]} :--- Quantity: '
                f'{tags["msg-param-mass-gift-count"]}'
            )

            if channel_name == "cakez77":
                thank_you_msg = (
                    f'GG cakezRub @{tags["login"]} {randint(10, 20) * " cakezRub2"}'
                )
                bot.logger.debug("Thankyou msg sent: %s", thank_you_msg)
                return thank_you_msg

            if channel_name == "jonbams":
                thank_you_msg = (
                    f'GG bamOML @{tags["login"]} {randint(10, 20) * " bamHeart"}'
                )

                bot.logger.debug("Thankyou msg sent: %s", thank_you_msg)

                return thank_you_msg

        # Handle and an individual gift sub
        if tags["msg-id"] == "subgift":

            print(f'Gifted persons  name is: {tags["msg-param-recipient-user-name"]}')

            thank_you_msg = generate_emotes(bot.channels[channel_name]["thanks_emotes"])

            bot.logger.debug("Thankyou msg sent: %s", thank_you_msg)

            return thank_you_msg


async def create_thank_you_message(bot, subscription_data: dict):
    """
    May get rid of this after testing.

    :param bot:
    :param subscription_data:
    :return:
    """

    channel_name = subscription_data["channel"].name

    # Increase the rate_limit by 1
    if bot.rate_limits.get(channel_name) > 5:
        bot.logger.debug("Rate limit exceeded!!")
        return

    bot.rate_limits[channel_name] = bot.rate_limits.get(channel_name) + 1

    # Add streak months to sub data tags if not present (set to 0)
    if "msg-param-streak-months" not in subscription_data["tags"].keys():
        subscription_data["tags"]["msg-param-streak-months"] = "0"

    sub_data = {
        "channel": channel_name,
        "user": subscription_data["user"].name,
        "display_name": subscription_data["tags"]["display-name"],
        "months": subscription_data["tags"]["msg-param-cumulative-months"],
        "streak_months": subscription_data["tags"]["msg-param-streak-months"],
        "tier": get_sub_tier(subscription_data["sub_plan"]),
        "gifted": get_sub_tier(subscription_data["sub_plan"]),
    }

    await sleep(randint(9, 16))

    thank_you_msg = generate_emotes(bot.channels[channel_name]["thanks_emotes"])

    print(f'{sub_data["display_name"]=} : {sub_data["channel"]=} : ({thank_you_msg=})')

    return thank_you_msg
