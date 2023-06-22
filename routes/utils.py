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
    db.execute(text("DELETE FROM teams"))
    #db.commit()
    a = [
    "0, TEAM_NOP",
    "1, Accademia Aeronautica di Pozzuoli",
    "2, Alma Mater Studiorum - Università di Bologna",
    "3, Centro di Competenza in Cybersecurity Toscano",
    "4, Comando per la Formazione e Scuola di Applicazione dell'Esercito",
    "5, Libera Università di Bolzano",
    "6, Politecnico di Bari",
    "7, Politecnico di Milano",
    "8, Politecnico di Torino",
    "9, Sapienza Università di Roma",
    "10, Università Ca' Foscari Venezia",
    "11, Università Campus Bio-Medico di Roma",
    "12, Università degli Studi della Campania Luigi Vanvitelli",
    "13, Università degli Studi dell'Aquila",
    "14, Università degli Studi dell'Insubria",
    "15, Università degli Studi di Bari Aldo Moro",
    "16, Università degli Studi di Brescia",
    "17, Università degli Studi di Cagliari",
    "18, Università degli Studi di Camerino",
    "19, Università degli studi di Cassino e del Lazio Meridionale",
    "20, Università degli Studi di Catania",
    "21, Università degli Studi di Ferrara",
    "22, Università degli Studi di Genova",
    "23, Università degli Studi di Messina",
    "24, Università degli Studi di Milano",
    "25, Università degli Studi di Milano-Bicocca",
    "26, Università degli Studi di Padova",
    "27, Università degli Studi di Palermo",
    "28, Università degli Studi di Parma",
    "29, Università degli Studi di Perugia",
    "30, Università degli Studi di Salerno",
    "31, Università degli Studi di Trento",
    "32, Università degli Studi di Udine",
    "33, Università degli Studi di Verona",
    "34, Università degli Studi 'Gabriele d'Annunzio'",
    "35, Università degli Studi Roma Tre",
    "36, Università della Calabria",
    "37, Università del Salento",
    "38, Università di Modena e Reggio Emilia",
    "39, Università di Napoli",
    "40, Università di Pisa",
    "41, Università di Torino",
    "42, Università Mediterranea di Reggio Calabria",
    "43, Università Politecnica delle Marche"
    ]

    for team in a:
        split = team.split(", ")
        ip = f"10.60.{split[0]}.1"
        db.execute(text("INSERT INTO teams (name, ip) VALUE (:name, :ip)"), { "name": split[1], "ip": ip})

    db.commit()

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