from fastapi import FastAPI
from models import User

app = FastAPI()

user_db = []


@app.get("/users/")
def get_users():
    return {"users": user_db}


@app.post("/users/")
def create_user(user: User):
    user_db.append(user)
    return {"message": "User created!", "user": user}
# uvicorn main:app --reload
#  zad2 % uvicorn main:app --reload
# http://127.0.0.1:8000/docs
