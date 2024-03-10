import string, random, asyncpg, asyncio

async def create():
    conn = await asyncpg.connect(user='postgres', password='uchebnick', database='postgres', host='127.0.0.1')
    doc = await conn.fetch('''
    CREATE TABLE IF NOT EXISTS document (
        id char(256) NOT NULL,
        user_name VARCHAR(100),
        file_path TEXT NOT NULL
    )
    ''')

asyncio.run(create())

async def get_file(id):
    conn = await asyncpg.connect(user='postgres', password='uchebnick', database='postgres', host='127.0.0.1')
    doc = await conn.fetch('SELECT file_path, user_name FROM document WHERE id = $1', id)
    doc = doc[0]
    return (doc["file_path"], doc["user_name"])


async def insert_file(id, name, file_path):
    conn = await asyncpg.connect(user='postgres', password='uchebnick', database='postgres', host='127.0.0.1')
    await conn.fetch('INSERT INTO document VALUES ($1, $2, $3)', id, name, file_path)
