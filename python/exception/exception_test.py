import logging
import logging.handlers
import os
import sys
import time
import traceback
from types import TracebackType
from typing import Optional, Type

# 配置日志
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

my_handler = logging.handlers.WatchedFileHandler("./hello.log")
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
my_handler.setFormatter(formatter)
logger.addHandler(my_handler)


def master():
    cnt = 0
    for i in range(5):
        cnt += 1
        print(f"pid: {os.getpid()} master: {cnt}")
        time.sleep(1)
    raise Exception(f"pid: {os.getpid()} master error")


def slave():
    cnt = 0
    for i in range(2):
        cnt += 1
        print(f"pid: {os.getpid()} slave: {cnt}")
        time.sleep(1)
    raise KeyboardInterrupt


def global_exception_handler(
    exc_type: Type[BaseException],
    exc_value: BaseException,
    exc_traceback: Optional[TracebackType],
) -> None:
    """
    全局异常处理函数。

    参数：
    - exc_type: 异常类型
    - exc_value: 异常实例
    - exc_traceback: 异常追踪对象
    """
    error_message = "".join(
        traceback.format_exception(exc_type, exc_value, exc_traceback)
    )
    print(f"程序发生崩溃，错误信息已记录并发送告警邮件：\n{error_message}")

    # 写入日志
    logger.error(f"程序崩溃: {error_message}")

    # 可以选择在这里退出程序，或者进行其他清理操作
    sys.exit(1)


# 设置全局异常处理器
sys.excepthook = global_exception_handler

if __name__ == "__main__":
    try:
        pid = os.fork()
        if pid == 0:
            slave()
        else:
            master()
    except Exception as e:
        print(f"发生错误: {e}")
