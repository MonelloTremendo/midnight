"""
Module with SQLite helpers, see http://flask.pocoo.org/docs/0.12/patterns/sqlite3/
"""

import os
from mysql.connector import connect


def get():
    database = connect(
        host="localhost",
        user="root",
        password="midnight",
        database="midnight",
    )
    
    return database

def query(sql, args=()):
    conn = get()

    with conn.cursor(dictionary=True, buffered=True) as cursor:
        cursor.execute(sql, args)
        return cursor.fetchall()