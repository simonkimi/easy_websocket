# easy_websocket
## 基于python和websockets二次封装的异步服务端与客户端

demo：

server.py
```python
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

```

client.py
```python
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

```