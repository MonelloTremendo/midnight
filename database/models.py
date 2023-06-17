from pydantic import BaseModel
from enum import IntEnum
from typing import List
from datetime import date

class FlagStatus(IntEnum):
    QUEUED = 0
    ACCEPTED = 1
    REJECTED = 2

class ExploitStatus(IntEnum):
    STOPPED = 0
    RUNNING = 1

class Flag(BaseModel):
    flag: str
    run_id: int
    status: FlagStatus = FlagStatus.QUEUED
    checksystem_response: str = ""

    class Config:
        orm_mode = True

class Run(BaseModel):
    id: int
    exploit_id: int
    team_id: int
    start_time: date
    end_time: date
    exitcode: int

    class Config:
        orm_mode = True

class ExploitBase(BaseModel):
    name: str
    threads: int
    timeout: int
    runperiod: int
    source: str

class Exploit(ExploitBase):
    id: int

    class Config:
        orm_mode = True

class ExploitTeams(BaseModel):
    ids: List[int]

class TeamBase(BaseModel):
    name: str
    ip: str

class Team(TeamBase):
    id: int

    class Config:
        orm_mode = True

class FlagStatsAllTime(BaseModel):
    total: int
    queued: int
    accepted: int
    rejected: int

    class Config:
        orm_mode = True

class FlagStatsPerTick(BaseModel):
    total: int
    queued: int
    accepted: int
    rejected: int
    tick_start: int

    class Config:
        orm_mode = True

class FlagStatsPerTickTeam(FlagStatsPerTick):
    team: int