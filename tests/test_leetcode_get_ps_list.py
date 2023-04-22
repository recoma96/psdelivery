import unittest

from psdelivery.crawlers.leetcode import LeetcodeCrawler

class TestLeetcodeGetPsList(unittest.TestCase):
    
    def test_aaa(self):
        crawler = LeetcodeCrawler()
        crawler.open()
        crawler.open_web()
        res = crawler.get_list()
        for r in res:
            print(r.__dict__())
        crawler.close()
    