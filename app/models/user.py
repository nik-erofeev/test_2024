from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    hashed_password: str


class UserResponse(UserBase):
    message: str

    class Config:
        from_attributes = True
