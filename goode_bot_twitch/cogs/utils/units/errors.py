"""
Created 8/7/2022 by goode_cheeseburgers.
"""


class UnitError(Exception):
    """Unit Error"""


class UnitExecutionError(UnitError):
    """Unit Execution Error"""


class UnitOutputError(UnitError):
    """Unit Output Error"""
