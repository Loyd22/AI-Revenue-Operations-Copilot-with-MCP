# These schemas define the input and output data for auth endpoints.

from pydantic import BaseModel, EmailStr


class UserRegisterRequest(BaseModel):
    """
    Request body for creating a new user account.
    """
    full_name: str
    email: EmailStr
    password: str
    role: str


class UserLoginRequest(BaseModel):
    """
    Request body for logging in.
    """
    email: EmailStr
    password: str


class RefreshTokenRequest(BaseModel):
    """
    Request body for refreshing an access token.
    """
    refresh_token: str


class UserResponse(BaseModel):
    """
    Safe user data returned to the client.
    """
    id: int
    full_name: str
    email: EmailStr
    role: str

    model_config = {"from_attributes": True}


class TokenResponse(BaseModel):
    """
    Token response returned after successful login.
    """
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserResponse


class MessageResponse(BaseModel):
    """
    Simple response for messages like logout confirmation.
    """
    message: str