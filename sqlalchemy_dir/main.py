# import os
import sys
# sys.path.insert(1, os.path.join(sys.path[0], '..'))

from queries.core import SyncCore,AsyncCore
from queries.orm import SyncORM,AsyncORM
import asyncio


async def main():
    # ========== SYNC ==========
    # CORE
    if "--core" in sys.argv and "--sync" in sys.argv:
        SyncCore.create_table()
        SyncCore.insert_workers()
        SyncCore.select_workers()
        SyncCore.update_worker()
        SyncCore.insert_resumes()
        SyncCore.select_resumes_avg_compensation()
        SyncCore.insert_additional_resumes()
        SyncCore.join_cte_subquery_window_func()

    # ORM
    if "--orm" in sys.argv and "--sync" in sys.argv:
        SyncORM.create_table()
        SyncORM.insert_workers()
        SyncORM.select_workers()
        SyncORM.update_worker()
        SyncORM.insert_resumes()
        SyncORM.select_resumes_avg_compensation()
        SyncORM.insert_additional_resumes()
        SyncORM.join_cte_subquery_window_func()
        SyncORM.select_workers_with_lazy_relationship()
        SyncORM.select_workers_with_joined_relationship()
        SyncORM.select_workers_with_selection_relationship()
        SyncORM.select_workers_with_condition_relationship()
        SyncORM.select_workers_with_condition_relationship_contains_eager()
        SyncORM.select_workers_with_relationship_contains_eager_with_limit()

    # ========== ASYNC ==========
    # CORE
    if "--core" in sys.argv and "--async" in sys.argv:
        await AsyncCore.create_tables()
        await AsyncCore.insert_workers()
        await AsyncCore.select_workers()
        await AsyncCore.update_worker()
        await AsyncCore.insert_resumes()
        await AsyncCore.select_resumes_avg_compensation()
        await AsyncCore.insert_additional_resumes()
        await AsyncCore.join_cte_subquery_window_func()

    # ORM
    if "--orm" in sys.argv and "--async" in sys.argv:
        await AsyncORM.create_tables()
        await AsyncORM.insert_workers()
        await AsyncORM.select_workers()
        await AsyncORM.update_worker()
        await AsyncORM.insert_resumes()
        await AsyncORM.select_resumes_avg_compensation()
        await AsyncORM.insert_additional_resumes()
        await AsyncORM.join_cte_subquery_window_func()


if __name__ == "__main__":
    asyncio.run(main())
