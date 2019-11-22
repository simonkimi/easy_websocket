import asyncio
import websockets
from websockets import WebSocketCommonProtocol
from abc import abstractmethod


class WebsocketBase:
    def __init__(self):
        self.websocket: WebSocketCommonProtocol
        self._async_event = []
        self._async_init_event = []

    @abstractmethod
    async def _init(self, *args, **kwargs):
        pass

    @abstractmethod
    def start(self):
        pass

    def init_event(self, index=99):
        def inner(func):
            self._async_init_event.append({
                "index": index,
                "func": func
            })
        return inner

    def event(self):
        def inner(func):
            self._async_event.append(func)

        return inner

    async def _start_websocket(self, websocket):
        self.websocket = websocket
        self._async_init_event.sort(key=lambda x: x["index"])
        for i in self._async_init_event:
            await i["func"](self.websocket)

        tasks = [asyncio.ensure_future(i(websocket)) for i in self._async_event]
        await asyncio.wait(tasks)


class EasyClient(WebsocketBase):
    def __init__(self, uri):
        super().__init__()
        self.uri = uri

    async def _init(self):
        async with websockets.connect(self.uri) as websocket:
            await self._start_websocket(websocket)

    def start(self):
        asyncio.get_event_loop().run_until_complete(self._init())


class EasyServer(WebsocketBase):
    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port

    async def _init(self, websocket, path):
        await self._start_websocket(websocket)

    def start(self):
        start_server = websockets.serve(self._init, self.host, self.port)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()
