import asyncio
import logging
from enum import Enum
from mlog import get_logger

_logger = get_logger(__name__)


class ConnectionState(Enum):
    WAIT_INIT = 0
    INITIALIZING = 1
    INITIALIZED = 2


class Connection:
    def __init__(self):
        self._state = ConnectionState.WAIT_INIT
        self._condition = asyncio.Condition()

    async def initialize(self):
        await self._change_state(ConnectionState.INITIALIZING)
        _logger.info("initialize: initializing connection...")
        await asyncio.sleep(3)
        _logger.info("initialize: initialized connection")
        await self._change_state(ConnectionState.INITIALIZED)

    async def _change_state(self, state: ConnectionState):
        async with self._condition:
            _logger.info(f"change state from {self._state} to {state}")
            self._state = state
            self._condition.notify_all()

    async def execute(self, query: str):
        async with self._condition:
            _logger.info("execute: waiting for connection to initialize")
            await self._condition.wait_for(self._is_initialized)
            _logger.info(f"execute: running {query}")
            await asyncio.sleep(3)

    async def _is_initialized(self) -> bool:
        if self._state is not ConnectionState.INITIALIZED:
            _logger.info(f'_is_initialized: waiting for connection to initialize, current state: {self._state}')
            return False
        _logger.info(f'_is_initialized: connection is initialized')
        return True


async def main():
    conn = Connection()
    query_one = asyncio.create_task(conn.execute("query one"))
    query_two = asyncio.create_task(conn.execute("query two"))
    conn_init = asyncio.create_task(conn.initialize())

    await asyncio.gather(query_one, query_two, conn_init)


if __name__ == "__main__":
    logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s", level=logging.INFO)
    asyncio.run(main())
