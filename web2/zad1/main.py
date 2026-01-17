# pip install fastapi
import uvicorn
from fastapi import FastAPI

# pip install uvicorn - server www, serwer aplikacji web
app = FastAPI()


@app.get("/")
def hello_world():
    return {"message": "Hello, World"}

# http://0.0.0.0:8000/hello/Radek
@app.get("/hello/{name}")
def hello_name(name: str):
    return {"message": f"Hello, {name.title()}!"}

if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True  # tylkow środowiskach dev, zmiana przeładowuje serwer
    )
# http://0.0.0.0:8000
# localhost:8000
# http://127.0.0.1:8000/docs
# Dokumentacja OpenAPI - Swagger
# http://0.0.0.0:8000/docs
# postman
# INFO:     127.0.0.1:65441 - "GET /radek HTTP/1.1" 404 Not Found
# (.venv) radoslawjaniak@mac BootCamp-11-10-2025-WEB % curl -X 'GET' \
#   'http://0.0.0.0:8000/hello/tomek' \
#   -H 'accept: application/json'
# {"message":"Hello, Tomek!"}%
