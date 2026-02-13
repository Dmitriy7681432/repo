import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from sqlalchemy import text,insert
from sqlalchemy_dir.database import sync_engine, async_engine, session_factory,async_session_factory
from sqlalchemy_dir.models import WorkerOrm,Base



def create_table():
    sync_engine.echo = True
    Base.metadata.drop_all(sync_engine)
    Base.metadata.create_all(sync_engine)
    sync_engine.echo = True

# Асинхронный вариант, не показанный в видео
async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

def insert_data():
    with session_factory() as session:
        worker_bobr = WorkerOrm(username="Bobr")
        worker_volk = WorkerOrm(username="Volk")
        session.add_all([worker_bobr,worker_volk])
        session.commit()

async def insert_data():
    async with async_session_factory() as session:
        worker_bobr = WorkerOrm(username="Bobr")
        worker_volk = WorkerOrm(username="Volk")
        session.add_all([worker_bobr,worker_volk])
        await session.commit()
