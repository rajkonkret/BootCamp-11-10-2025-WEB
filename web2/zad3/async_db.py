import aiosqlite

DB_FILE = "async_example.db"


async def init_db():
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL);
        """)
        await db.commit()


async def add_task(title: str):
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute("INSERT INTO tasks (title) VALUES (?);", (title,))
        await db.commit()
