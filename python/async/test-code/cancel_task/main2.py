#! /usr/bin/env python3
# vim:fenc=utf-8
#
# Copyright © 2024 shih <shih@fedora>
#
# Distributed under terms of the MIT license.
import asyncio
from util import delay


async def main():
    task = asyncio.create_task(delay(10))

    try:
        result = await asyncio.wait_for(asyncio.shield(task), timeout=5)
        print(result)
    except asyncio.exceptions.TimeoutError:
        print("Task took longer than five secs, it will finish soon")
        result = await task
        print(result)


if __name__ == "__main__":
    asyncio.run(main())
