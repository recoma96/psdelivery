from typing import List, Any
import time
from abc import ABCMeta, abstractmethod

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement
from webdriver_manager.chrome import ChromeDriverManager

from psdelivery.core.engine import CrawlingEngine
from psdelivery.core.option import DefaultCrawlerOption, CrawlerOption
from psdelivery.core.item import ProblemItem
from psdelivery.exc import WebdriverIsNotLoaded


class ProblemCrawler(metaclass=ABCMeta):
    base_url: str
    engine: CrawlingEngine

    def open(self) -> None:
        self.engine.open()

    def close(self) -> None:
        self.engine.close()

    def __del__(self) -> None:
        self.engine.close()

    def open_web(self):
        self.engine.open_web(self.base_url)

    @abstractmethod
    def access_to_problem_list(self) -> None: ...

    @abstractmethod
    def get_problem_elements(self) -> List[Any]: ...

    @abstractmethod
    def parse_problem_from_problem_element(self, item: Any) -> ProblemItem | None: ...

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
