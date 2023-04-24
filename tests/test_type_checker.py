import unittest

from psdelivery.utils.type_checker import must_be_type

class TestTypeChecker(unittest.TestCase):

    @staticmethod
    @must_be_type('a', int)
    @must_be_type('b', int)
    def print_two_int(a: int, b: int) -> int:
        return print(a, b)
    
    @staticmethod
    @must_be_type('msg', int | str)
    def print_int_or_str(msg: int | str) -> None:
        print(msg)

    def test_single_type_is_not_valid(self):
        with self.assertRaises(ValueError):
            self.print_two_int(a='1', b=2)
        with self.assertRaises(ValueError):
            self.print_two_int(a=1, b='2')

    def test_union_type_is_valid(self):
        self.print_int_or_str(msg=1)
        self.print_int_or_str(msg='b')

    def test_union_type_is_not_valid(self):
        with self.assertRaises(ValueError):
            self.print_int_or_str(msg=None)

    def test_arg_not_exists(self):
        with self.assertRaises(ValueError):
            self.print_int_or_str(1)
