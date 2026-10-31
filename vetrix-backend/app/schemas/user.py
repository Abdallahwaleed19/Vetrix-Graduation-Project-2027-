from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr


class RoleBase(BaseModel):
    name: str
    description: Optional[str] = None


class RoleResponse(RoleBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class UserBase(BaseModel):
    email: EmailStr
    full_name: str


class UserCreate(UserBase):
    password: str
    role_id: int


class UserResponse(UserBase):
    id: int
    is_active: bool
    role_id: int
    role: Optional[RoleResponse] = None

    model_config = ConfigDict(from_attributes=True)
