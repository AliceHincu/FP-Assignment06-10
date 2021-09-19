import unittest


class Iterable:
    def __init__(self, sir=None):
        if sir is None:
            self._list = []
        else:
            self._list = sir
        self._len = len(self._list)
        self._current = 0

    def __setitem__(self, index, value):
        self._list[index] = value

    def __getitem__(self, index):
        return self._list[index]

    def __delitem__(self, index):
        del self._list[index]
        self._len -= 1

    def __next__(self):
        self._current += 1
        if self._current <= self._len:
            return self._list[self._current - 1]
        raise StopIteration

    def __iter__(self):
        """
        we turn it into a generator. good for memory & infinite loops. One thing at a time.
        :return:
        """
        for i in self._list:
            yield i

    def __len__(self):
        return self._len

    def append(self, obj):
        self._list.append(obj)
        self._len += 1

    def __str__(self):
        return str(self._list)


def shell_sort(arr, comp=lambda x, y: x <= y, reverse=False):
    # Start with a big gap, then reduce the gap
    n = len(arr)
    gap = n // 2

    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap and comp(temp, arr[j - gap]):
                arr[j] = arr[j - gap]
                j -= gap

            arr[j] = temp
        gap //= 2

    if reverse is True:
        return arr[::-1]
    return arr


def filter_function(array, function=lambda x: x == x):
    return [x for x in array if function(x)]
