from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from datetime import date

DATABASE_URL = "sqlite:///./salary.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

class Base(DeclarativeBase):
    pass

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    Base.metadata.create_all(bind=engine)



