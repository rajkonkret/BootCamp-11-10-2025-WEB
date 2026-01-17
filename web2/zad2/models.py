from pydantic import BaseModel, EmailStr, constr


class User(BaseModel):
    id: int
    name: constr(min_length=3, max_length=50)
    email: EmailStr
