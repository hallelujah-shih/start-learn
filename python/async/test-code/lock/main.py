import asyncio
from asyncio import Lock
from util import delay


async def a(lock: Lock):
    print("coroutine a waiting to acquire the lock")
    async with lock:
        print("coroutine a is in the critical section")
        await delay(2)
        print("coroutine a released the lock")


async def b(lock: Lock):
    print("coroutine b waiting to acquire the lock")
    async with lock:
        print("coroutine b is in the critical section")
        await delay(2)
        print("coroutine b released the lock")


async def main():
    lock = Lock()
    await asyncio.gather(a(lock), b(lock))


if __name__ == "__main__":
    asyncio.run(main())
