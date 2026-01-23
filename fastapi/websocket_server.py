# -*- coding: utf-8 -*-
import asyncio
import websockets

async def echo(websocket):
    print(f"Клиент подключился: {websocket.remote_address}")
    async for message in websocket:
        print(f"Получено от клиента: {message}")
        await websocket.send(f"Сервер получил: {message}")
    print(f"Клиент отключился: {websocket.remote_address}")

async def main():
    # Запускаем сервер на localhost по порту 8765
    async with websockets.serve(echo, "localhost", 8765) as server:
        print("WebSocket сервер запущен на ws://localhost:8765")
        await asyncio.Future()  # Держим сервер в работе

if __name__ == "__main__":
    asyncio.run(main())
