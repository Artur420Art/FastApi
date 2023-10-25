import hashlib
import uuid
from base64 import b64encode
from datetime import timedelta

from sqlalchemy.orm import Session
import bcrypt
from automapper import mapper
from userAuth.helper.mailSender import send_activation_email
from userAuth.auth import create_access_token
from userAuth.exeptions import UserExeption
from userAuth.model import UserEntity, Activate
from userAuth.schema import UserDto, UserLogin
from userAuth.validation import validate_email, uniqeue_user, get_user, is_valid_password
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_user(db: Session, user: UserDto):
    try:
        uniqeue_user(db=db, user=user)
        is_valid_password(user.password)
    except UserExeption as e:
        raise e

    salt = bcrypt.gensalt()
    password = user.password.encode('utf-8')
    hashed_password = bcrypt.hashpw(password, salt)
    db_user = UserDto(email=validate_email(user.email), password=hashed_password, username=user.username)

    mapper.add(UserDto, UserEntity)
    entityUs = mapper.map(db_user)
    send_activation_email(user_email=entityUs.email)
    db.add(entityUs)
    db.commit()
    return db_user
def login_user(db: Session, username: str, password: str):

    x = get_user(db=db, username= username, password=password)
    access_token = create_access_token(
        data={"username": x.username, "id": x.id}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return access_token

def activate_user_account(db: Session, user: UserEntity):
    userAct = Activate()
    userAct.is_active = True
    userAct.role = False
    userAct.user = user
    userAct.user_id = user.id
    db.add(userAct)
    db.commit()


