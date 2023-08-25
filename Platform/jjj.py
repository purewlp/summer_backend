import asyncio
import websockets

async def connect():
    async with websockets.connect('ws://localhost:8000/chat/message/text/') as websocket:
        await websocket.send('Hello, server!')
        response = await websocket.recv()
        print(response)

asyncio.get_event_loop().run_until_complete(connect())
