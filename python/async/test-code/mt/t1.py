import threading
import asyncio


def run_event_loop(loop: asyncio.AbstractEventLoop):
    asyncio.set_event_loop(loop)
    loop.run_forever()


async def task() -> int:
    print(f'{threading.current_thread().native_id}, task is running in the event loop')
    await asyncio.sleep(1)
    return 100


def print_thread_info_msg(msg: str) -> None:
    print(f'{threading.current_thread().native_id}, {msg}')


if __name__ == '__main__':
    print(f'{threading.current_thread().native_id}, main thread is running')
    loop = asyncio.new_event_loop()
    threading.Thread(target=run_event_loop, args=(loop,), daemon=True).start()

    loop.call_soon_threadsafe(print_thread_info_msg, 'call_soon_threadsafe')
    future = asyncio.run_coroutine_threadsafe(task(), loop)
    print(f'got async result: {future.result()}')
