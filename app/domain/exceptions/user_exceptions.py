class UserAlreadyRegisteredError(Exception):
    """Raised when a user is already registered."""

    def __init__(self, email: str) -> None:
        super().__init__(f"User with email {email} is already registered")
        self.email = email
