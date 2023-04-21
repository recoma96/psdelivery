from typing import List
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from psdelivery.exc import ElementNotFoundError
from psdelivery.crawlers.baekjoon.item import BaekjoonProblemItem
from psdelivery.core.crawler import ProblemCrawler

class BaekjoonCrawler(ProblemCrawler):
    base_url = 'https://solved.ac/ko'
        
    def access_to_problem_list(self, *args, **kwargs):
        navbar_btns = self.driver.find_elements(By.CLASS_NAME, 'css-1va60cc')
        show_search_form_btn = None
        for btn in navbar_btns:
            if btn.get_attribute('href') == 'https://solved.ac/ko#':
                show_search_form_btn = btn
                break
        if not show_search_form_btn:
            raise ElementNotFoundError('Show search input button on naver is not exists.')

        show_search_form_btn.send_keys(Keys.ENTER)
        time.sleep(0.3)

        input_form = self.driver.find_element(By.CLASS_NAME, 'css-1cprwwy') \
                                    .find_element(By.TAG_NAME, 'input')
        input_form.send_keys('*')
        input_form.send_keys(Keys.ENTER)
        time.sleep(0.5)

    def get_problem_elements(self) -> List:
        items = self.driver.find_elements(By.CLASS_NAME, 'css-1ojb0xa')
        return items
    
    def parse_problem_from_problem_element(self, item) -> BaekjoonProblemItem:
        seq_element = item.find_element(By.CLASS_NAME, 'css-1raije9')
        seq = seq_element.find_element(By.TAG_NAME, 'span').text
        difficulty =seq_element.find_element(By.TAG_NAME, 'img') \
                                    .get_attribute('src').split('/')[-1][:-4] 
        if difficulty == 'nr' or difficulty == '0':
            # 난이도가 책정되어 있지 않은 문제는 제외시킴
            return None
        if difficulty == 'sprout':
            # 새싹문제
            difficulty = '1'
        difficulty = int(difficulty)
        
        title_element = item.find_element(By.CLASS_NAME, 'css-d6mf5j')
        title = title_element.find_element(By.CLASS_NAME, '__Latex__').text
        website = title_element.find_element(By.TAG_NAME, 'a').get_attribute('href')
        tag_btn = item.find_element(By.CLASS_NAME, 'css-gv0s7n')
        tag_btn.send_keys(Keys.ENTER)
        time.sleep(0.1)
        tag_elements = item.find_elements(By.CLASS_NAME, 'css-18la3yb')
        tags = []
        for element in tag_elements:
            tag = element.find_element(By.CLASS_NAME, 'css-1rqtlpb').text
            if tag:
                tags.append(tag[1:])
        return BaekjoonProblemItem(seq, title, website, difficulty, tags)
