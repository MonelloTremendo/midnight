from flask import jsonify, render_template, request

from server import app
import server.database.database as database

from server.runner import runner

@app.route('/api/test', methods=['GET'])
#@auth.auth_required
def test():
    runner.ExploitRunner().execute_scripts()

    return jsonify({"message": 2})