from typing import Type

from psdelivery.core.crawler import ProblemCrawler
from psdelivery.crawlers.baekjoon import BaekjoonCrawler as BaekjoonCrawler
from psdelivery.crawlers.baekjoon import SolvedacCrawler as SolvedacCrawler
from psdelivery.crawlers.leetcode import LeetcodeCrawler as LeetcodeCrawler

CRAWLER_MAP = {
    'baekjoon': BaekjoonCrawler,
    'solved.ac': SolvedacCrawler,
    'leetcode': LeetcodeCrawler,
}

def generate_crawler(topic: str) -> ProblemCrawler:
    crawler: Type[ProblemCrawler] | None = CRAWLER_MAP.get(topic.lower())
    if not crawler:
        raise ValueError(f'{topic} crawler is not exists.')
    return crawler()
