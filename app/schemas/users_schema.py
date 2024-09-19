from pydantic import BaseModel, EmailStr

class UserSchema(BaseModel):
    id: int
    username: str
    email: EmailStr = "example@gmail.com"
    full_name: str | None = None
    disabled: bool | None = None
    hashed_password: str





