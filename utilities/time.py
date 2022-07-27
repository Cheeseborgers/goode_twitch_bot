"""
Created 27/7/2022 by goode_cheeseburgers.
"""
import datetime

import pytz

from utilities.errors import UnitExecutionError


def duration_to_string(duration: datetime.timedelta) -> str:
    """
    Returns a datatime duration as a string

    :param duration: The datetime delta as a string
    :return: str

    :raise: utilities.errors.UnitExecutionError:
    Raised when the duration is not a datetime.timedelta
    """

    if not isinstance(duration, datetime.timedelta):
        raise UnitExecutionError("duration must be datetime.timedelta")

    negative = False

    if duration.total_seconds() < 0:
        duration = abs(duration)
        negative = True

    units = {
        "year": duration.days // 365,
        "week": duration.days % 365 // 7,
        "day": duration.days % 365 % 7,
    }

    outputs = []

    for name, value in units.items():

        if not value:
            continue

        if negative:
            value = -value

        output = f"{value} {name}"

        if abs(value) > 1:
            output += "s"
        outputs.append(output)
    return " ".join(outputs)


async def seconds_to_hms(seconds: float) -> tuple[int, int, int]:
    """
    Converts a float value of seconds to hour, minutes, seconds and
    returns them as a tuple.

    :param seconds: The quantity of seconds to calculated from.
    :return: str: A tuple containing the hours, minutes, seconds.
    """
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)

    return int(hours), int(minutes), int(seconds)


async def get_common_timezones() -> list[str]:
    """
    Returns a list of common timezones.

    :return: list[str]: A list of common timezones.
    """
    return pytz.common_timezones
