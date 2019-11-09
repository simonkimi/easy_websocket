import asyncio
import websockets
from abc import abstractmethod


class EasyClient:
    def __init__(self, uri):
        self.uri = uri
        self.websocket = None
        self._async_task = []

    async def _init(self):
        async with websockets.connect(self.uri) as websocket:
            self.websocket = websocket

            tasks = [asyncio.ensure_future(i()) for i in self._async_task]
            tasks.append(asyncio.ensure_future(self._on_message()))

            await asyncio.wait(tasks)

    def start(self):
        asyncio.get_event_loop().run_until_complete(self._init())

    async def _on_message(self):
        while True:
            msg = await self.websocket.recv()
            await self.on_message(msg)

    @abstractmethod
    async def on_message(self, msg):
        pass

    def add_event(self, task):
        self._async_task.append(task)


class EasyServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.websocket = None
        self._async_task = []

    async def _init(self, websocket, path):
        self.websocket = websocket

        tasks = [asyncio.ensure_future(i()) for i in self._async_task]
        tasks.append(asyncio.ensure_future(self._on_message()))

        await asyncio.wait(tasks)

    async def _on_message(self):
        while True:
            msg = await self.websocket.recv()
            await self.on_message(msg)

    @abstractmethod
    async def on_message(self, msg):
        pass

    def start(self):
        start_server = websockets.serve(self._init, self.host, self.port)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()

    def add_event(self, task):
        self._async_task.append(task)