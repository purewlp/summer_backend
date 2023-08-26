import asyncio
import websockets
import json


async def send_test_message(uri, message):
    async with websockets.connect(uri) as websocket:
        await websocket.send(message)
        response = await websocket.recv()
        print(f"Received response: {response}")


async def main():
    uri = f"ws://localhost:8000/ws/chat/?roomId=1&userId=1"
    text_message = json.dumps({"text": "Hello, World!"})

    await send_test_message(uri, text_message)


if __name__ == "__main__":
    asyncio.run(main())

