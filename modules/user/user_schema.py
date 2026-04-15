from pydantic import BaseModel, EmailStr, field_validator


class RegisterSchema(BaseModel):
    name: str
    email: EmailStr
    password: str
    phone: str
    gender: str


class UserSchema(BaseModel):
    name: str
    age: int
    email: EmailStr

  # Custom validation for name
    @field_validator('name')
    def name_must_not_be_empty(cls, value):
        if not value.strip():
            raise ValueError("Name cannot be empty")
        return value

    # Custom validation for age
    @field_validator('age')
    def age_must_be_positive(cls, value):
        if value <= 0:
            raise ValueError("Age must be greater than 0")
        return value
    
class LoginSchema(BaseModel):
    email: EmailStr
    password: str