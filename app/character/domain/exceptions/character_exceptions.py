class CharacterValidationError(Exception):
    """Base class for all character validation errorrs."""


class CharactersEmptyError(CharacterValidationError):
    """Raised when no characters are provided for story generation."""

    def __init__(self):
        super().__init__("At least one character is required to generate a story.")
