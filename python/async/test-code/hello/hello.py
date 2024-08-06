import asyncio


async def hello():
    print("Hello world!")
    r = await asyncio.sleep(1, "I am done")
    print("Hello again!")
    return r


async def main():
    print("main start")
    task = asyncio.create_task(hello())
    print("main wait")
    await task
    print("main end")


if __name__ == "__main__":
    asyncio.run(main())