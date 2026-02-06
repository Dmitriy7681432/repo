from sqlalchemy import text
from sqlalchemy_dir.database import sync_engine, async_engine
import asyncio

def get_123():
    with sync_engine.connect() as conn:
        res = conn.execute(text("SELECT 1,2,3 union select 4,5,6"))
        print(f"{res.first()=}")


async def get_123_async():
    async with async_engine.connect() as conn:
        res = await conn.execute(text("SELECT 1,2,3 union select 4,5,6"))
        print(f"{res.first()=}")

# def create_table()


asyncio.run(get_123_async())
