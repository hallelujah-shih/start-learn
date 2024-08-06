import asyncio
import functools
import logging
from asyncio import Event
from contextlib import suppress
from mlog import get_logger
from util import delay

_logger = get_logger(__name__)


async def trigger_event_periodically(event: Event):
    while True:
        _logger.info("triggering event!")
        event.set()
        await asyncio.sleep(1)


async def do_work_on_event(event: Event, worker_num: int):
    while True:
        _logger.info(f"wrk:{worker_num} waiting for event...")
        await event.wait()
        event.clear()
        _logger.info(f"wrk:{worker_num} doing work!")
        await delay(5)
        _logger.info(f"wrk:{worker_num} work done!")


async def main():
    event = Event()
    trigger = asyncio.wait_for(trigger_event_periodically(event), 5.0)
    with suppress(asyncio.TimeoutError):
        await asyncio.gather(do_work_on_event(event, 1), do_work_on_event(event, 2), trigger)


if __name__ == "__main__":
    logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s", level=logging.INFO)
    asyncio.run(main())
