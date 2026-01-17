from fastapi import FastAPI

app = FastAPI()

user_db = []


@app.get("/users/")
def get_users():
    return {"users": user_db}

# uvicorn main:app --reload
#  zad2 % uvicorn main:app --reload