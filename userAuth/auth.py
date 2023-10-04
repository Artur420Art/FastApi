from datetime import timedelta, datetime
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel
from sqlalchemy.orm import Session
import main
from userAuth.model import UserEntity
from userAuth.validation import get_user_with_token

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class TokenData(BaseModel):
    username: str | None = None
    id: int

class Token(BaseModel):
    access_token: str
    token_type: str


class User(BaseModel):
    username: str
    email: str | None = None

class UserInDB(User):
    hashed_password: str

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Could not validate credentials token = {token}",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")
        id: str = payload.get("id")

        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username, id=id)
    except JWTError:
        raise credentials_exception
    return token_data


async def get_current_active_user(
    current_user: Annotated[TokenData, Depends(get_current_user)],
):
    return current_user

