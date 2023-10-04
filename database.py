import dotenv
import os
import databases
import sqlalchemy
from sqlalchemy.orm import declarative_base, sessionmaker
from userAuth.model import metadata

dotenv.load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
mdatabase = databases.Database(DATABASE_URL)

engine = sqlalchemy.create_engine(
    DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

metadata.create_all(engine)

