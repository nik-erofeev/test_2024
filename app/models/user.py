from uuid import UUID

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    hashed_password: str


class UserCreateResponse(UserBase):
    message: str

    class Config:
        from_attributes = True


class UserResponseAll(UserBase):
    is_active: bool
    id: UUID
    hashed_password: str

    class Config:
        from_attributes = True


class UserDelResponse(BaseModel):
    id: UUID
    message: str

    class Config:
        from_attributes = True


class UserResponse(UserBase):
    is_active: bool
    id: UUID

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
