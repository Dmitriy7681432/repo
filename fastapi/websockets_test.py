import asyncio
import websockets

async def echo(websocket, path):
    async for message in websocket:
        await websocket.send(message)

start_server = websockets.serve(echo, "localhost", 8001)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()


async def connect_to_server():
    async with websockets.connect("ws://localhost:8765") as websocket:
        await websocket.send("Hello, Server!")
        response = await websocket.recv()
        print(f"Received: {response}")

asyncio.get_event_loop().run_until_complete(connect_to_server())