import sqlite3

import bcrypt

SCHEMA_PATH = "data/schema.sql"
DB_PATH = "data/car_ads_portal.db"


def add_table_users():
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        print("Połączono z bazą danych")

        with open(SCHEMA_PATH, "r") as f:
            schema = f.read()
            conn.executescript(schema)
        print("Tabela users zostałą utworzona")

    except sqlite3.Error as e:
        print("Bład:", e)
    finally:
        if conn:
            conn.close()
            print("Baza została zamknięta")


def create_start_user():
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        print("Połączono z bazą danych")

        insert = """
        INSERT INTO users (name, email, password, is_active, is_admin)
        VALUES (?,?,?,?,?);
        """
        password = "admin123"
        password_hash = (bcrypt.hashpw(password.encode('utf-8'),
                                       bcrypt.gensalt())
                         .decode('utf-8'))

        cur.execute(insert, ('admin1', 'admin1@caradsportal.pl', password_hash, 1, 1))
        conn.commit()
        print("Użytkownik admin dodany, hasło admin123")

    except sqlite3.Error as e:
        print("Bład:", e)
    finally:
        if conn:
            conn.close()
            print("Baza została zamknięta")


if __name__ == '__main__':
    add_table_users()
    create_start_user()
