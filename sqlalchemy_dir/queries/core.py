import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from sqlalchemy import text,insert
from sqlalchemy_dir.database import sync_engine, async_engine
from sqlalchemy_dir.models import metadata_obj,workers_table

def get_123():
    with sync_engine.connect() as conn:
        res = conn.execute(text("SELECT 1,2,3 union select 4,5,6"))
        print(f"{res.first()=}")


async def get_123_async():
    async with async_engine.connect() as conn:
        res = await conn.execute(text("SELECT 1,2,3 union select 4,5,6"))
        print(f"{res.first()=}")

def create_table():
    sync_engine.echo = False
    metadata_obj.drop_all(sync_engine)
    metadata_obj.create_all(sync_engine)
    sync_engine.echo = True

# Асинхронный вариант, не показанный в видео
async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(metadata_obj.drop_all)
        await conn.run_sync(metadata_obj.create_all)
def insert_data():
    with sync_engine.connect() as conn:
        # stmt = """INSERT INTO workers (username) VALUES
        # ('Bobr'),
        # ('Volk');"""
        stmt = insert(workers_table).values(
            [
                {"username": "Bobr"},
                {"username": "Volk"},
            ]
        )
        conn.execute(stmt)
        conn.commit()


# asyncio.run(get_123_async())
