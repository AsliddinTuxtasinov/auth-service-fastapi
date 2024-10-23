from pydantic import BaseModel, constr, EmailStr, Field


class UserLoginSchema(BaseModel):
    # Validates phone numbers with 10 to 15 digits, optionally starting with '+'
    phone_number: str = Field(..., pattern=r'^\+?\d{10,15}$')
    password: str = Field(..., min_length=8)  # Ensures the password is at least 8 characters long


class UserAuthSchema(UserLoginSchema):
    email: EmailStr  # Ensures the email is a valid email address format
