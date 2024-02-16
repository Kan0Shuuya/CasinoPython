from fastapi import HTTPException

UnableToValidateException = HTTPException(
    status_code=401,
    detail="Couldn't validate credentials",
    headers={"WWW-Authenticate": "Bearer"}
)
TokenExpiredException = HTTPException(
    status_code=401,
    detail="Token expired",
    headers={"WWW-Authenticate": "Bearer"}
)
IncorrectUsernameOrPasswordException = HTTPException(
    status_code=401,
    detail="Incorrect username or password",
    headers={"WWW-Authenticate": "Bearer"}
)