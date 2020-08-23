import typing
import threading


class _DataWithLock:
    def __init__(self, data):
        self.data = data
        self.lock = threading.Lock()


class _MutexGuard:
    def __init__(self, pimpl: _DataWithLock):
        self.pimpl = pimpl

    def __enter__(self):
        self.pimpl.lock.acquire()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.pimpl.lock.release()
        # Do propagate exception.
        return False

    def get(self):
        return self.pimpl.data

    def set(self, value):
        self.pimpl.data = value


class Mutex:
    def __init__(self, data: typing.Any):
        self.pimpl = _DataWithLock(data)

    def lock(self) -> _MutexGuard:
        return _MutexGuard(self.pimpl)
