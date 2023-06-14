from flask import jsonify, render_template, request

from server import app
import server.database.database as database

@app.route('/teams', methods=['GET'])
#@auth.auth_required
def teams():
    teams = database.query("SELECT * FROM teams")

    teams = [{"id": item["id"], "name": item["name"], "ip": item["ip"]} for item in teams]

    return render_template('teams.html', teams=teams)
    
@app.route('/teams/<int:uid>', methods=['GET'])
#@auth.auth_required
def teams_get(uid: int):
    item = database.query("SELECT * FROM teams WHERE id = %s", (uid,))

    if len(item) > 0:
        return jsonify({"id": item[0]["id"], "name": item[0]["name"], "ip": item[0]["ip"]}), 200
    else:
        return jsonify({"message": "not found"}), 404


@app.route('/teams', methods=['POST'])
def teams_add():
    if request.json["name"] == "" or request.json["ip"] == "":
        return jsonify({"message": "invalid data"}), 400

    conn = database.get()

    cursor = conn.cursor(dictionary=True, buffered=True)
    cursor.execute("INSERT INTO teams (name, ip) VALUES (%s, %s)", (request.json["name"], request.json["ip"]))
    conn.commit()

    return jsonify({"id": cursor.lastrowid}), 200

@app.route('/teams/<int:uid>', methods=['PATCH'])
def teams_edit(uid: int):
    if request.json["name"] == "" or request.json["ip"] == "":
        return jsonify({"message": "invalid data"}), 400

    conn = database.get()

    cursor = conn.cursor(dictionary=True, buffered=True)
    cursor.execute("UPDATE teams SET name = %s, ip = %s WHERE id = %s", (request.json["name"], request.json["ip"], uid))
    conn.commit()

    return jsonify({}), 204

@app.route('/teams/<int:uid>', methods=['DELETE'])
def teams_delete(uid: int):
    conn = database.get()

    cursor = conn.cursor(dictionary=True, buffered=True)
    cursor.execute("UPDATE teams SET deleted = 1 WHERE id = %s", (uid,))
    conn.commit()

    return jsonify({}), 204