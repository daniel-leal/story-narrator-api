class StoryValidationError(Exception):
    """Base class for all story validation errors."""

    pass


class InvalidNarrativeStyleError(StoryValidationError):
    """Raised when an invalid or empty narrative style is provided."""

    def __init__(self):
        super().__init__("A valid narrative style is required.")


class CharactersEmptyError(StoryValidationError):
    """Raised when no characters are provided for story generation."""

    def __init__(self):
        super().__init__("At least one character is required to generate a story.")


class TooManyCharactersError(StoryValidationError):
    """Raised when too many characters are included in a story."""

    def __init__(self, max_characters=5):
        super().__init__(f"A story cannot have more than {max_characters} characters.")


class InvalidScenarioError(StoryValidationError):
    """Raised when an invalid scenario is provided."""

    def __init__(self):
        super().__init__("Scenario not found.")
