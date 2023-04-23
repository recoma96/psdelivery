from typing import Type, List

from psdelivery.core.crawler import ProblemCrawler
from psdelivery.core.item import ProblemItem
from psdelivery.crawlers.baekjoon import SolvedacCrawler, BaekjoonCrawler
from psdelivery.crawlers.leetcode import LeetcodeCrawler

CRAWLER_MAP = {
    'baekjoon': BaekjoonCrawler,
    'solved.ac': SolvedacCrawler,
    'leetcode': LeetcodeCrawler,
}

class PsDelivery:
    crawler: ProblemCrawler

    def __init__(self, topic: str) -> None:
        crawler: Type[ProblemCrawler] | None = CRAWLER_MAP.get(topic.lower())
        if not crawler:
            raise ValueError(f'{topic} crawler is not exists.')
        self.crawler = crawler()

    def get_list_by_single_page(self, page: int) -> List[ProblemItem]:
        return self.crawler.get_list(page=page)
