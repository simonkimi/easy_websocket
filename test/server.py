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
