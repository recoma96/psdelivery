from typing import List
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement

from psdelivery.exc import ElementNotFoundError
from psdelivery.crawlers.baekjoon.item import BaekjoonProblemItem
from psdelivery.core.crawler import ProblemCrawler

class BaekjoonCrawler(ProblemCrawler):
    base_url = 'https://solved.ac/search'
    
    def access_to_problem_list(self):
        input_form = self.driver.find_element(By.CLASS_NAME, 'css-1ep4btc') \
                                .find_element(By.TAG_NAME, 'input')
        input_form.send_keys('*')
        input_form.send_keys(Keys.ENTER)
        self.driver.implicitly_wait(10)

    def get_problem_elements(self) -> List[WebElement]:
        items = self.driver.find_elements(By.CLASS_NAME, 'css-1ojb0xa')
        return items
    
    def parse_seq(self, item: WebElement) -> str:
        return item.find_element(By.CLASS_NAME, 'css-1raije9') \
                    .find_element(By.TAG_NAME, 'span').text
    
    def parse_web_difficulty(self, item: WebElement) -> str:
        return item.find_element(By.CLASS_NAME, 'css-1raije9') \
                    .find_element(By.TAG_NAME, 'img') \
                    .get_attribute('src').split('/')[-1][:-4]
    
    def parse_title(self, item: WebElement) -> str:
        return item.find_element(By.CLASS_NAME, 'css-d6mf5j') \
                    .find_element(By.CLASS_NAME, '__Latex__').text
    
    def parse_website(self, item: WebElement) -> str:
        return item.find_element(By.CLASS_NAME, 'css-d6mf5j') \
                    .find_element(By.TAG_NAME, 'a').get_attribute('href')
    
    def parse_algorithm_tags(self, item: WebElement) -> List[str]:
        tag_btn = item.find_element(By.CLASS_NAME, 'css-gv0s7n')
        tag_btn.send_keys(Keys.ENTER)
        self.driver.implicitly_wait(0.2)

        tag_elements = item.find_elements(By.CLASS_NAME, 'css-18la3yb')
        tags = []
        for element in tag_elements:
            tag = element.find_element(By.CLASS_NAME, 'css-1rqtlpb').text
            if tag:
                tags.append(tag[1:])
        return tags
    
    def convert_difficulty_to_int(self, difficulty: str) -> int | None:
        if difficulty == 'nr' or difficulty == '0':
            # 난이도가 책정되어 있지 않은 문제는 제외시킴
            return None
        if difficulty == 'sprout':
            # 새싹문제는 브론즈5
            return 1
        return int(difficulty)

    def parse_problem_from_problem_element(self, item: WebElement) -> BaekjoonProblemItem | None:
        seq = self.parse_seq(item)
        difficulty = self.convert_difficulty_to_int(self.parse_web_difficulty(item))
        title = self.parse_title(item)
        website = self.parse_website(item)
        tags = self.parse_algorithm_tags(item)
        
        if not difficulty:
            return None

        return BaekjoonProblemItem(seq, title, website, difficulty, tags)
