import unittest
from Iterable.IterableObject import Iterable, shell_sort, filter_function


class IterableTest(unittest.TestCase):
    def test_len(self):
        arr = Iterable([3, 7, 2, 0, 5, 8, 4])
        self.assertEqual(len(arr), 7)

    def test_setItem(self):
        arr = Iterable([3, 7, 2, 0, 5, 8, 4])
        arr[3] = 77
        self.assertEqual(arr[3], 77)

    def test_delItem(self):
        arr = Iterable([3, 7, 2, 0, 5, 8, 4])
        del arr[3]
        self.assertEqual(len(arr), 6)
        self.assertEqual(arr[3], 5)

    def test_iteration(self):
        sir = [3, 7, 2, 0, 5, 8, 4]
        arr = Iterable(sir)
        for i in arr:
            self.assertGreater(i, -1)

    def test_next(self):
        sir = [3, 7, 2, 0]
        arr = Iterable(sir)
        self.assertEqual(next(arr), 3)
        self.assertEqual(next(arr), 7)
        self.assertEqual(next(arr), 2)
        self.assertEqual(next(arr), 0)
        self.assertRaises(StopIteration, next, arr)

    def test_str(self):
        sir = [3, 7, 2, 0, 5, 8, 4]
        arr = Iterable(sir)
        actual_list = str(arr)
        self.assertEqual(actual_list, '[3, 7, 2, 0, 5, 8, 4]')

    def test_append(self):
        arr = Iterable([3, 7, 2, 0, 5, 8, 4])
        arr.append(9999)
        self.assertEqual(len(arr), 8)
        self.assertEqual(arr[-1], 9999)


class FunctionTest(unittest.TestCase):
    def test_filter(self):
        arr = [3, 7, 2, 0, 5, 8, 4]
        actual_list = filter_function(arr, function=lambda x: x % 2 == 0)
        expected_list = [2, 0, 8, 4]
        self.assertEqual(actual_list, expected_list)

    def test_sort(self):
        arr = [3, 7, 2, 0, 5, 8, 4]
        actual_list = shell_sort(arr)
        expected_list = [0, 2, 3, 4, 5, 7, 8]
        self.assertEqual(actual_list, expected_list)

        actual_list = shell_sort(arr, reverse=True)
        expected_list = [8, 7, 5, 4, 3, 2, 0]
        self.assertEqual(actual_list, expected_list)