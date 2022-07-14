"""
Created 14/7/2022 by goode_cheeseburgers.

Converts units from one unit to another.
Conversions are returns as strings or a tuple of strings.
"""


async def celsius_to_fahrenheit(celsius: str) -> str:
    """
    Converts Celsius to Fahrenheit.

    :param celsius: Degrees Celsius to convert.
    :return: str:
    """

    return str(int(celsius) * 9 / 5 + 32)


async def fahrenheit_to_celsius(fahrenheit: str) -> str:
    """
    Converts Fahrenheit to Celsius

    :param fahrenheit: Degrees Fahrenheit to convert.
    :return: str:
    """
    return str((int(fahrenheit) - 32) * 5 / 9)


async def lb_to_kg(pounds: str) -> str:
    """
    Converts Pounds to Kilograms.

    :param pounds: Quantity of Pounds to convert.
    :return: str:
    """

    return str(int(pounds) * 0.45359237)


async def kg_to_lb(kilos: str) -> str:
    """
    Converts Kilograms to Pounds.

    :param kilos: Quantity of Kilograms to convert.
    :return: str:
    """

    return str(int(kilos) * 2.2046)


async def feet_to_metres(feet: str) -> str:
    """
    Converts Feet to Metres.

    :param feet: Quantity of Feet to convert.
    :return: str:
    """

    return str(int(feet) * 0.3048)


async def metres_to_feet(metres: str) -> str:
    """
    Converts Metres to Feet

    :param metres: Quantity of Metres to convert.
    :return: str:
    """

    return str(int(metres) * 3.2808)


async def feet_and_inches_to_metres(feet: str, inches: str) -> str:
    """
    Converts Feet and Inches to Metres.

    :param feet: The Quantity of Feet to convert.
    :param inches: The Quantity of Inches to convert.
    :return: str:
    """

    return str((int(feet) + int(inches) / 12) * 0.3048)


async def metres_to_feet_and_inches(metres: str) -> tuple[str, str]:
    """
    Converts Metres to Feet-Inches.

    :param metres: The Quantity of Metres to convert.
    :return: tuple[str, str]: A tuple of feet and inches.
    """

    feet = int(metres) * 39.37 // 12
    inches = int(metres) * 39.37 - feet * 12

    return str(feet), str(inches)


async def grams_to_oz(grams: str) -> str:
    """
    Converts Grams to Ounces.

    :param grams: The quantity of Grams to convert.
    :return: str
    """

    return str(int(grams) * 0.035274)


async def oz_to_grams(ounces: str) -> str:
    """
    Converts Ounces to Grams.

    :param ounces: The quantity of Ounces to convert.
    :return: str:
    """

    return str(int(ounces) / 0.035274)


async def miles_to_km(miles: str) -> str:
    """
    Converts Miles to Kilometres.

    :param miles: The quantity of Miles to convert.
    :return: str:
    """
    return str(int(miles) / 0.62137)


async def km_to_miles(kilometres: str) -> str:
    """
    Converts Kilometres to Miles.

    :param kilometres: The quantity of Kilometres to convert.
    :return: str:
    """
    return str(int(kilometres) * 0.62137)


async def oz_troy_to_grams(ounce_troy: str) -> str:
    """
    Converts Ounce Troy to Grams.

    :param ounce_troy: Quantity of Ounce Troy to convert.
    :return: str:
    """

    return str(int(ounce_troy) / 0.032151)


async def grams_to_oz_troy(grams: str) -> str:
    """
    Converts Grams to Ounce Troy.

    :param grams: Quantity of Grams to convert.
    :return: str:
    """

    return str(int(grams) * 0.032151)


async def oz_troy_to_oz(ounce_troy: str) -> str:
    """
    Converts Ounce Troy to Ounces.

    :param ounce_troy: Quantity of Ounce Troy to convert to ounces.
    :return: str:
    """

    return str(int(ounce_troy) * 1.09714996656)


async def oz_to_oz_troy(ounces: str) -> str:
    """
    Converts Ounces to Ounce Troy.

    :param ounces: Quantity of Ounces to convert
    :return: str:
    """

    return str(int(ounces) * 0.911452427176)
