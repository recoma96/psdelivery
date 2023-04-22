import unittest

from psdelivery.crawlers.leetcode import LeetcodeCrawler

class TestLeetcodeGetPsList(unittest.TestCase):

    crawler = LeetcodeCrawler()

    def test_page_index_is_minus(self):
        res = self.crwaler.get_list(page = -1)
        self.assertEqual(0, len(res))

    def test_page_index_is_too_large(self):
        res = self.crwaler.get_list(page = 9999999)
        self.assertEqual(0, len(res))

    def test_page_index_is_str(self):
        with self.assertRaises(ValueError):
            self.crwaler.get_list(page = 'hello world')

    def test_success(self):
        res = self.crwaler.get_list(page = 4)
        self.assertEqual(50, len(res))
