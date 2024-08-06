#! /usr/bin/env python3
# vim:fenc=utf-8
#
# Copyright © 2024 shih <shih@fedora>
#
# Distributed under terms of the MIT license.
import signal
import asyncio
import socket
import typing
from asyncio import AbstractEventLoop
from util import delay


class GracefullExit(SystemExit):
    pass


def shutdown():
    raise GracefullExit()


async def close_echo_tasks(echo_tasks: typing.List[asyncio.Task]):
    waiters = [asyncio.wait_for(task, 2) for task in echo_tasks]
    for task in waiters:
        try:
            await task
        except asyncio.exceptions.TimeoutError:
            pass


async def echo(conn: socket.socket, loop: AbstractEventLoop) -> None:
    try:
        while data := await loop.sock_recv(conn, 1024):
            if data.decode().strip() == 'boom':
                raise Exception("Unexpected network error")
            await loop.sock_sendall(conn, data)
    except Exception as ex:
        print("capture err:", ex)
    finally:
        conn.close()


async def listen_for_conn(server_socket: socket.socket, loop: AbstractEventLoop) -> None:
    while True:
        conn, addr = await loop.sock_accept(server_socket)
        conn.setblocking(False)
        asyncio.create_task(echo(conn, loop))


async def main():
    loop = asyncio.get_running_loop()
    loop.add_signal_handler(signal.SIGINT, shutdown)

    server_socket = socket.socket()
    try:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        server_addr = ("127.0.0.1", 8000)
        server_socket.setblocking(False)
        server_socket.bind(server_addr)
        server_socket.listen()

        await listen_for_conn(server_socket, asyncio.get_running_loop())
    except Exception as ex:
        print(f'main func recv exception err: {ex}')
    finally:
        server_socket.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"ex: {e}")
