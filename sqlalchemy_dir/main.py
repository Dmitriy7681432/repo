# import os
# import sys
# sys.path.insert(1, os.path.join(sys.path[0], '..'))

from queries.core import SyncCore,AsyncCore
from queries.orm import SyncORM,AsyncORM
import asyncio

SyncORM.create_table()
# SyncCore.create_table()

SyncORM.insert_workers()
# SyncCore.insert_workers()

# SyncCore.select_workers()
# SyncCore.update_worker()

# SyncORM.select_workers()
# SyncORM.update_worker()

