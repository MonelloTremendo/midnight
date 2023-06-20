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
        use_enum_values = True

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

class FlagStats(BaseModel):
    total: int = 0
    queued: int = 0
    accepted: int = 0
    rejected: int = 0

    class Config:
        orm_mode = True

class FlagStatsPerTick(FlagStats):
    tick_start: int = 0

class FlagStatsPerTickTeam(FlagStatsPerTick):
    team: int

class FlagStatsTeam(FlagStats):
    id: int
    name: str

class FlagsExploitTimestamp(BaseModel):
    id: int
    flags: int

    class Config:
        orm_mode = True