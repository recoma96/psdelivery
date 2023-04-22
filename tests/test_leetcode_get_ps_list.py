import unittest

from psdelivery import generate_crawler

class TestLeetcodeGetPsList(unittest.TestCase):
    crawler = generate_crawler('leetcode')

    def test_page_index_is_minus(self):
        with self.assertRaises(ValueError):
            self.crawler.get_list(page = -1)

    def test_page_index_is_too_large(self):
        res = self.crawler.get_list(page = 9999999)
        self.assertEqual(0, len(res))

    def test_page_index_is_str(self):
        with self.assertRaises(ValueError):
            self.crawler.get_list(page = 'hello world')

    def test_success(self):
        res = self.crawler.get_list(page = 4)
        self.assertEqual(50, len(res))
