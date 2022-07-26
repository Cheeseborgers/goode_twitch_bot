"""
Created 12/7/2022 by goode_cheeseburgers.
"""
import os

import sqlalchemy
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from goode_bot_twitch.logging_handler import get_logger
from goode_bot_twitch.models.abstract_base import AbstractBase

load_dotenv()

logger = get_logger(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL")

# An async SQLAlchemy Engine that will interact with a PostgreSQL database.
if os.environ.get("DEBUG"):
    logger.debug("Starting database engine...")
    logger.debug("Sqlalchemy version: %s", sqlalchemy.__version__)
    engine = create_async_engine(DATABASE_URL, echo=True)
else:
    engine = create_async_engine(DATABASE_URL)

# An async SQLAlchemy ORM session factory bound to the above engine.
async_session: sessionmaker = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def drop_models() -> None:
    """
    Drops all models from the database.

    :return: None
    """
    async with engine.begin() as conn:
        await conn.run_sync(AbstractBase.metadata.drop_all)
        logger.debug("All models dropped.")


async def create_models() -> None:
    """
    Creates all models in the database

    :return: None
    """
    async with engine.begin() as conn:
        await conn.run_sync(AbstractBase.metadata.create_all)
        logger.debug("All models created.")


async def init_models() -> None:
    """
    Drops all tables from the database and recreates them.

    :return: None
    """
    await drop_models()
    await create_models()
    logger.debug("Database initialized.")
