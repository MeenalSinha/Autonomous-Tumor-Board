from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.database import Base
import os

DB_URL = os.getenv("DATABASE_URL", "sqlite:///./tumor_board.db")

engine = create_engine(DB_URL, connect_args={"check_same_thread": False} if "sqlite" in DB_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
