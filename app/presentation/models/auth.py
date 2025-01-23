from pydantic import BaseModel, EmailStr


class RegisterUserRequest(BaseModel):
    """
    Pydantic model for user registration request payload.
    """

    name: str
    email: EmailStr
    password: str


class RegisterUserResponse(BaseModel):
    """
    Pydantic model for user registration response payload.
    """

    email: EmailStr
    name: str
    message: str


class LoginRequest(BaseModel):
    """
    Pydantic model for user login request payload.
    """

    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    """
    Pydantic model for user login response payload.
    """

    access_token: str
    token_type: str = "bearer"
