import unittest

from psdelivery import PsDelivery


class TestBaekjoonGetPsList(unittest.TestCase):
    crawler = PsDelivery('baekjoon')

    def test_page_index_is_minus(self):
        with self.assertRaises(ValueError):
            self.crawler.get_list_by_single_page(-1)

    def test_page_index_is_too_large(self):
        res = self.crawler.get_list_by_single_page(999999)
        self.assertEqual(0, len(res))

    def test_page_index_is_str(self):
        with self.assertRaises(ValueError):
            self.crawler.get_list_by_single_page('hello world')

    def test_success_with_serialize(self):
        crawler = PsDelivery('solved.ac')
        res = crawler.get_list_by_single_page(1, True)
        self.assertEqual(50, len(res))

    def test_exclude_non_rated_problem(self):
        res = self.crawler.get_list_by_single_page(523)
        self.assertEqual(47, len(res))
