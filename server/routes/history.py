from flask import render_template
from server import app

@app.route('/history')
def history():
    exploits = [
        {'id': 1,'name': 'EXPLOIT 1','author': 'gg',},
        {'id': 2,'name': 'EXPLOIT 2','author': 'gabibbo',},
        {'id': 3,'name': 'skill issues','author': 'mr96',},
        {'id': 3,'name': 'skill issues','author': 'mr96',},
        {'id': 3,'name': 'skill issues','author': 'mr96',},
        {'id': 3,'name': 'skill issues','author': 'mr96',},
        {'id': 3,'name': 'skill issues','author': 'mr96',},
        {'id': 3,'name': 'skill issues','author': 'mr96',},
        {'id': 3,'name': 'skill issues','author': 'mr96',},
        {'id': 3,'name': 'skill issues','author': 'mr96',},
        {'id': 3,'name': 'skill issues','author': 'mr96',},
        {'id': 3,'name': 'skill issues','author': 'mr96',},
        {'id': 3,'name': 'skill issues','author': 'mr96',},
        {'id': 3,'name': 'skill issues','author': 'mr96',},
        {'id': 3,'name': 'skill issues','author': 'mr96',},
        {'id': 3,'name': 'skill issues','author': 'mr96',},
        {'id': 3,'name': 'skill issues','author': 'mr96',},
        {'id': 3,'name': 'skill issues','author': 'mr96',},
        {'id': 3,'name': 'skill issues','author': 'mr96',},
        {'id': 3,'name': 'skill issues','author': 'mr96',},
        {'id': 3,'name': 'skill issues','author': 'mr96',},
        {'id': 3,'name': 'skill issues','author': 'mr96',},
        {'id': 3,'name': 'skill issues','author': 'mr96',},
        {'id': 3,'name': 'skill issues','author': 'mr96',},
        {'id': 3,'name': 'skill issues','author': 'mr96',},
        {'id': 3,'name': 'skill issues','author': 'mr96',},
        {'id': 3,'name': 'skill issues','author': 'mr96',},
        {'id': 3,'name': 'skill issues','author': 'mr96',},
    ]
    teams = [
        {'id': 1, 'name':'giorgiovanni', 'ip':'10.60.1.1'},
        {'id': 2, 'name':'forzanapoli', 'ip':'10.60.2.1'},
        {'id': 3, 'name':'gg per catania', 'ip':'10.60.3.1'},
    ]
    return render_template('history.html', exploits=exploits, teams=teams)