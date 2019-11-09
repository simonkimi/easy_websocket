# easy_websocket
## 基于websocket二次封装的websocket异步服务端与客户端

demo：

server.py
```python
import asyncio
import time
from easy_websocket import EasyServer


class Server(EasyServer):
    def __init__(self, host, port):
        super().__init__(host, port)
        
        # add you task here
        self.add_event(self.send_time)

    async def on_message(self, msg):
        print(f"Server get message {msg}")
        await self.websocket.send(f"You send {msg}")

    async def send_time(self):
        while True:
            await self.websocket.send(str(time.time()))
            await asyncio.sleep(1)


if __name__ == "__main__":
    server = Server("localhost", 5678)
    server.start()
```

client.py
```python
import asyncio
from easy_websocket import EasyClient


class Client(EasyClient):
    def __init__(self, host):
        super().__init__(host)

        # add you task here
        self.add_event(self.heartbeat)

    async def on_message(self, msg):
        print(f"Client get message: {msg}")

    async def heartbeat(self):
        while True:
            await self.websocket.send("Heartbeat")
            await asyncio.sleep(5)


if __name__ == "__main__":
    client = Client('ws://localhost:5678')
    client.start()

```