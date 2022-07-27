"""
Created 27/7/2022 by goode_cheeseburgers.
"""
import typing
from sqlalchemy import select, delete
from sqlalchemy.engine import ScalarResult
from sqlalchemy.exc import (
    NoResultFound,
    IntegrityError,
    InvalidRequestError,
    ArgumentError,
)

from goode_bot_twitch.database import async_session
from goode_bot_twitch.models.abstract_base import AbstractBase
from goode_bot_twitch.models.errors import (
    ModelNotFound,
    ModelAlreadyExists,
    BaseModelUsedInCall,
)


async def add_model(model: AbstractBase) -> None:
    """
    Adds a single model to the database.

    Parameters
    ------------
    @param: model: A model to add to the database
    :return: None

    @raise: ModelAlreadyExists: Raised if the model already exists in the database.
    """
    try:
        async with async_session() as session:
            async with session.begin():
                session.add(model)
                await session.commit()

    except IntegrityError as exc:
        raise ModelAlreadyExists(model) from exc


async def add_models(models: typing.Union[list, tuple]) -> None:
    """
    Adds a list or tuple of models to the database.

    Parameters
    ------------
    @param: users: A list or tuple of models to add to the database
    :return: None

    @raise: ModelAlreadyExists: Raised if the model already exists in the database.
    """
    try:
        async with async_session() as session:
            async with session.begin():
                for model in models:
                    session.add(model)

                await session.commit()

    except IntegrityError as exc:
        raise ModelAlreadyExists(model) from exc


async def delete_model(model: typing.Any) -> None:
    """
    Deletes a single model from the database.

    Parameters
    ------------
    @param: model: A model to delete from the database
    :return: None

    @raise: ModelNotFound: Raised when the model is not found in the database.
    @raise: BaseModelUsedInCall: Raised when the abstract base model is called
    instead of the child model.
    """
    try:
        async with async_session() as session:
            async with session.begin():
                statement = (
                    delete(model.__class__)
                    .where(model.__class__.name == model.name)
                    .execution_options(synchronize_session="fetch")
                )

                await session.execute(statement)

                await session.commit()

    except IntegrityError as exc:
        raise ModelNotFound(model) from exc
    except InvalidRequestError as exc:
        raise ModelNotFound(model) from exc
    except ArgumentError as exc:
        raise BaseModelUsedInCall(model) from exc


async def delete_models(models: typing.Union[list, tuple]) -> None:
    """
    Deletes a list or tuple of models from the database.

    Parameters
    ------------
    @param: users: A list or tuple of models to delete from the database
    :return: None

    @raise: ModelNotFound: Raised when the model is not found in the database.
    """
    try:
        async with async_session() as session:
            async with session.begin():
                for model in models:
                    statement = (
                        delete(model.__class__)
                        .where(model.__class__.name == model.name)
                        .execution_options(synchronize_session="fetch")
                    )

                    await session.execute(statement)

                await session.commit()

    except IntegrityError as exc:
        raise ModelNotFound(model) from exc
    except InvalidRequestError as exc:
        raise ModelNotFound(model) from exc


async def get_model(model: AbstractBase) -> AbstractBase:
    """
    Fetches a model from database.

    Parameters
    ------------
    @param: model: A model to fetch from the database.
    :return: AbstractBase: The model object returned from database.

    @raise: ModelNotFound: Raised when the model is not found in the database.
    """
    try:
        async with async_session() as session:
            async with session.begin():
                # query from a class
                statement = select(model).filter_by(name=model.name)

                # list of first element of each row (i.e. User objects)
                cursor = await session.execute(statement)

                # Return the TwitchChannel if found, raise if not.
                return cursor.scalars().one()

    except NoResultFound as exc:
        raise ModelNotFound(model) from exc


async def get_models(model) -> ScalarResult:
    """
    Fetches all types of given model type from the database.

    parameters
    ----------
    :return: ScalarResult: The Models
    """

    async with async_session() as session:
        async with session.begin():
            query = select(model)

            result = await session.execute(query)

            return result.scalars()
