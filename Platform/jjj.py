import asyncio
import websockets
import json


async def send_test_message(uri, message):
    async with websockets.connect(uri) as websocket:
        await websocket.send(message)
        response = await websocket.recv()
        print(f"Received response: {response}")


async def main():
    uri = f"ws://43.143.140.26:7002/ws/chat/?roomId=1&userId=2"
    text_message = json.dumps({"text": "@@@"})

    await send_test_message(uri, text_message)


if __name__ == "__main__":
    asyncio.run(main())

