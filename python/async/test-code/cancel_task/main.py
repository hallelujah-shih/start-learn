#! /usr/bin/env python3
# vim:fenc=utf-8
#
# Copyright © 2024 shih <shih@fedora>
#
# Distributed under terms of the MIT license.
import asyncio
from asyncio import CancelledError
from util import delay


async def main():
    long_task = asyncio.create_task(delay(10))

    seconds_elapsed = 0

    while not long_task.done():
        print('task not finished, checking again in a sec')
        await asyncio.sleep(1)
        seconds_elapsed = seconds_elapsed + 1
        if seconds_elapsed == 5:
            long_task.cancel()

    try:
        await long_task
    except CancelledError as e:
        print("long_task was cancelled")


if __name__ == '__main__':
    asyncio.run(main())
