# i cant name shit okay
from loguru import logger
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from database import *
from passlib.context import CryptContext
from jose import jwt, JWTError
from typing import Annotated
import uvicorn

# ===[CONSTANT DECLARATION START]===
# To generate a new one run: openssl rand -hex 32
# Ideally should be rotated once in a while
SECRET_KEY = "c61634b5c9f1c5243e44f718dd9a8de805e6a394a405f1be523f490522e2ce25"
TOKEN_EXPIRE_TIMEDELTA_MINUTES = 24 * 60
app = FastAPI()
db = Database(":memory:")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
cryptcontext = CryptContext(schemes=["bcrypt"])


def hash_password(password_plaintext: str) -> str:
    return cryptcontext.hash(password_plaintext)


def verify_password(password_plaintext: str, supposed_hash: str) -> bool:
    return cryptcontext.verify(password_plaintext, supposed_hash)


def authenticate_by_credentials(username: str, password_userinput: str) -> User | bool:
    user_dict = db.getAllUserDataAsDict(username)
    if not user_dict:
        return False
    if not verify_password(password_userinput, user_dict["password"]):
        return False
    return User(**user_dict)


def generate_token(username: str) -> str:
    expiry = str(datetime.now() + timedelta(minutes=TOKEN_EXPIRE_TIMEDELTA_MINUTES))
    data = {"username": username,
            "expiry": expiry}
    return jwt.encode(data, SECRET_KEY, algorithm="HS256")


@app.post("/token")
def obtain_new_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_by_credentials(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = generate_token(form_data.username)
    return Token(access_token=token, token_type="bearer")


@app.get("/me")
def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    cred_exception = HTTPException(
        status_code=401,
        detail="Couldn't validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, "HS256")
        username = payload.get("username")
        if not username:
            raise cred_exception
    except JWTError:
        raise cred_exception
    user = db.getAllUserDataAsDict(username)
    if not user:
        raise cred_exception

    return user


@app.post("/register")
def create_user(username: str, password_plaintext: str):
    result = db.registration(username, hash_password(password_plaintext))
    if not result:
        raise HTTPException(status_code=418, detail="жуй хуй")


def run(port: int):
    uvicorn.run(app, port=port)


if __name__ == "__main__":
    raise NotImplementedError("Not supposed to be ran standalone")
