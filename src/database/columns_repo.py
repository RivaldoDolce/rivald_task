import aiosqlite
from ..config import DB_NAME

async def get_all_columns():
    async with aiosqlite.connect(DB_NAME) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute('SELECT * FROM columns ORDER BY position')
        columns = await cursor.fetchall()
        return columns

async def add_column(title, color="#1E293B", position=0):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            'INSERT INTO columns (title, color, position) VALUES (?, ?, ?)',
            (title, color, position)
        )
        await db.commit()
        return cursor.lastrowid

async def update_column_title(col_id, title):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('UPDATE columns SET title = ? WHERE id = ?', (title, col_id))
        await db.commit()

async def delete_column(col_id):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('DELETE FROM cards WHERE column_id = ?', (col_id,))
        await db.execute('DELETE FROM columns WHERE id = ?', (col_id,))
        await db.commit()

async def reorder_columns(ordered_ids):
    """
    Persist the new column order.
    `ordered_ids` is a list of column ids in the desired display order.
    """
    async with aiosqlite.connect(DB_NAME) as db:
        for index, col_id in enumerate(ordered_ids):
            await db.execute(
                'UPDATE columns SET position = ? WHERE id = ?',
                (index, col_id)
            )
        await db.commit()
