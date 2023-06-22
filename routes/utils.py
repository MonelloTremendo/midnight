from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text

from database.connection import get_db
from runner.runner import run_exploit

from database.models import Flag

from routes.websocket import manager
import asyncio


router = APIRouter(
    prefix="/utils",
    tags=["api"],
    responses={404: {"description": "Not found"}},
)

@router.get("/init")
def random(db: Session = Depends(get_db)):
    return {}

@router.get("/flags")
def get_flags(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT * FROM flags")).fetchall()
    result = [Flag.from_orm(flag) for flag in result]

    return result

@router.get("/test")
def get_test(db: Session = Depends(get_db)):
    import string, random

    print(Flag(flag="".join(random.choice(string.ascii_uppercase) for _ in range(31)) + "=", run_id=1, status=1).dict())

    return {}