from pydantic import BaseModel, EmailStr

class UserSchema(BaseModel):
    name: str
    age: int
    email: EmailStr