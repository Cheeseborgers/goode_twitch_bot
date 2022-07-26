"""
Created 26/7/2022 by goode_cheeseburgers.
"""
import uuid

import typing
from sqlalchemy import Column, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm.exc import DetachedInstanceError

Base = declarative_base()


class AbstractBase(Base):  # pylint: disable=too-few-public-methods
    """
    The Abstract Base class for all sqlalchemy models.
    """

    __abstract__ = True

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now())

    def __repr__(self) -> str:
        return self._repr(
            id=self.id, created_at=self.created_at, updated_at=self.updated_at
        )

    def _repr(self, **fields: typing.Any) -> str:
        """
        Helper for __repr__
        """
        field_strings = []
        at_least_one_attached_attribute = False
        for key, field in fields.items():
            try:
                field_strings.append(f"{key}={field!r}")
            except DetachedInstanceError:
                field_strings.append(f"{key}=DetachedInstanceError")
            else:
                at_least_one_attached_attribute = True
        if at_least_one_attached_attribute:
            return f"<{self.__class__.__name__}({', '.join(field_strings)})>"
        return f"<{self.__class__.__name__} {id(self)}>"

    def __str__(self) -> str:
        return self._str(
            id=self.id, created_at=self.created_at, updated_at=self.updated_at
        )

    def _str(self, **fields: typing.Any) -> str:
        """
        Helper for __str__
        """
        field_strings = []
        at_least_one_attached_attribute = False
        for key, field in fields.items():
            try:
                field_strings.append(f"{key}={field!r}")
            except DetachedInstanceError:
                field_strings.append(f"{key}=DetachedInstanceError")
            else:
                at_least_one_attached_attribute = True
        if at_least_one_attached_attribute:
            return f"{self.__class__.__name__}({', '.join(field_strings)})"
        return f"<{self.__class__.__name__} {id(self)}>"
