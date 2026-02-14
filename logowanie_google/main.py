from fastapi import FastAPI, Request, Depends, HTTPException, Cookie
from fastapi.responses import RedirectResponse
from fastapi.responses import HTMLResponse

import os
from dotenv import load_dotenv
import httpx

from baza import init_db, get_user, add_user

from jose import jwt, JWTError

init_db()

app = FastAPI()