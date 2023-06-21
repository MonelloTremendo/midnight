from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import text

from typing import List

from database.connection import get_db
from database.models import FlagStats, FlagStatsPerTick, FlagStatsTeam, FlagsExploitTimestamp, FlagStatsPerTickTeam

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

    if None not in result:
        return FlagStats.from_orm(result)
    else:
        return JSONResponse(status_code=404, content={"message": "stats not found"})


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

    if result:
        result = [FlagStatsPerTick.from_orm(tick) for tick in result]
        return result
    else:
        return JSONResponse(status_code=404, content={"message": "stats not found"})


@router.get("/flags/script/{exploit_id}")
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

    if result:
        result = [FlagStatsPerTick.from_orm(tick) for tick in result]
        return result
    else:
        return JSONResponse(status_code=404, content={"message": "stats not found"})

@router.get("/flags/script/{exploit_id}/all")
def get_flags_script(exploit_id:int, db: Session = Depends(get_db)) -> FlagStats:
    query = """
        SELECT 
            COUNT(*) AS total,
            SUM(status=0) AS queued,
            SUM(status=1) AS accepted,
            SUM(status=2) AS rejected
        FROM flags INNER JOIN runs ON flags.run_id = runs.id
        WHERE runs.exploit_id = :exploit_id
        """
    
    result = db.execute(text(query), { "exploit_id": exploit_id }).fetchone()

    if None not in result:
        return FlagStats.from_orm(result)
    else:
        return JSONResponse(status_code=404, content={"message": "stats not found"})
    
@router.get("/flags/script/{exploit_id}/teams")
def get_flags_script_teams_lastrun(exploit_id:int, db: Session = Depends(get_db)) -> List[FlagStatsPerTickTeam]:
    query = """
        SELECT 
            runs.team_id as team,
            COUNT(*) AS total,
            SUM(status=0) AS queued,
            SUM(status=1) AS accepted,
            SUM(status=2) AS rejected,
            (end_time - MOD(end_time, 120)) AS tick_start
        FROM runs INNER JOIN flags ON runs.id = flags.run_id
        WHERE runs.exploit_id = :exploit_id
        GROUP BY tick_start, runs.team_id
        HAVING tick_start = (
            SELECT
            (end_time - MOD(end_time, 120)) AS tick_start 
            FROM runs 
            GROUP BY tick_start 
            ORDER BY tick_start DESC 
            LIMIT 1, 1
        )
        """
    
    result = db.execute(text(query), { "exploit_id": exploit_id }).fetchall()

    if result:
        result = [FlagStatsPerTickTeam.from_orm(tick) for tick in result]
        return result
    else:
        return JSONResponse(status_code=404, content={"message": "stats not found"})


@router.get("/flags/scripts/time/{timestamp}")
def get_flags_scripts_timestamp(timestamp:int, db: Session = Depends(get_db)) -> List[FlagsExploitTimestamp]:
    query = """
        SELECT 
            exploits.id,
            COALESCE(tab1.flags, 0) as flags
        FROM exploits LEFT JOIN (
            SELECT 
                runs.exploit_id AS expl_id,
                COUNT(*) AS flags,
                (runs.end_time - MOD(runs.end_time, 120)) AS tick_start 
            FROM flags INNER JOIN runs ON run_id = runs.id
            GROUP BY tick_start, runs.exploit_id
            HAVING tick_start = :timestamp
        ) AS tab1 ON exploits.id = tab1.expl_id;
        """
    
    result = db.execute(text(query), { "timestamp": timestamp }).fetchall()

    if result:
        result = [FlagsExploitTimestamp.from_orm(tick) for tick in result]
        return result
    else:
        return JSONResponse(status_code=404, content={"message": "stats not found"})


@router.get("/flags/scripts/all")
def get_flags_scripts(db: Session = Depends(get_db)) -> List[FlagStatsTeam]:
    query = """
        SELECT
            exploits.id,
            exploits.name,
            COUNT(*) AS total,
            SUM(status=0) AS queued,
            SUM(status=1) AS accepted,
            SUM(status=2) AS rejected
        FROM (runs INNER JOIN flags ON runs.id = flags.run_id) INNER JOIN exploits ON runs.exploit_id = exploits.id
        GROUP BY runs.exploit_id, exploits.name;
        """

    result = db.execute(text(query)).fetchall()

    if result:
        result = [FlagStatsTeam.from_orm(tick) for tick in result]
        return result
    else:
        return JSONResponse(status_code=404, content={"message": "stats not found"})
    
@router.get("/flags/exploit/{exploit_id}/teams")
def get_flags_sexploit_teams(exploit_id: int, db: Session = Depends(get_db)):
    teamids = db.execute(text("SELECT id FROM teams")).fetchall()

    query = """
        SELECT 
            runs.team_id,
            COUNT(*) AS total,
            (end_time - MOD(end_time, 120)) AS tick_start
        FROM runs INNER JOIN flags ON runs.id = flags.run_id
        WHERE runs.exploit_id = :exploit_id
        GROUP BY tick_start, runs.team_id
        ORDER BY tick_start
        """

    result = db.execute(text(query), { "exploit_id": exploit_id }).fetchall()

    if not result:
        return JSONResponse(status_code=404, content={"message": "stats not found"})

    times = set(map(lambda item: item[2], result))

    for i in range(list(times)[0], list(times)[-1], 120):
        times.add(i)

    out = {i: {} for i in times}

    for time in times:
        data = list(filter(lambda item: item[2] == time, result))

        for team in teamids:
            d = list(filter(lambda item: item[0] == team[0], data))

            if len(d) > 0:
                out[time][team[0]] = d[0][1]
            else:
                out[time][team[0]] = 0

    
    return out
    #if result:
    #    result = [FlagStatsTeam.from_orm(tick) for tick in result]
    #    return result
    #else:
    #    return JSONResponse(status_code=404, content={"message": "stats not found"})