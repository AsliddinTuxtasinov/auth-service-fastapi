import datetime

from pydantic import BaseModel, EmailStr, Field


class UserLoginSchema(BaseModel):
    # Validates phone numbers with 10 to 15 digits, optionally starting with '+'
    phone_number: str = Field(..., pattern=r'^\+?\d{10,15}$')
    password: str = Field(..., min_length=8)  # Ensures the password is at least 8 characters long


class UserAuthSchema(UserLoginSchema):
    email: EmailStr  # Ensures the email is a valid email address format

    class Config:
        orm_mode = True  # Enables Pydantic to work with ORM objects directly
        from_attributes = True


class UserSchema(BaseModel):
    email: EmailStr
    phone_number: str
    created_at: datetime  # Datetime type for created_at field
    is_verified: bool

    class Config:
        orm_mode = True  # Enables Pydantic to work with ORM objects directly
        from_attributes = True
        arbitrary_types_allowed = True  # This allows Pydantic to work with datetime


class ResponseLoginSchema(BaseModel):
    user: UserSchema
    access: str  # Token for access
    refresh: str  # Token for refreshing the session
