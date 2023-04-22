from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from psdelivery.core.engine import SeleniumEngine

from psdelivery.crawlers.baekjoon.item import BaekjoonProblemItem
from psdelivery.core.crawler import ProblemCrawler


class BaekjoonProblemListItemParser:
    item: WebElement

    def __init__(self, item: WebElement):
        self.item = item

    @property
    def seq(self) -> str:
        return self.item.find_element(By.CLASS_NAME, 'css-1raije9')  \
                        .find_element(By.TAG_NAME, 'span').text

    @property
    def web_difficulty(self) -> str:
        return self.item.find_element(By.CLASS_NAME, 'css-1raije9') \
                        .find_element(By.TAG_NAME, 'span').text

    @property
    def title(self) -> str:
        return self.item.find_element(By.CLASS_NAME, 'css-d6mf5j') \
                        .find_element(By.CLASS_NAME, '__Latex__').text

    @property
    def website(self) -> str:
        return self.item.find_element(By.CLASS_NAME, 'css-d6mf5j') \
                    .find_element(By.TAG_NAME, 'a').get_attribute('href')


class BaekjoonCrawler(ProblemCrawler):
    base_url = 'https://solved.ac/search'
    engine = SeleniumEngine()
    
    def access_to_problem_list(self):
        input_form = self.engine().find_element(By.CLASS_NAME, 'css-1ep4btc') \
                                .find_element(By.TAG_NAME, 'input')
        input_form.send_keys('*')
        input_form.send_keys(Keys.ENTER)
        self.engine().implicitly_wait(3)

    def get_problem_elements(self) -> List[WebElement]:
        items = self.engine().find_elements(By.CLASS_NAME, 'css-1ojb0xa')
        return items
    
    def convert_difficulty_to_int(self, difficulty: str) -> int | None:
        if difficulty == 'nr' or difficulty == '0':
            # 난이도가 책정되어 있지 않은 문제는 제외시킴
            return None
        if difficulty == 'sprout':
            # 새싹문제는 브론즈5
            return 1
        return int(difficulty)

    def parse_problem_from_problem_element(
            self, item: WebElement) -> BaekjoonProblemItem | None:
        parser: BaekjoonProblemListItemParser = BaekjoonProblemListItemParser(item)

        seq = parser.seq
        difficulty = self.convert_difficulty_to_int(parser.web_difficulty)
        title = parser.title
        website = parser.website
        
        if not difficulty:
            return None

        return BaekjoonProblemItem(seq, title, website, difficulty)
