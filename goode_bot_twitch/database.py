"""
Created 12/7/2022 by goode_cheeseburgers.
"""
import os

import aiosqlite
from dotenv import load_dotenv

load_dotenv()


async def fetchall(query: str) -> tuple:
    """
    Fetch all remaining rows.

    :param query: The sql query to execute.
    :return: tuple:
    """
    async with aiosqlite.connect(
        database=os.environ.get("DATABASE_PATH")
    ) as connection:
        async with connection.execute(query) as cursor:
            rows = await cursor.fetchall()
            return rows


async def fetchone(query: str) -> tuple:
    """
    Fetch a single row.

    :param query: The sql query to execute.
    :return: tuple: The row queried form the database
    """
    async with aiosqlite.connect(
        database=os.environ.get("DATABASE_PATH")
    ) as connection:
        async with connection.execute(query) as cursor:
            row = await cursor.fetchone()
            return row


async def execute(query: str) -> None:
    """
    Execute the given query.

    :param query: The sql query to execute.
    :return: None
    """
    async with aiosqlite.connect(
        database=os.environ.get("DATABASE_PATH")
    ) as connection:
        await connection.execute(query)
        await connection.commit()


async def execute_many(query: str) -> None:
    """
    Execute the given query.

    :param query: The sql query to execute.
    :return: None
    """
    async with aiosqlite.connect(
        database=os.environ.get("DATABASE_PATH")
    ) as connection:
        await connection.execute(query)
        await connection.commit()

    # pylint: disable=pointless-string-statement
    """
    async def execute_script(sql_script: str) -> None:

        Execute a user script.

        :param sql_script: sql_script must be a string
        :return: None

        async with aiosqlite.connect(database=os.environ.get("DATABASE_PATH")) as connection:
            async with connection.executescript(sql_script):

                await connection.commit() """
