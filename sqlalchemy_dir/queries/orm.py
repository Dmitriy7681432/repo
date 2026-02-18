# -*- coding: utf-8 -*-
import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], '..'))

from sqlalchemy import text, insert, select,func,cast,Integer,and_
from sqlalchemy_dir.database import sync_engine, async_engine, session_factory, async_session_factory
from sqlalchemy_dir.models import WorkerOrm, Base, ResumesOrm,Workload


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
            session.add_all([worker_bobr, worker_volk])
            # flush отправляет запрос в базу данных после flush каждый
            # из работников получает первичный ключ id, который отдала БД
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
    def update_worker(worker_id: int = 2, new_username: str = "Misha"):
        with session_factory() as session:
            worker_bob = session.get(WorkerOrm, worker_id)
            worker_bob.username = new_username
            session.refresh(worker_bob)
            session.commit()

    @staticmethod
    def insert_resumes():
        with session_factory() as session:
            resumes_bobr_1 = ResumesOrm(title='Python Junior Developer',
                compensation=50000, workload=Workload.fulltime, worker_id=1)
            resumes_bobr_2 = ResumesOrm(title='Python Разработчик',
                compensation=150000, workload=Workload.fulltime, worker_id=1)
            resumes_misha_1 = ResumesOrm(title='Python Data Engineer',
                compensation=250000, workload=Workload.parttime, worker_id=2)
            resumes_misha_2 = ResumesOrm(title='Data Scientist',
                compensation=300000, workload=Workload.fulltime, worker_id=2)
            session.add_all([resumes_bobr_1,resumes_bobr_2,resumes_misha_1,
                             resumes_misha_2])
            session.commit()
            sync_engine.echo = True
    @staticmethod
    def select_resumes_avg_compensation(like_language: str = "Python"):
        # Это запрос опишем с помощью sqlalchemy
        """
        select workload, avg(compensation) as avg_compensation
        from resumes
        where title like '%Python%' and compensation > 40000
        group by workload
        """
        with session_factory() as session:
            query = (
                select(
                    ResumesOrm.workload,
                    cast(func.avg(ResumesOrm.compensation),Integer)
                      .label("avg_compensation"),
                )
                .select_from(ResumesOrm)
                .filter(and_(
                    ResumesOrm.title.contains(like_language),
                    ResumesOrm.compensation > 40000,
                ))
                .group_by(ResumesOrm.workload)
                .having(cast(func.avg(ResumesOrm.compensation), Integer) > 70000)
            )
            # Преобразовать в читаемый sql запрос
            print(query.compile(compile_kwargs={"literal_binds": True}))
            res = session.execute(query)
            result = res.all()
            print(result)
            print(result[0].avg_compensation)
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
            session.add_all([worker_bobr, worker_volk])
            await session.commit()
