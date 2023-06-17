from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text

from database.connection import get_db

router = APIRouter(
    prefix="/stats",
    tags=["teams"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
def get_teams(db: Session = Depends(get_db)):
    return