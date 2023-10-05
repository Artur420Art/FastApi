import time
from datetime import timedelta
from typing import Annotated

from starlette.responses import JSONResponse

from userAuth.exeptions import UserExeption
from userAuth.validation import get_user_with_token
from fastapi import FastAPI, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
# from passlib.context import CryptContext
import bcrypt
from sqlalchemy.orm import Session

from database import mdatabase, engine, SessionLocal
from userAuth import manager
from userAuth.auth import get_current_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, get_current_active_user, Token
from userAuth.schema import UserDto, UserLogin
from userAuth.model import UserEntity, Base
import databases
import dotenv
import os


from fastapi import Depends, FastAPI

app = FastAPI()
Base.metadata.create_all(bind=engine)
dotenv.load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
mdatabase = databases.Database(DATABASE_URL)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.on_event("startup")
async def startup():
    await mdatabase.connect()

@app.on_event("shutdown")
async def shutdown():
    await mdatabase.disconnect()


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

@app.exception_handler(UserExeption)
async def unicorn_exception_handler(request: Request, exc: UserExeption):
    return JSONResponse(
        status_code=418,
        content={"message": f"Oops! {exc.name} did something. There goes a rainbow..."},
    )

@app.get("/unicorns/{name}")
async def read_unicorn(name: str):
    if name == "yolo":
        raise UserExeption(name=name)
    return {"unicorn_name": name}
@app.post("/add")
async def create_user(user: UserDto, db: Session = Depends(get_db)):
    return manager.create_user(db=db, user=user)

@app.post("/token", response_model=Token)
async def login_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    User_token = manager.login_user(db=db, username=form_data.username, password=form_data.password)
    return {"access_token": User_token, "token_type": "bearer"}


@app.get("/user/me")
async def get_user(current_user: Annotated[UserEntity, Depends(get_current_active_user)], db: Session = Depends(get_db)):
    return get_user_with_token(db=db, username=current_user.username, id=current_user.id)