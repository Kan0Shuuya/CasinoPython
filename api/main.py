from datetime import datetime, timedelta
from typing import Annotated
import uvicorn
from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from api.exceptions import *
from database import *
from main import logger  # TODO: Import from main file to retain settings
import sys

# ===[CONSTANT DECLARATION START]===
sys.path.insert("/persist")
SECRET_KEY = "6f1ba5597ebd52c859e42e176ab526baa3fb8d9ad2f848383397e3f2f68a39d8"
TOKEN_EXPIRE_TIMEDELTA_MINUTES = 24 * 60
app = FastAPI()
app.logger = logger
db = Database("/persist/db.db")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
cryptcontext = CryptContext(schemes=["bcrypt"])
# ===[CONSTANT DECLARATION END]===

logger.debug("Initializing API structures...")


def hash_password(password_plaintext: str) -> str:
    """Hashes a password using bcrypt. Returns a hash."""
    return cryptcontext.hash(password_plaintext)


def verify_password(password_plaintext: str, supposed_hash: str) -> bool:
    """Verifies a password against a hash. Returns True if the password is correct, False otherwise."""
    return cryptcontext.verify(password_plaintext, supposed_hash)


def authenticate_by_credentials(username: str, password_userinput: str) -> User | bool:
    """Authenticates a user by username and password. Returns a User object if successful, False otherwise."""
    user_dict = db.getAllUserDataAsDict(username)
    if not user_dict:
        return False
    if not verify_password(password_userinput, user_dict["password"]):
        return False
    return User(**user_dict)


def generate_token(username: str) -> str:
    """Generates a new access token. Returns a token."""
    expiry = str(datetime.now() + timedelta(minutes=TOKEN_EXPIRE_TIMEDELTA_MINUTES))
    data = {"username": username,
            "expiry": expiry}
    return jwt.encode(data, SECRET_KEY, algorithm="HS256")


@app.post("/token")
def obtain_new_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """Returns a new access token if credentials are valid. Raises exceptions otherwise.
    Although it seems like it requires a fancy OAuth2PasswordRequestForm, a username & password dict will do."""
    user = authenticate_by_credentials(form_data.username, form_data.password)
    if not user:
        raise IncorrectUsernameOrPasswordException

    token = generate_token(form_data.username)
    return Token(access_token=token, token_type="bearer")


def get_user_from_token(token: str) -> dict:
    """Performs token validation and returns user data if successful. Raises exceptions otherwise.
    Do NOT put this in try/except block, it's supposed to be handled by FastAPI."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except JWTError:
        raise UnableToValidateException

    username: str = payload.get("username")
    expiry: str = payload.get("expiry")

    if not username or not expiry:
        raise UnableToValidateException

    if datetime.now() > datetime.fromisoformat(expiry):
        raise TokenExpiredException

    user = db.getNonSensitiveUserDataAsDict(username)
    if not user:
        raise UnableToValidateException
    return user


@app.get("/me")
def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    """Returns user data if token is valid. Raises exceptions otherwise."""
    return get_user_from_token(token)


@app.post("/register")
def create_user(username: str, password_plaintext: str):
    """Registers a new user. Raises exceptions if user already exists.
    TODO: Add a check for username length and password complexity."""
    result = db.registration(username, hash_password(password_plaintext))
    if not result:
        raise HTTPException(status_code=418, detail="жуй хуй")


def run(host: str, port: int):
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    raise NotImplementedError("Not supposed to be ran standalone")
