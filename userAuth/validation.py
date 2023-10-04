from http.client import HTTPException
import re

import bcrypt
from sqlalchemy.orm import Session
from userAuth.model import UserEntity
from userAuth.schema import UserDto, UserLogin

EMAIL_REGEX_PATTERN = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

def uniqeue_user(db: Session, user: UserDto):
    existing_user = db.query(UserEntity).filter(
        (UserEntity.email == user.email) | (UserEntity.username == user.username)
    ).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="username or email is used")


def get_user(db: Session, username: str, password: str):
    user_entity = db.query(UserEntity).filter(UserEntity.username == username).first()
    if user_entity is None:
        raise HTTPException(status_code=404, detail="User not found")

    if not bcrypt.checkpw(password.encode('utf-8'), user_entity.password.encode('utf-8')):
        raise HTTPException(status_code=401, detail="Incorrect password")

    return user_entity

def get_user_with_token(db:Session, username: str, id:int):
    user_entity =  db.query(UserEntity).filter(UserEntity.id == id).first()
    return user_entity

def validate_email(email):
    if not re.match(EMAIL_REGEX_PATTERN, email):
        raise HTTPException(status_code=400, detail="Invalid email address")
    return email
