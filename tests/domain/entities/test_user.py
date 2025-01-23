import pytest
from pydantic import ValidationError

from app.domain.entities.user import User


def test_user_creation_success():
    user = User(
        name="John Doe",
        email="john.doe@example.com",
        hashed_password="hashed_pwd",
        is_active=True,
    )
    assert user.name == "John Doe"
    assert user.email == "john.doe@example.com"


def test_user_creation_failure_with_invalid_email():
    with pytest.raises(ValidationError):
        User(
            name="John Doe",
            email="john.doe",
            hashed_password="hashed_pwd",
            is_active=True,
        )
