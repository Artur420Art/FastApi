from http.client import HTTPException
import re

import bcrypt
from sqlalchemy.orm import Session

from constants import statuseCode, messages
from userAuth.exeptions import UserExeption
from userAuth.model import UserEntity
from userAuth.schema import UserDto, UserLogin

EMAIL_REGEX_PATTERN = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

def uniqeue_user(db: Session, user: UserDto):
    existing_user = db.query(UserEntity).filter(
        (UserEntity.email == user.email) | (UserEntity.username == user.username)
    ).first()
    if existing_user:
        raise UserExeption(name=messages.USED, status_code=statuseCode.UNAUTHORIZED)


def get_user(db: Session, username: str, password: str):
    user_entity = db.query(UserEntity).filter(UserEntity.username == username).first()
    if user_entity is None:
        raise UserExeption(name=messages.UNOTFOUND ,status_code=statuseCode.NOTFOUND)

    if not bcrypt.checkpw(password.encode('utf-8'), user_entity.password.encode('utf-8')):
        raise UserExeption(name=messages.INCPASS, status_code=statuseCode.UNAUTHORIZED,)

    return user_entity

def get_user_with_token(db:Session, username: str, id: int):
    user_entity =  db.query(UserEntity).filter(UserEntity.id == id).first()
    if user_entity is None:
        raise UserExeption(status_code=statuseCode.NOTFOUND, name=messages.UNOTFOUND)
    return user_entity
def validate_email(email):
    if not re.match(EMAIL_REGEX_PATTERN, email):
        raise UserExeption(status_code=statuseCode.BADREQUEST, name=messages.INVEMAIL)
    return email


def is_valid_password(password):
    pattern = r'^(?=.*[A-Z])(?=.*\d).+$'
    if re.match(pattern, password):
        return password
    else:
        raise UserExeption(status_code=statuseCode.BADREQUEST, name=messages.PASSVALID)