from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# for firebase auth
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status, Response

from enum import Enum
from typing import Union
from pydantic import BaseModel
import os

from firebase_admin import auth, credentials
import firebase_admin

import logging
logger = logging.getLogger(__name__)

# initialize firebase admin
path_to_certificate = os.environ.get('PATH_TO_FIREBASE_CREDENTIALS')
if not path_to_certificate:
    logger.info("PATH_TO_FIREBASE_CREDENTIALS not set. Using default path.")
    path_to_certificate = "./backend_app/firebase_credentials.json"
else:
    logger.info("PATH_TO_FIREBASE_CREDENTIALS set, use {}".format(path_to_certificate))


cred = credentials.Certificate(path_to_certificate)
firebase_admin.initialize_app(cred)


app = FastAPI()
logger.info("App successfully initialized.")

# Configurations for CORS:
# The following means;
allowed_origins = [
    "http://localhost:5173"
]

allowed_methods = [
    "POST",
    "GET"
]

allowed_headers = [
    "*",
    # "application/json",
    # "X-AUTH-TOKEN"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=allowed_methods,
    allow_headers=allowed_headers
)


app = FastAPI()


def get_user(res: Response,
             cred: HTTPAuthorizationCredentials=Depends(HTTPBearer(auto_error=False))):
    if cred is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Bearer authentication required",
            headers={'WWW-Authenticate': 'Bearer realm="auth_required"'},
        )
    try:
        decoded_token = auth.verify_id_token(cred.credentials)
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication credentials. {err}",
            headers={'WWW-Authenticate': 'Bearer error="invalid_token"'},
        )
    res.headers['WWW-Authenticate'] = 'Bearer realm="auth_required"'
    return decoded_token


@app.get("/user_info")
async def user(user_info=Depends(get_user)):
    return {"message": "User",
            "user_info": user_info}

@app.get("/special_message")
async def special_message():
    the_special_message = "You are the best!"
    return {"message": the_special_message}

@app.get("/greeting_message")
async def greeting_message():
    return {"message": "Welcome back, sir!"}
