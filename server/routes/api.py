from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text

from server.app import app

from server.database.connection import get_db
from server.database.models import Team

#from server.runner import runner

@app.get("/")
def read_root(db: Session = Depends(get_db)):
    #result = db.execute(text("INSERT INTO teams (name, ip) VALUE ('test', 'lmao')"))
    #db.commit()

    result = db.execute(text("SELECT * FROM teams"))
    return Team.from_orm(result.fetchall())

#@app.route('/api/test2', methods=['GET'])
##@auth.auth_required
#def test2():
#    flags = database.query("SELECT * FROM flags")
#
#    return jsonify(flags)