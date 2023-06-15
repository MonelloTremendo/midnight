from pydantic import BaseModel
from datetime import date

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

class Exploit(BaseModel):
    id: int
    name: str
    threads: int
    timeout: int
    running: ExploitStatus
    source: str

    class Config:
        orm_mode = True

class Team(BaseModel):
    id: int
    name: str
    ip: str

    class Config:
        orm_mode = True