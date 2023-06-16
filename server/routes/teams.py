from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text

from server.app import app

from server.database.connection import get_db
from server.database.models import TeamBase, Team

@app.get("/teams")
def get_teams(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT * FROM teams")).fetchall()
    result = [Team.from_orm(team) for team in result]

    return result
    
@app.get("/teams/{team_id}")
def get_team(team_id: int, db: Session = Depends(get_db)):
    result = db.execute(text("SELECT * FROM teams WHERE id = :team_id"), { "team_id": team_id }).fetchone()

    if not result:
        raise HTTPException(404, "Not found")

    return Team.from_orm(result)


@app.post("/teams")
def add_team(team: TeamBase, db: Session = Depends(get_db)):
    db.execute(text("INSERT INTO teams (name, ip) VALUES (:name, :ip)"), { "name" : team.name, "ip" : team.ip })
    db.commit()

    return team

@app.patch("/teams/{team_id}")
def edit_team(team_id: int, team: TeamBase, db: Session = Depends(get_db)):
    db.execute(text("UPDATE teams SET name = :name, ip = :ip WHERE id = :id"), { "name" : team.name, "ip" : team.ip, "id" : team_id })
    db.commit()

    return team

@app.delete("/teams/{team_id}")
def delete_team(team_id: int, db: Session = Depends(get_db)):
    db.execute(text("DELETE FROM teams WHERE id = :id"), { "id" : team_id })
    db.commit()

    return team_id