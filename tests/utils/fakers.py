from factory import Factory, Faker

from app.domain.entities.user import User


class UserFactory(Factory):
    """Factory for generating User entities."""

    class Meta:
        model = User

    id = Faker("uuid4")
    name = Faker("name")
    email = Faker("email")
    hashed_password = Faker("password")
    is_active = True
