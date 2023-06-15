from server.app import app

#from server.database import database
#from server.runner import runner

@app.get("/")
def read_root():
    return {"Hello": "World"}

#@app.route('/api/test2', methods=['GET'])
##@auth.auth_required
#def test2():
#    flags = database.query("SELECT * FROM flags")
#
#    return jsonify(flags)