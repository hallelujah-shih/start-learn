# tips

## 装饰器
````markdown
# sync
```
F = typing.TypeVar("F", bound=typing.Callable[..., typing.Any])

def timer(func: F) -> F:
    def wrapper(*args: typing.Any, **kwargs: typing.Any):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start} seconds to run.")
        return result

    return typing.cast(F, wrapper)

################ spit ################

F = typing.TypeVar("F", bound=typing.Callable[..., typing.Any])

def timer_v1(func: F) -> F:
    @functools.wraps(func)
    def wrapper(*args: typing.Any, **kwargs: typing.Any) -> typing.Any:
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start} seconds to run.")
        return result

    return typing.cast(F, wrapper)
```

# pass args
```
def repeat(num_times: int) -> typing.Callable[[F], F]:
    def decorator_repeat(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: typing.Any, **kwargs: typing.Any) -> typing.Any:
            result = None
            for _ in range(num_times):
                result = func(*args, **kwargs)
            return result

        return typing.cast(F, wrapper)

    return decorator_repeat


@repeat(num_times=3)
def greet(name: str):
    print(f"Hello {name}")


greet("Alice")
```

# async
```
def async_repeat(num_times: int) -> typing.Callable[[F], F]:
    def decorator_repeat(func: F) -> F:
        @functools.wraps(func)
        async def wrapper(*args: typing.Any, **kwargs: typing.Any) -> typing.Any:
            result = None
            for _ in range(num_times):
                result = await func(*args, **kwargs)
            return result

        return typing.cast(F, wrapper)

    return decorator_repeat

@async_repeat(num_times=3)
async def greet(name: str):
    print(f"Hello {name}")
    await asyncio.sleep(1)
```
````

## 迭代
````markdown
# sync
```
def my_iter(n: int)-> typing.Generator[int, None, None]:
    for i in range(n):
        yield i
```
# async
```
async def my_aiter(n: int)-> typing.AsyncGenerator[int, None]:
    for i in range(n):
        yield i

############# split #############
import asyncio
from typing import AsyncGenerator

async def async_generator() -> AsyncGenerator[int, str]:
    value = yield 1  # 初始化值
    while value != "stop":
        value = yield value  # 生成传入的值

async def main():
    agen = async_generator()
    await agen.asend(None)  # 启动生成器
    try:
        print(await agen.asend("hello"))  # 发送值并获取下一个生成的值
        print(await agen.asend("world"))
        print(await agen.asend("stop"))  # 停止生成器
    except StopAsyncIteration:
        print("Generator has stopped.")

asyncio.run(main())
```
````

## context
````markdown
常用的with语句实现上下文管理，此处我们通过contextlib实现上下文管理

from contextlib import contextmanager

@contextmanager
def managed_resource(*args, **kwds):
    # Code to acquire resource, e.g.:
    resource = acquire_resource(*args, **kwds)
    try:
        yield resource
    finally:
        # Code to release resource, e.g.:
        release_resource(resource)

######## split ########

from contextlib import asynccontextmanager

@asynccontextmanager
async def get_connection():
    conn = await acquire_db_connection()
    try:
        yield conn
    finally:
        await release_db_connection(conn)

async def get_all_users():
    async with get_connection() as conn:
        return conn.query('SELECT ...')
````