import asyncio
import threading
from queue import Queue
from tkinter import Tk, Label, Entry, ttk
from typing import Optional
from util import StressTest


class LoadTester(Tk):
    def __init__(self, loop: asyncio.AbstractEventLoop, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self._queue: Queue = Queue()
        self._refresh_ms: int = 25

        self._loop = loop
        self._load_test: Optional[StressTest] = None
        self.title('Load Tester')

        self._url_label = Label(self, text='URL:')
        self._url_label.grid(row=0, column=0)

        self._url_field = Entry(self, width=10)
        self._url_field.grid(row=0, column=1)

        self._request_label = Label(self, text='Requests:')
        self._request_label.grid(row=1, column=0)

        self._request_field = Entry(self, width=10)
        self._request_field.grid(row=1, column=1)

        self._submit = ttk.Button(self, text='Submit', command=self._start)
        self._submit.grid(row=1, column=2)

        self._pb_label = Label(self, text='Progress:')
        self._pb_label.grid(row=3, column=0)

        self._pb = ttk.Progressbar(self, orient='horizontal', length=200, mode='determinate')
        self._pb.grid(row=3, column=1, columnspan=2)

    def _update_bar(self, pct: int):
        if pct == 100:
            self._load_test = None
            self._submit['text'] = 'Submit'
        else:
            self._pb['value'] = pct
            self.after(self._refresh_ms, self._poll_queue)

    def _queue_update(self, completed_requests: int, total_requests: int):
        self._queue.put(int(completed_requests / total_requests * 100))

    def _poll_queue(self):
        if not self._queue.empty():
            pct = 0
            while not self._queue.empty():
                pct = self._queue.get()
            self._update_bar(pct)
        else:
            if self._load_test:
                self.after(self._refresh_ms, self._poll_queue)

    def _start(self):
        if self._load_test is None:
            self._submit['text'] = 'Cancel'
            test = StressTest(self._loop, self._url_field.get(), int(self._request_field.get()), self._queue_update)
            self.after(self._refresh_ms, self._poll_queue)
            test.start()
            self._load_test = test
        else:
            self._load_test.cancel()
            self._load_test = None
            self._submit['text'] = 'Submit'


class ThreadEventLoop(threading.Thread):
    def __init__(self, loop: asyncio.AbstractEventLoop):
        super().__init__()
        self._loop = loop
        self.daemon = True

    def run(self):
        self._loop.run_forever()


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio_thread = ThreadEventLoop(loop)
    asyncio_thread.start()

    app = LoadTester(loop)
    app.mainloop()
