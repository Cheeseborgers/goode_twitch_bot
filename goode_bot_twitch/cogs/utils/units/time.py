"""
Created 8/7/2022 by goode_cheeseburgers.
"""
import datetime

from .errors import UnitExecutionError


def duration_to_string(duration: datetime.timedelta) -> str:
    """
    Returns a datatime duration as a string

    :param duration: The datetime delta
    :return: str
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
