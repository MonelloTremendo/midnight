from flask import render_template
from server import app

@app.route('/background')
def background():
    return render_template('background.html')