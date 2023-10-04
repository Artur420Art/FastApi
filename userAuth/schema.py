from pydantic import BaseModel

class Userin(BaseModel):
    id: int
    username: str
    email: str
    password: str

class UserDto(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password:str