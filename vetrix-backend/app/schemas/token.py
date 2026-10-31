from typing import Optional, Union
from pydantic import BaseModel


class Token(BaseModel):
    """Schema for JWT access token response."""

    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    """Schema for decoded JWT token claims."""

    sub: Optional[Union[int, str]] = None
    role: Optional[str] = None
