from typing import List
import time
from abc import ABCMeta, abstractmethod

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

from psdelivery.core.option import DefaultCrawlerOption, CrawlerOption
from psdelivery.core.item import ProblemItem
from psdelivery.exc import WebdriverIsNotLoaded


class ProblemCrawler(metaclass=ABCMeta):
    option_generator: CrawlerOption = DefaultCrawlerOption()
    driver: webdriver.Chrome | None = None
    base_url: str

    def open_driver(self):
        chrome_driver_path = ChromeDriverManager().install()
        self.driver = webdriver.Chrome(service=Service(chrome_driver_path),
                                       options=self.option_generator.generate())
        
    def open_web(self):
        if self.driver:
            self.driver.get(self.base_url)
            time.sleep(1)
        else:
            raise WebdriverIsNotLoaded('Webdriver is not loaded')
    
    def close_web(self):
        if self.driver:
            self.driver.close()

    def close_driver(self):
        if self.driver:
            self.driver.quit()

    def __del__(self):
        if self.driver:
            self.driver.quit()

    @abstractmethod
    def access_to_problem_list(self, *args, **kwargs):
        """
        문제 리스트를 가져오기 전의 작업
        """
        pass

    @abstractmethod
    def get_problem_elements(self) -> List:
        """
        문제 리스트 엘리먼트 가져오기
        """
        pass

    @abstractmethod
    def parse_problem_from_problem_element(self, item) -> ProblemItem | None:
        """
        아이템 엘러먼트로부터
        문제 데이터 파싱하기
        """
        pass

    def get_list(self, *args, **kwargs) -> List[ProblemItem]:
        self.access_to_problem_list()
        items = self.get_problem_elements()
        problems: List[ProblemItem] = []
        for item in items:
            try:
                problems.append(self.parse_problem_from_problem_element(item))
            except NoSuchElementException:
                continue
        return problems