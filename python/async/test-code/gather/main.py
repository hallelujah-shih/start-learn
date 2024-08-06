import asyncio
import logging
from aiohttp import ClientSession
from util import async_timed, fetch_status
from mlog import get_logger

_logger = get_logger(__name__)


@async_timed()
async def main():
    async with ClientSession() as session:
        urls = ['http://www.ahhhbbb.com/' for _ in range(3)]
        requests = [fetch_status(session, url) for url in urls]
        status_codes = await asyncio.gather(*requests, return_exceptions=True)
        for status_code in status_codes:
            if isinstance(status_code, Exception):
                _logger.info(f"gather err: {status_code}")
            else:
                _logger.info(f"gather result: {status_code}")

    print("------------------------split with gather----------------------------")

    async with ClientSession() as session:
        urls = ['http://www.knownsec.com/', 'http://ahhh.com/', 'https://www.baidu.com/']
        fetchers = [fetch_status(session, url) for url in urls]
        for rt in asyncio.as_completed(fetchers):
            try:
                result = await rt
                _logger.info(result)
            except Exception as ex:
                _logger.info(f"catch exception: {ex}")

    print("------------------------split with as_completed----------------------------")
    async with ClientSession() as session:
        urls = ['http://www.knownsec.com/', 'http://ahhh.com/', 'https://www.baidu.com/']
        ftasks = [asyncio.create_task(fetch_status(session, urls[0], delay_ts=2)),
                    asyncio.create_task(fetch_status(session, urls[1], delay_ts=0.5)),
                    asyncio.create_task(fetch_status(session, urls[2], delay_ts=5))]
        done, pending = await asyncio.wait(ftasks, return_when=asyncio.FIRST_COMPLETED)
        _logger.info(f"done: {len(done)}")
        for task in done:
            if task.exception() is not None:
                _logger.info(f"task exception: {task.exception()}")
            else:
                _logger.info(f"task: {task.result()}")
        _logger.info(f"pending: {len(pending)}")
        for task in pending:
            task.cancel()
        done, pending = await asyncio.wait(pending)
        _logger.info(f"cancel done: {len(done)}")
        _logger.info(f"cancel pending: {len(pending)}")
        for task in done:
            if task.cancelled():
                _logger.info(f"cancel task: {task}")
            else:
                if task.exception() is not None:
                    _logger.info(f"cancel task exception: {task.exception()}")
                else:
                    _logger.info(f"cancel task: {task.result()}")


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)
    asyncio.run(main())
