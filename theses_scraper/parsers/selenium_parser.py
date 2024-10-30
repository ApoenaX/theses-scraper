"""Module for SeleniumParser class."""

import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from .generic import GenericParser


class SeleniumParser(GenericParser):
    """
    Parser para repositórios que necessitam de JavaScript para carregamento completo.
    """

    def get_html(self, url: str, **kwargs) -> tuple[str, str]:
        """
        Obtém o HTML da página e a URL final.
        """
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")

        with webdriver.Chrome(options=options) as driver:
            driver.get(url)
            time.sleep(3)
            page_content = driver.page_source
            current_url = driver.current_url
            return page_content, current_url
