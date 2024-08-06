import os
import asyncio
from asyncio import AbstractEventLoop
from concurrent.futures import ProcessPoolExecutor
from functools import partial
from typing import List
from util import timed

cur_dir = os.path.dirname(os.path.abspath(__file__))


@timed
def count(count_to: int) -> int:
    counter = 0
    while counter < count_to:
        counter += 1
    if count_to % 3 == 0:
        raise Exception("count_to is not divisible by 3")
    return counter


async def main():
    with ProcessPoolExecutor() as pool:
        loop: AbstractEventLoop = asyncio.get_running_loop()
        nums = [1, 2, 5, 21, 100_000_000]
        calls: List[partial[int]] = [partial(count, num) for num in nums]
        call_coros = []
        for call in calls:
            call_coros.append(loop.run_in_executor(pool, call))

        results = await asyncio.gather(*call_coros, return_exceptions=True)
        for result in results:
            if isinstance(result, Exception):
                print(f"catch exception: {result}")
            else:
                print(f"result: {result}")


if __name__ == '__main__':
    asyncio.run(main())
