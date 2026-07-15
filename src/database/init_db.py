import aiosqlite
from datetime import datetime
from ..config import DB_NAME


async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS columns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                color TEXT DEFAULT "#1E293B",
                position INTEGER DEFAULT 0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        await db.execute('''
            CREATE TABLE IF NOT EXISTS cards (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                column_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                description TEXT,
                color TEXT DEFAULT "transparent",
                priority INTEGER DEFAULT 1,
                tags TEXT DEFAULT "[]",
                due_date TEXT,
                assignee TEXT,
                checklist TEXT DEFAULT "[]",
                attachments INTEGER DEFAULT 0,
                comments_count INTEGER DEFAULT 0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (column_id) REFERENCES columns (id)
            )
        ''')
        await db.execute('''
            CREATE TABLE IF NOT EXISTS activities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                card_id INTEGER,
                action TEXT NOT NULL,
                details TEXT,
                timestamp TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        await db.execute('''
            CREATE TABLE IF NOT EXISTS notifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT NOT NULL,
                priority TEXT DEFAULT 'info',
                title TEXT NOT NULL,
                message TEXT,
                icon TEXT DEFAULT 'info',
                read INTEGER DEFAULT 0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        cursor = await db.execute('SELECT COUNT(*) FROM columns')
        count = (await cursor.fetchone())[0]
        if count == 0:
            default_columns = [
                ("Backlog", "#1E293B", 0),
                ("À faire", "#3B9EFF", 1),
                ("En cours", "#FB923C", 2),
                ("Revue", "#B47CFF", 3),
                ("Terminé", "#4ADE80", 4),
            ]
            await db.executemany(
                'INSERT INTO columns (title, color, position) VALUES (?, ?, ?)',
                default_columns
            )
        await db.commit()
