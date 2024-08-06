import asyncio
import threading
import time


# Set SHOW_MAIN_HANG to True to see main loop hang due to unsafe event set.
# Set SHOW_MAIN_HANG to False to see main loop properly exit due to save event set.
# The term "safe" here means the main loop is awaked to process any work
# adjusted by non-asyncio threads such as in the example below.
# Most importantly, "safe" here means the callable is run in the context
# of the event loop (main loop below) thread, which means it can access any
# event loop items that woudl be unsafe to access from a different thread.
SHOW_MAIN_HANG = False


def print_thread_info_msg(msg):
    print(
        f"{msg}: "
        f"name={threading.current_thread().name} "
        f"native_id={threading.current_thread().native_id}"
    )


def set_the_event(event: asyncio.Event):
    print_thread_info_msg(f"Setting the event from callable, native_id={threading.current_thread().native_id}")
    event.set()


def other_thread_func(
        main_loop: asyncio.AbstractEventLoop,
        main_loop_event: asyncio.Event
):
    # For example, this thread is doing other work.
    # This thread's work is being performed while the
    # main loop is both running tasks but also when the
    # main loop might be doing nothing, waiting. This
    # thread cannot predict if the main loop is running
    # or waiting, nor should it have to conern itself
    # with such details. Nevertheless, this thread wishes
    # to signal the main loop when something happens, perhaps
    # when there's work ready, or maybe to indicate the
    # work is completed, the program should end. There
    # many examples to choose from... this is just one
    # abstract hypothetical.
    print_thread_info_msg("other_thread_func: doing some other work")
    time.sleep(3)
    if SHOW_MAIN_HANG:
        # This way sets the event but does not wake the main loop
        # which means the event can be set but the main loop sits
        # waiting, not checking the vent. This will cause main loop
        # to hang, not knowing the event has been signaled.
        print(f"other_thread_func: set (unsafe way)")
        main_loop_event.set()
    else:
        # This way sets the event and wakes the main loop, which
        # avoids the hang.
        print(f"other_thread_func: set (safe way)")
        main_loop.call_soon_threadsafe(set_the_event, main_loop_event)


async def main():
    print_thread_info_msg(f"Main event loop thread, native_id={threading.current_thread().native_id}")
    main_loop = asyncio.get_running_loop()
    main_loop_event = asyncio.Event()
    thd = threading.Thread(target=other_thread_func, args=(main_loop, main_loop_event,))
    thd.start()
    print(f"main: wait")
    the_task = asyncio.create_task(main_loop_event.wait())
    await asyncio.wait([the_task])
    print(f"main: wait completed")


if __name__ == "__main__":
    asyncio.run(main())
    print("program exit")
