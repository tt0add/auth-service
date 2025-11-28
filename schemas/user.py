from pydantic import BaseModel, EmailStr

class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str

class UserResponseSchema(BaseModel):
    id: int
    email: EmailStr
    role: str