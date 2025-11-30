from pydantic import BaseModel, EmailStr


class SUserAuth(BaseModel):
    email: EmailStr # валидация что действительно являестся строка емеилом
    password: str


