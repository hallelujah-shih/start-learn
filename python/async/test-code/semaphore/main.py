import asyncio
import logging
from asyncio import Semaphore
from mlog import get_logger
from util import delay

_logger = get_logger(__name__)


async def operation(semaphore: Semaphore):
    _logger.info("waiting for semaphore")
    async with semaphore:
        _logger.info("acquired semaphore")
        await delay(1)
    _logger.info("released semaphore")


async def main():
    smf = Semaphore(2)
    await asyncio.gather(*[operation(smf) for _ in range(10)])
    _logger.info("done")


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    asyncio.run(main())
