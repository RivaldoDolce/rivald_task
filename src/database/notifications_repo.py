import aiosqlite
from datetime import datetime
from ..config import DB_NAME


async def init_notifications_table():
    async with aiosqlite.connect(DB_NAME) as db:
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
        await db.commit()


async def add_notification(type_, title, message="", priority="info", icon="info"):
    """Ajoute une notification et purge les plus anciennes (>50 entrées)."""
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            '''INSERT INTO notifications (type, priority, title, message, icon)
               VALUES (?, ?, ?, ?, ?)''',
            (type_, priority, title, message, icon)
        )
        # Purge: keep only the latest 50 notifications
        await db.execute(
            '''DELETE FROM notifications WHERE id NOT IN (
                   SELECT id FROM notifications ORDER BY id DESC LIMIT 50
               )'''
        )
        await db.commit()
        return cursor.lastrowid


async def get_all_notifications():
    async with aiosqlite.connect(DB_NAME) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            'SELECT * FROM notifications ORDER BY id DESC LIMIT 50'
        )
        return await cursor.fetchall()


async def mark_all_read():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('UPDATE notifications SET read = 1')
        await db.commit()


async def mark_read(notification_id):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            'UPDATE notifications SET read = 1 WHERE id = ?',
            (notification_id,)
        )
        await db.commit()


async def clear_all_notifications():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('DELETE FROM notifications')
        await db.commit()
