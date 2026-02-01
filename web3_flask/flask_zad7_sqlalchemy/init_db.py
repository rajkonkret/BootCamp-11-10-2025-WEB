import sqlite3

try:
    conn = sqlite3.connect("data/car_ads_portal.db")
    c = conn.cursor()

    query = """
    CREATE TABLE IF NOT EXISTS offers (
    id INTEGER PRIMARY KEY,
    brand TEXT,
    price INTEGER,
    user TEXT);
    """

    c.execute(query)
    conn.commit()
except sqlite3.Error as e:
    print("Bład bazy:", e)
finally:
    if conn:
        conn.close()
