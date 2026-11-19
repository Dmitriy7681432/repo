# -*- coding: utf-8 -*-
import asyncio
import websockets

async def hello():
    # Подключаемся к нашему локальному серверу
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        print(f"Подключено к {uri}")

        # Отправляем сообщения
        await websocket.send("Привет, мир!")
        print("Отправлено: Привет, мир!")
        response = await websocket.recv()
        print(f"Получено от сервера: {response}")

        await websocket.send("Как дела?")
        print("Отправлено: Как дела?")
        response = await websocket.recv()
        print(f"Получено от сервера: {response}")

if __name__ == "__main__":
    asyncio.run(hello())
