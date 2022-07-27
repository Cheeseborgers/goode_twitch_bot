"""
Created 26/7/2022 by goode_cheeseburgers.
"""
import uuid

from sqlalchemy import Column, DateTime, func, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm.exc import DetachedInstanceError

Base = declarative_base()


class AbstractBase(Base):
    """
    The Abstract Base class for all sqlalchemy models.
    """

    __abstract__ = True

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(36), nullable=False, unique=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now())

    def __repr__(self) -> str:
        return self._repr()

    def _repr(self) -> str:
        """
        Helper for __repr__
        """
        field_strings = []
        at_least_one_attached_attribute = False

        for key, field in self.__dict__.items():

            if key != "_sa_instance_state":
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
        return self._str()

    def _str(self) -> str:
        """
        Helper for __str__
        """
        field_strings = []
        at_least_one_attached_attribute = False

        for key, field in self.__dict__.items():

            if key != "_sa_instance_state":
                try:
                    field_strings.append(f"{key}={field!r}")
                except DetachedInstanceError:
                    field_strings.append(f"{key}=DetachedInstanceError")
                else:
                    at_least_one_attached_attribute = True

        if at_least_one_attached_attribute:
            return f"{self.__class__.__name__}({', '.join(field_strings)})"

        return f"<{self.__class__.__name__} {id(self)}>"

    def as_dict(self) -> dict:
        """
        Returns the object as a dictionary.

        :return: dict:
        """
        return {
            x: self.__dict__[x]
            for x in self.__dict__.items()
            if x != "_sa_instance_state"
        }
