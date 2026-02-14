from fastapi import FastAPI, Request, Depends, HTTPException, Cookie
from fastapi.responses import RedirectResponse
from fastapi.responses import HTMLResponse

import os
from dotenv import load_dotenv
import httpx

from baza import init_db, get_user, add_user

from jose import jwt, JWTError

init_db()

load_dotenv()
app = FastAPI()

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGO = "HS256"

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
BACK_URI = os.getenv("BACK_URI")

print(BACK_URI)

GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://openidconnect.googleapis.com/v1/userinfo"
