# -*- coding: utf-8 -*-
from fastapi import FastAPI, BackgroundTasks
import asyncio
import time

app = FastAPI()


def sync_task():
    time.sleep(3)
    print("Отправлен email")


async def async_task():
    await asyncio.sleep(1)
    print("Сделан запрос в сторонний API")


@app.post("/")
async def some_route(background_task: BackgroundTasks):
    # asyncio.create_task(async_task())
    background_task.add_task(sync_task)
    return {"ok": True}
