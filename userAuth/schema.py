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

class Activate(BaseModel):
    is_active: bool
    role: bool
    user_id: object

class UploadFileTit(BaseModel):
    title: str
    description: str
    image_data: bytes