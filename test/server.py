import asyncio
import time
from easy_websocket import EasyServer
from websockets import WebSocketCommonProtocol

server = EasyServer("localhost", 5678)


@server.init_event()
async def auth(websocket: WebSocketCommonProtocol):
    token = await websocket.recv()
    if token != "123456":
        await websocket.send("error")
        await websocket.close(code=1008, reason="token not expected")
    else:
        await websocket.send("ok")


@server.event()
async def on_message(websocket: WebSocketCommonProtocol):
    while True:
        msg = await websocket.recv()
        print(f"Server get message: {msg}")


@server.event()
async def send_time(websocket: WebSocketCommonProtocol):
    while True:
        await websocket.send(str(time.time()))
        await asyncio.sleep(1)

server.start()
