from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

# SQL_DATABASE_URL = "postgresql://docker:docker@localhost:32767/fastapi"
SQL_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'
engine = create_engine(SQL_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# dependency
# bunu sqlalchemy icin yapiyoruz. bu aslinda bir dependency injection.


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
