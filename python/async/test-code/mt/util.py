import asyncio
from concurrent.futures import Future
from asyncio import AbstractEventLoop
from typing import Callable, Optional
from aiohttp import ClientSession, TCPConnector, ClientTimeout


class StressTest:
    def __init__(self, loop: AbstractEventLoop, url: str, total_reqs: int, callback: Callable[[int, int], None]):
        self._completed_reqs: int = 0
        self._load_test_future: Optional[Future] = None
        self._loop = loop
        self._url = url
        self._total_reqs = total_reqs
        self._callback = callback
        self._refresh_rate = total_reqs // 100

    def start(self):
        future = asyncio.run_coroutine_threadsafe(self._make_requests(), self._loop)
        self._load_test_future = future

    def cancel(self):
        if self._load_test_future:
            self._loop.call_soon_threadsafe(self._load_test_future.cancel)

    async def _get_url(self, session: ClientSession, url: str):
        rsp = None
        try:
            rt = await session.get(url)
            rsp = await rt.text()
        except Exception as ex:
            print(ex)
        self._completed_reqs += 1
        if self._completed_reqs % self._refresh_rate == 0 or self._completed_reqs == self._total_reqs:
            self._callback(self._completed_reqs, self._total_reqs)
        return rsp

    async def _make_requests(self):
        conn = TCPConnector(verify_ssl=False, limit=1000)
        async with ClientSession(connector=conn) as session:
            reqs = [self._get_url(session, self._url) for _ in range(self._total_reqs)]
            for item in asyncio.as_completed(reqs):
                print(await item)
            # await asyncio.gather(*reqs)
