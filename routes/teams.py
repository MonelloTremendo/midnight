from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import text

from ..database.connection import get_db
from ..database.models import TeamBase, Team

router = APIRouter(
    prefix="/teams",
    tags=["teams"],
    responses={404: {"description": "not found"}},
)

@router.get("/")
def get_teams(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT * FROM teams")).fetchall()
    result = [Team.from_orm(team) for team in result]

    return result
    
@router.get("/{team_id}")
def get_team(team_id: int, db: Session = Depends(get_db)):
    result = db.execute(text("SELECT * FROM teams WHERE id = :team_id"), { "team_id": team_id }).fetchone()

    if not result:
        return JSONResponse(status_code=404, content={"message": "team not found"})

    return Team.from_orm(result)


@router.post("/")
def add_team(team: TeamBase, db: Session = Depends(get_db)):
    result = db.execute(text("INSERT INTO teams (name, ip) VALUES (:name, :ip)"), { "name" : team.name, "ip" : team.ip })
    db.commit()

    return result.lastrowid

@router.patch("/{team_id}")
def edit_team(team_id: int, team: TeamBase, db: Session = Depends(get_db)):
    db.execute(text("UPDATE teams SET name = :name, ip = :ip WHERE id = :id"), { "name" : team.name, "ip" : team.ip, "id" : team_id })
    db.commit()

    return

@router.delete("/{team_id}")
def delete_team(team_id: int, db: Session = Depends(get_db)):
    db.execute(text("DELETE FROM teams WHERE id = :id"), { "id" : team_id })
    db.commit()

    return team_id