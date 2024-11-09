"""Este módulo contém o parser para o repositório Sophia."""

import re
from urllib.parse import urlparse

from bs4 import BeautifulSoup

from theses_scraper.utils import http_utils

from .generic import GenericParser


class SophiaParser(GenericParser):
    """
    Parser para o repositório Sophia.
    """

    async def get_html(self, url: str, **kwargs) -> tuple[str, str]:
        """
        Obtém o HTML da página e a URL final.
        """
        sophia_code = self.extract_sophia_code(url)
        if not sophia_code:
            return "", ""
        new_url = f"https://{urlparse(url).netloc}/php"
        download_page_url = f"{new_url}/midia.php?tipo=1&codigo={sophia_code}"
        response = await http_utils.get(download_page_url, **kwargs)
        return response.content, str(response.url)

    async def get_pdf_link(self, url: str, **kwargs) -> str | list[str] | None:
        """
        Extrai o link do PDF da página.
        """
        html, url = await self.get_html(url, **kwargs)
        soup = BeautifulSoup(html, "html.parser")
        if pdf_url := self.find_meta_pdf_url(soup, url):
            return pdf_url
        return self.extract_pdf_url_from_soup(soup, url)

    def extract_sophia_code(self, url: str) -> str | None:
        """Extrai o código Sophia da URL."""
        match = re.search(r"codigo_sophia=([^&]+)", url)
        return match.group(1) if match else None
