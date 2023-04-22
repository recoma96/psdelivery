from typing import List
import time
from abc import ABCMeta, abstractmethod

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement
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
    def access_to_problem_list(self) -> None: ...

    @abstractmethod
    def get_problem_elements(self) -> List[WebElement]: ...

    @abstractmethod
    def parse_problem_from_problem_element(self, item: WebElement) -> ProblemItem | None: ...

    def get_list(self) -> List[ProblemItem]:
        self.access_to_problem_list()
        items = self.get_problem_elements()
        problems: List[ProblemItem] = []
        for item in items:
            try:
                problem = self.parse_problem_from_problem_element(item)
            except NoSuchElementException:
                continue
            else:
                if problem:
                    problems.append(problem)
        return problems
