#! /usr/bin/env python3
# vim:fenc=utf-8
#
# Copyright © 2024 shih <shih@fedora>
#
# Distributed under terms of the MIT license.
import asyncio
from util import delay


async def hello_every_sec():
    for i in range(2):
        await asyncio.sleep(1)
        print("I'm running other code while I'm waiting!")


async def main():
    deley_3sec = asyncio.create_task(delay(3))
    deley_3sec1 = asyncio.create_task(delay(3))
    await hello_every_sec()
    await deley_3sec
    await deley_3sec1


if __name__ == "__main__":
    asyncio.run(main())
