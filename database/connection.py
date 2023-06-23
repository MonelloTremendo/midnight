from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import os

SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_CONNECTION_STRING", "mysql+mysqldb://root:midnight@127.0.0.1/midnight")

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=False)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = scoped_session(SessionLocal)()
    try:
        yield db
    finally:
        db.close()