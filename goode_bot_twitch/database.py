"""
Created 12/7/2022 by goode_cheeseburgers.
"""
import asyncio
import os
from pathlib import Path

import aiosqlite
from dotenv import load_dotenv

load_dotenv()


# add exception handling


class Database:
    """
    Sqlite3 data base functions.

    """

    def __init__(self):
        self.database_path = Path(os.environ.get("DATABASE_PATH"))

    async def fetchall(self, loop: asyncio.AbstractEventLoop, query: str) -> tuple:
        """
        Fetch all remaining rows.

        :param loop:
        :param query:
        :return:
        """
        async with aiosqlite.connect(
            database=self.database_path, loop=loop
        ) as connection:
            async with connection.execute(query) as cursor:
                rows = await cursor.fetchall()
                return rows

    async def fetchone(self, loop: asyncio.AbstractEventLoop, query: str) -> tuple:
        """
        Fetch a single row.

        :param loop:
        :param query:
        :return:
        """
        async with aiosqlite.connect(
            database=self.database_path, loop=loop
        ) as connection:
            async with connection.execute(query) as cursor:
                row = await cursor.fetchone()
                return row

    async def execute(self, loop: asyncio.AbstractEventLoop, query: str):
        """
        Execute the given query.

        :param loop:
        :param query:
        :return:
        """
        async with aiosqlite.connect(
            database=self.database_path, loop=loop
        ) as connection:
            await connection.execute(query)
            await connection.commit()

    async def execute_many(self, loop: asyncio.AbstractEventLoop, query: str):
        """
        Execute the given query.

        :param loop:
        :param query:
        :return:
        """
        async with aiosqlite.connect(
            database=self.database_path, loop=loop
        ) as connection:
            await connection.execute(query)
            await connection.commit()

    async def execute_script(self, loop: asyncio.AbstractEventLoop, sql_script: str):
        """
        Execute a user script.

        :param loop:
        :param sql_script: sql_script must be a string
        :return:
        """
        async with aiosqlite.connect(
            database=self.database_path, loop=loop
        ) as connection:
            async with connection.executescript(sql_script):
                await connection.commit()
