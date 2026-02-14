import sqlite3


def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE
    """)

    conn.commit()
    conn.close()


def get_user(email):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute("""
    SELECT id, email FROM users WHERE email=?
    """, (email,))
    user = c.fetchone()

    # conn.commit()
    conn.close()
    return user


def add_user():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    conn.commit()
    conn.close()
