import unittest
import time

from psdelivery.crawlers.baekjoon import BaekjoonCrawler

class TestBaekjoonGetPsList(unittest.TestCase):
    
    def test_aaa(self):
        crawler = BaekjoonCrawler()
        crawler.open_driver()
        crawler.open_web()
        res = crawler.get_list()
        for r in res:
            print(r.__dict__())
        crawler.close_driver()
    