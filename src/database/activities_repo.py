import aiosqlite
from ..config import DB_NAME

async def log_activity(card_id, action, details=""):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            'INSERT INTO activities (card_id, action, details) VALUES (?, ?, ?)',
            (card_id, action, details)
        )
        await db.commit()
