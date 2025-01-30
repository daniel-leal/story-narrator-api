class ScenarioAlreadyExistsError(Exception):
    """Raised when trying to create a scenario that already exists."""


class InvalidScenarioDataError(Exception):
    """Raised when scenario data is invalid (e.g., missing fields, too long)."""
