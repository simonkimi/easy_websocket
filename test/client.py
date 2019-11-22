import asyncio
from easy_websocket import EasyClient
from websockets import WebSocketCommonProtocol

client = EasyClient('ws://localhost:5678')


@client.init_event()
async def auth(websocket: WebSocketCommonProtocol):
    await websocket.send("123456")
    msg = await websocket.recv()
    if msg != "ok":
        await websocket.close(code=1008)


@client.event()
async def on_message(websocket: WebSocketCommonProtocol):
    while True:
        msg = await websocket.recv()
        print(f"Client get message: {msg}")


@client.event()
async def heartbeat(websocket: WebSocketCommonProtocol):
    while True:
        await websocket.send("Heartbeat")
        await asyncio.sleep(5)


client.start()
