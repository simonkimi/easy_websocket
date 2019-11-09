import asyncio
from easy_websocket import EasyClient


class Client(EasyClient):
    def __init__(self, uri):
        super().__init__(uri)

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
