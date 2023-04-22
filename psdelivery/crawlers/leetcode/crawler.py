from typing import List

import bs4

from psdelivery.core.crawler import ProblemCrawler
from psdelivery.core.engine import BeautifulSoupEngine
from psdelivery.crawlers.leetcode.item import LeetcodeProblemItem

class LeetcodeCrawler(ProblemCrawler):
    base_url = 'https://leetcode.com/problemset/all'
    engine = BeautifulSoupEngine()

    def access_to_problem_list(self) -> None: ...
    
    def get_problem_elements(self) -> List[bs4.element.Tag]:
        problem_table: bs4.element.Tag = \
            self.engine().find('div', attrs={'role': 'rowgroup'})
        return [p for p in problem_table.children]
    
    def parse_problem_from_problem_element(
            self, item: bs4.element.Tag) -> LeetcodeProblemItem | None:
        title, difficulty, seq, website = None, None, None, None
        for i, attr in enumerate(item.children):
            if i == 1:
                title_raw = attr.find('div', 'truncate').a.text
                title = '.'.join(title_raw.split('.')[1:])[1:]

                splited_title = title.lower().split()
                seq = '-'.join(splited_title)

                website = f'https://leetcode.com/problems/{seq}/'
            
            elif i == 5:
                difficulty = {'Easy': 1, 'Medium': 2, 'Hard': 3}[attr.span.text]

        return LeetcodeProblemItem(seq, title, website, difficulty)
