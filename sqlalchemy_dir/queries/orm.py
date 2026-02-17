import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from sqlalchemy import text,insert,select
from sqlalchemy_dir.database import sync_engine, async_engine, session_factory,async_session_factory
from sqlalchemy_dir.models import WorkerOrm,Base



class SyncORM:
    @staticmethod
    def create_table():
        sync_engine.echo = True
        Base.metadata.drop_all(sync_engine)
        Base.metadata.create_all(sync_engine)
        sync_engine.echo = True
    @staticmethod
    def insert_workers():
        with session_factory() as session:
            worker_bobr = WorkerOrm(username="Bobr")
            worker_volk = WorkerOrm(username="Volk")
            session.add_all([worker_bobr,worker_volk])
            session.flush()
            session.commit()
    @staticmethod
    def select_workers():
        with session_factory() as session:
            query = select(WorkerOrm)
            result = session.execute(query)
            workers = result.scalars().all()
            print(f"{workers=}")



    @staticmethod
    def update_worker(worker_id: int=2, new_username: str = "Misha"):
        with session_factory() as session:
            worker_bob = session.get(WorkerOrm,worker_id)
            worker_bob.username = new_username
            session.refresh(worker_bob)
            session.commit()


class AsyncORM:
    # Асинхронный вариант, не показанный в видео
    @staticmethod
    async def create_tables():
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    @staticmethod
    async def insert_data():
        async with async_session_factory() as session:
            worker_bobr = WorkerOrm(username="Bobr")
            worker_volk = WorkerOrm(username="Volk")
            session.add_all([worker_bobr,worker_volk])
            await session.commit()
