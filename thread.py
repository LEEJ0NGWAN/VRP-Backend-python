from threading import current_thread
from threading import Thread as _Thread

class Thread(_Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None):
        super().__init__(group, target, name, args, kwargs)
        self.done = False
        self.result = None
        self.start()

    def run(self):
        try:
            if self._target:
                self.result = self._target(*self._args, **self._kwargs)
        finally:
            del self._target, self._args, self._kwargs

        self.done = True

    def join(self, timeout=None):
        if not self._initialized:
            raise RuntimeError("Thread.__init__() n t called")
        if not self._started.is_set():
            raise RuntimeError("cannot join thread before it is started")
        if self is current_thread():
            raise RuntimeError("cannot join current thread")

        if timeout is None:
            self._wait_for_tstate_lock()
        else:
            self._wait_for_tstate_lock(timeout=max(timeout, 0))
        if self.done:
            return self.result


def _chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))

