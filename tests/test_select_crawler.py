import unittest

from psdelivery import PsDelivery


class TestSelectCrawler(unittest.TestCase):

    def test_select_no_exists_crawler(self):
        with self.assertRaises(ValueError):
            PsDelivery('wrong')
