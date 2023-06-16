from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text

from ..database.connection import get_db

router = APIRouter(
    prefix="/api",
    tags=["api"],
    responses={404: {"description": "Not found"}},
)

@router.get("/random")
def random(db: Session = Depends(get_db)):
    #result = db.execute(text("INSERT INTO teams (name, ip) VALUE ('test', 'lmao')"))
    #db.commit()

    return {}