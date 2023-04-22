from typing import Any
from abc import ABCMeta, abstractmethod
import time

import requests
from requests import Response
import bs4
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement
from webdriver_manager.chrome import ChromeDriverManager

from psdelivery.core.option import CrawlerOption, DefaultCrawlerOption
from psdelivery.exc import RequestTimeout, RequestFailed, WebdriverIsNotLoaded


class CrawlingEngine(metaclass=ABCMeta):
    engine: Any | None = None
    
    @abstractmethod
    def open(self) -> None: ...

    @abstractmethod
    def close(self) -> None: ...

    @abstractmethod
    def open_web(self, url: str) -> None: ...

    def __call__(self) -> Any | None:
        return self.engine


class BeautifulSoupEngine(CrawlingEngine):
    engine: BeautifulSoup | None = None

    def open(self) -> None: ...
    def close(self) -> None: ...

    def open_web(self, url: str) -> None:
        try:
            response: Response = requests.get(url, timeout=30)
        except TimeoutError:
            raise RequestTimeout('Request timeout.')

        if response.status_code == 200:
            self.engine = BeautifulSoup(response.text, 'html.parser')
        else:
            raise RequestFailed('Request failed to web.')



class SeleniumEngine(CrawlingEngine):
    engine: webdriver.Chrome
    option_generator: CrawlerOption = DefaultCrawlerOption()

    def open(self) -> None:
        self.engine = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=self.option_generator.generate())
        
    def close(self) -> None:
        if self.engine:
            self.engine.quit()

    def open_web(self, url: str) -> None:
        if self.engine:
            self.engine.get(url)
            time.sleep(1)
        else:
            raise WebdriverIsNotLoaded('Selenium webdriver is not loaded.')
