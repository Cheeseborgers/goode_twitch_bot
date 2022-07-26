"""
Created 26/7/2022 by goode_cheeseburgers.
"""


class ModelException(BaseException):
    """
    Base class for all model exceptions.
    """


class ModelNotFound(ModelException):
    """
    Raised when a model is not found in the database.

    Attributes
    ----------
    model -- input model which caused the error
    message -- explanation of the error
    """

    def __init__(self, model, message="Model not found in the database."):
        self.model = model
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.model.name} -> {self.message}"


class ModelAlreadyExists(ModelException):
    """
    Raised when a model already exists in the database.

    Attributes
    ----------
    model -- input model which caused the error
    message -- explanation of the error
    """

    def __init__(self, model, message="Model already exists in the database."):
        self.model = model
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.model.name} -> {self.message}"
