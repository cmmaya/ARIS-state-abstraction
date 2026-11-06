"""Minimal stand-in for sortedcontainers.SortedKeyList (only what simpn uses)."""
import bisect


class SortedKeyList(list):
    def __init__(self, iterable=None, key=None):
        super().__init__()
        self._key = key if key is not None else (lambda x: x)
        self._keys = []
        if iterable is not None:
            self.update(iterable)

    def add(self, value):
        k = self._key(value)
        i = bisect.bisect_right(self._keys, k)
        self._keys.insert(i, k)
        list.insert(self, i, value)

    def update(self, iterable):
        for v in list(iterable):
            self.add(v)

    def remove(self, value):
        i = list.index(self, value)
        list.pop(self, i)
        self._keys.pop(i)

    def discard(self, value):
        try:
            self.remove(value)
        except ValueError:
            pass

    def pop(self, index=-1):
        self._keys.pop(index)
        return list.pop(self, index)

    def clear(self):
        list.clear(self)
        self._keys.clear()
