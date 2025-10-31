from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

Base = declarative_base()

DB_PATH = os.path.join("data", "apply_me.db")
engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)
SessionLocal = sessionmaker(bind=engine)

def init_db():
    from app import models
    Base.metadata.create_all(bind=engine)
