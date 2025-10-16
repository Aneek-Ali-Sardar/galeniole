from pydantic import BaseModel, EmailStr

class User(BaseModel):
    email: EmailStr
    password: str
    name: str

class Userlogin(BaseModel):
    email: EmailStr
    password: str