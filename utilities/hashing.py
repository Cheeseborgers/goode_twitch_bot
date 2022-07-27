"""
Created 27/7/2022 by goode_cheeseburgers.
"""
from typing import Union

from dotenv import load_dotenv
import argon2.exceptions
from argon2 import PasswordHasher
from quart.utils import run_sync

from goode_bot_twitch.logging_handler import get_logger

load_dotenv()

logger = get_logger(__name__)


async def create(password: Union[str, bytes]) -> str:
    """
    Hashes a password with argon2

    :param password: The password to hash
    :return: str: The hashed password
    """

    if isinstance(password, str):
        password = password.encode()

    try:
        password_hash = PasswordHasher().hash(password)
        return password_hash

    except argon2.exceptions.HashingError as error:
        logger.error("Password hashing error: %s", error)


async def verify(password_hash: Union[str, bytes], password: Union[str, bytes]) -> bool:
    """
    Verify if the login password matches the users hash from the db.

    :param password_hash: The users has to verify against
    :param password: The requested password to challenge
    :return: bool: whether the password matches the hash
    """

    if isinstance(password, str):
        password = password.encode()

    try:
        is_match = await run_sync(PasswordHasher().verify)(password_hash, password)
    except argon2.exceptions.VerifyMismatchError:
        logger.debug("Password mismatch.")
        return False
    except argon2.exceptions.VerificationError as error:
        logger.error("Password verification failure: %s", error)
        return False
    except argon2.exceptions.InvalidHash as error:
        logger.warning(
            "The hash clearly invalid, and could not be passed by Argon2: %s", error
        )
        return False

    return is_match
