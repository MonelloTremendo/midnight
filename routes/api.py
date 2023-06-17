from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text

from database.connection import get_db
from runner.runner import run_exploit

from database.models import Flag

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

@router.get("/flags")
def get_flags(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT * FROM flags")).fetchall()
    result = [Flag.from_orm(flag) for flag in result]

    return result