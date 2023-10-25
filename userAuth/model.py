from sqlalchemy import Column, Integer, String, MetaData, Boolean, ForeignKey, LargeBinary
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

metadata = MetaData()

class UserEntity(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String)
    password = Column(String)
    activate = relationship("Activate", back_populates="user", uselist=False)
    def __repr__(self):
        return f"username - {self.username}, email - {self.email}, password- {self.password}"

class Activate(Base):
    __tablename__ = "activation"
    id = Column(Integer, primary_key=True, index=True)
    is_active = Column(Boolean, index=True)
    role = Column(Boolean, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("UserEntity", back_populates="activate")

class Friends(Base):
    __tablename__ = "friends"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    owner_id = relationship("UserEntity", back_populates="friends")
    friend_id = Column(Integer, ForeignKey("users.id"))
    friend = relationship("UserEntity", back_populates="friends")