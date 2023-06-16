from pydantic import BaseModel
from datetime import date
from typing import Optional

class FlagStatus(BaseModel):
    QUEUED = 0
    SKIPPED = 1
    ACCEPTED = 2
    REJECTED = 3

class ExploitStatus(BaseModel):
    STOPPED = 0
    RUNNING = 1

class Flag(BaseModel):
    flag: str
    run_id: int
    status: FlagStatus
    checksystem_response: str

    class Config:
        orm_mode = True

class Run(BaseModel):
    id: int
    exploit_id: int
    team_id: int
    time: date

    class Config:
        orm_mode = True

class ExploitBase(BaseModel):
    name: str
    threads: int
    timeout: int
    running: ExploitStatus
    source: str

class Exploit(ExploitBase):
    id: int

    class Config:
        orm_mode = True

class TeamBase(BaseModel):
    name: str
    ip: str

class Team(TeamBase):
    id: int

    class Config:
        orm_mode = True