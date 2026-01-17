from pydantic import BaseModel, EmailStr, constr

# pip install 'pydantic[email]'
class User(BaseModel):
    id: int
    name: constr(min_length=3, max_length=50)
    email: EmailStr
