from datetime import timedelta

from sqlalchemy.orm import Session
import bcrypt
from automapper import mapper

from userAuth.auth import create_access_token
from userAuth.model import UserEntity
from userAuth.schema import UserDto, UserLogin
from userAuth.validation import validate_email, uniqeue_user, get_user
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_user(db: Session, user: UserDto):
    uniqeue_user(db=db, user=user)
    salt = bcrypt.gensalt()
    password = user.password.encode('utf-8')
    hashed_password = bcrypt.hashpw(password, salt)
    db_user = UserDto(email=validate_email(user.email), password=hashed_password, username=user.username)
    mapper.add(UserDto, UserEntity)
    entityUs = mapper.map(db_user)

    db.add(entityUs)
    db.commit()
    db.refresh(entityUs)
    return db_user
def login_user(db: Session, username: str, password: str):

    x = get_user(db=db, username= username, password=password)
    access_token = create_access_token(
        data={"username": x.username, "id": x.id}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return access_token
