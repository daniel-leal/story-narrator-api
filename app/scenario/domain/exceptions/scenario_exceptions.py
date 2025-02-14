class ScenarioValidationError(Exception):
    """Base class for all scenario validation errors"""


class ScenarioAlreadyExistsError(Exception):
    """Raised when trying to create a scenario that already exists."""


class InvalidScenarioDataError(Exception):
    """Raised when scenario data is invalid (e.g., missing fields, too long)."""
