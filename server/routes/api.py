from flask import jsonify, render_template, request

from server import app
import server.database.database as database

from server.runner import runner

@app.route('/api/test', methods=['GET'])
#@auth.auth_required
def test():
    src = """
#!/usr/bin/env python3

import string
import random

print("".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(31)) + "=", flush=True)
""".strip()

    test = runner.Exploit(1, 16, 5, src, [{"id": 1, "ip": "10.60.0.1"}])

    test.run()

    return jsonify({})

@app.route('/api/test2', methods=['GET'])
#@auth.auth_required
def test2():
    flags = database.query("SELECT * FROM flags")

    return jsonify(flags)