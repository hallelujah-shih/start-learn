#! /usr/bin/env python3
# vim:fenc=utf-8
#
# Copyright © 2024 shih <shih@fedora>
#
# Distributed under terms of the MIT license.
import asyncio
from util import delay


async def main():
    sleep1 = asyncio.create_task(delay(3))
    sleep2 = asyncio.create_task(delay(3))
    sleep3 = asyncio.create_task(delay(3))

    await sleep1
    await sleep2
    await sleep3


if __name__ == '__main__':
    asyncio.run(main())
