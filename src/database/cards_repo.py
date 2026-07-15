import aiosqlite
from ..config import DB_NAME

async def get_all_cards():
    async with aiosqlite.connect(DB_NAME) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute('SELECT * FROM cards ORDER BY created_at')
        cards = await cursor.fetchall()
        return cards

async def add_card(column_id, title, description="", color="transparent", priority=1, tags="[]", due_date=None, assignee=None):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            '''INSERT INTO cards 
            (column_id, title, description, color, priority, tags, due_date, assignee) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
            (column_id, title, description, color, priority, tags, due_date, assignee)
        )
        await db.commit()
        return cursor.lastrowid

async def update_card_column(card_id, new_column_id):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('UPDATE cards SET column_id = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?', (new_column_id, card_id))
        await db.commit()

async def update_card_details(card_id, title, description, color, priority=1, tags="[]", due_date=None, assignee=None):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            '''UPDATE cards SET title = ?, description = ?, color = ?, priority = ?, tags = ?, due_date = ?, assignee = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?''',
            (title, description, color, priority, tags, due_date, assignee, card_id)
        )
        await db.commit()

async def delete_card(card_id):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('DELETE FROM cards WHERE id = ?', (card_id,))
        await db.commit()

async def get_card_stats():
    async with aiosqlite.connect(DB_NAME) as db:
        db.row_factory = aiosqlite.Row
        total = await db.execute('SELECT COUNT(*) FROM cards')
        total_count = (await total.fetchone())[0]

        by_priority = await db.execute('SELECT priority, COUNT(*) as count FROM cards GROUP BY priority')
        priority_stats = await by_priority.fetchall()

        by_color = await db.execute('SELECT color, COUNT(*) as count FROM cards WHERE color != "transparent" GROUP BY color')
        color_stats = await by_color.fetchall()

        return {"total": total_count, "priority": priority_stats, "color": color_stats}
