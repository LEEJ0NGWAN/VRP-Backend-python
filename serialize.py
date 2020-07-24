import uuid
import datetime
import collections
from itertools import chain
from functools import singledispatch
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
        connection.close()
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


@singledispatch
def serialize(value, **kwargs):
    pass


@serialize.register(bool)
@serialize.register(type(None))
@serialize.register(int)
@serialize.register(float)
@serialize.register(str)
def value_parse(value, **kwargs):
    return value


@serialize.register(collections.Iterable)
def iter_parse(value, **kwargs):
    value = list(value)
    if len(value) > 10:
        thread_list = [
            Thread(target=serialize, args=(element, ), kwargs=kwargs)
            for element in _chunker(value, 10)
        ]
        return list(chain(*[t.join() for t in thread_list]))
    return [
        serialize(element, **kwargs)
        for element in value
    ]


@serialize.register(collections.Mapping)
def map_parse(value, **kwargs):
    result = collections.OrderedDict()
    for key, value in value.items():
        result[key] = serialize(value, **kwargs)
    return result

@serialize.register(datetime.datetime)
@serialize.register(datetime.date)
def date_parse(value, **kwargs):
    return value.isoformat()


@serialize.register(datetime.time)
def time_parse(value, **kwargs):
    return value.replace(microsecond=0).isoformat()


@serialize.register(uuid.UUID)
def uuid_parse(value, **kwargs):
    return str(value)

