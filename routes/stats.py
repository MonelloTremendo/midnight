from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text

from typing import List

from database.connection import get_db
from database.models import FlagStats, FlagStatsPerTick, FlagStatsPerTickTeam, FlagStatsTeam

router = APIRouter(
    prefix="/stats",
    tags=["stats"],
    responses={404: {"description": "Not found"}},
)

@router.get("/flags/all")
def get_flags_all(db: Session = Depends(get_db)) -> FlagStats:
    query = """
        SELECT 
            COUNT(*) AS total,
            SUM(status=0) AS queued,
            SUM(status=1) AS accepted,
            SUM(status=2) AS rejected
        FROM flags
        """
    
    result = db.execute(text(query)).fetchone()

    return FlagStats.from_orm(result)

@router.get("/flags/tick")
def get_flags_tick(db: Session = Depends(get_db)) -> List[FlagStatsPerTick]:
    query = """
        SELECT 
            COUNT(*) AS total,
            SUM(status=0) AS queued,
            SUM(status=1) AS accepted,
            SUM(status=2) AS rejected,
            (end_time - MOD(end_time, 120)) AS tick_start
        FROM runs INNER JOIN flags ON runs.id = flags.run_id
        GROUP BY tick_start
        ORDER BY tick_start DESC
        LIMIT 15
        """
    
    result = db.execute(text(query)).fetchall()
    result = [FlagStatsPerTick.from_orm(tick) for tick in result]

    return result


@router.get("/flags/script/{exploit_id}/all")
def get_flags_script(exploit_id:int, db: Session = Depends(get_db)) -> List[FlagStatsPerTick]:
    query = """
        SELECT 
            COUNT(*) AS total,
            SUM(status=0) AS queued,
            SUM(status=1) AS accepted,
            SUM(status=2) AS rejected,
            (end_time - MOD(end_time, 120)) AS tick_start
        FROM runs INNER JOIN flags ON runs.id = flags.run_id
        WHERE runs.exploit_id = :exploit_id
        GROUP BY tick_start
        """
    
    result = db.execute(text(query), { "exploit_id": exploit_id }).fetchall()
    result = [FlagStatsPerTick.from_orm(tick) for tick in result]

    return result

@router.get("/flags/script/{exploit_id}/last/teams")
def get_flags_script_team(exploit_id:int, db: Session = Depends(get_db)) -> List[FlagStatsPerTickTeam]:
    query = """
        SELECT 
            runs.team_id as team,
            COUNT(*) AS total,
            SUM(status=0) AS queued,
            SUM(status=1) AS accepted,
            SUM(status=2) AS rejected,
            (end_time - MOD(end_time, 120)) AS tick_start
        FROM flags INNER JOIN runs ON runs.id = flags.run_id
        WHERE runs.exploit_id = :exploit_id
        GROUP BY tick_start, runs.team_id
        ORDER BY tick_start DESC
        LIMIT 1, 1
        """
    
    result = db.execute(text(query), { "exploit_id": exploit_id }).fetchall()
    result = [FlagStatsPerTickTeam.from_orm(tick) for tick in result]

    return result


@router.get("/flags/scripts/all")
def get_flags_tick(db: Session = Depends(get_db)) -> List[FlagStatsTeam]:
    query = """
        SELECT
            exploits.name,
            COUNT(*) AS total,
            SUM(status=0) AS queued,
            SUM(status=1) AS accepted,
            SUM(status=2) AS rejected
        FROM (runs INNER JOIN flags ON runs.id = flags.run_id) INNER JOIN exploits ON runs.exploit_id = exploits.id
        GROUP BY runs.exploit_id, exploits.name;
        """
    
    result = db.execute(text(query)).fetchall()
    result = [FlagStatsTeam.from_orm(tick) for tick in result]

    return result