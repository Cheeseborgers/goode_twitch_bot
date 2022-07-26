"""
Created 24/7/2022 by goode_cheeseburgers.
"""
from dataclasses import dataclass
import datetime


@dataclass
class User:
    """
    A Dataclass to hold information about a user

    """

    __slots__ = ["username", "email", "password_hash", "role", "account_creation_date"]

    username: str
    email: str
    password_hash: str
    role: int
    account_creation_date: datetime.datetime
