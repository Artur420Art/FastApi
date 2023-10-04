from sqlalchemy import Column, Integer, String, MetaData
from sqlalchemy.orm import declarative_base

Base = declarative_base()

metadata = MetaData()

class UserEntity(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String)
    password = Column(String, default=True)
    def __repr__(self):
        return f"username - {self.username}, email - {self.email}, password- {self.password}"
