#! /usr/bin/env python3
# vim:fenc=utf-8
#
# Copyright © 2024 shih <shih@fedora>
#
# Distributed under terms of the MIT license.
import asyncio
import time
import functools
from typing import Callable, Any
from aiohttp import ClientSession
from mlog import get_logger

_logger = get_logger(__name__)


async def delay(delay_seconds: float) -> float:
    _logger.info(f'sleep for {delay_seconds} second(s)')
    await asyncio.sleep(delay_seconds)
    _logger.info(f'finished sleep for {delay_seconds} second(s)')
    return delay_seconds


def async_timed():
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapped(*args, **kwargs) -> Any:
            _logger.info(f'starting {func} with args {args} {kwargs}')
            start = time.time()
            try:
                return await func(*args, **kwargs)
            finally:
                end = time.time()
                total = end - start
                _logger.info(f'finished {func} in {total:.4f} second(s)')
        return wrapped
    return wrapper


def timed(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start = time.time()
        try:
            return func(*args, **kwargs)
        finally:
            _logger.info(f'finished {func} in {time.time()-start:.4f} second(s)')
    return wrapper


@async_timed()
async def fetch_status(session: ClientSession, url: str, delay_ts: float = 0) -> int:
    if delay_ts > 0:
        await delay(delay_ts)

    async with session.get(url) as result:
        return result.status
