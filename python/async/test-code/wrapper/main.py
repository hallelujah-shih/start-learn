#! /usr/bin/env python3
# vim:fenc=utf-8
#
# Copyright © 2024 shih <shih@fedora>
#
# Distributed under terms of the MIT license.
import asyncio
from util import async_timed


@async_timed()
async def delay(delay_ts: float) -> float:
    print(f'sleeping for {delay_ts:.4f} s')
    await asyncio.sleep(delay_ts)
    print(f'finished sleeping for {delay_ts:.4f} s')
    return delay_ts


def call_later():
    print("I'm beging called in the future!")


@async_timed()
async def main():
    task_1 = asyncio.create_task(delay(2))
    task_2 = asyncio.create_task(delay(3))
    await asyncio.gather(task_1, task_2, return_exceptions=True)

    loop = asyncio.get_running_loop()
    loop.call_soon(call_later)
    await delay(1)


if __name__ == '__main__':
    asyncio.run(main(), debug=True)
