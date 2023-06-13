from flask import jsonify, render_template, request

from server import app
import server.database.database as database

from server.runner import runner

@app.route('/api/test', methods=['GET'])
#@auth.auth_required
def test():
    src = """
#!/usr/bin/env python3

print("A"*31 + "=")
""".strip()

    test = runner.Exploit(1, 16, 60, src, {})

    return jsonify({})