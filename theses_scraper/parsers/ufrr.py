"""Este módulo contém o parser para o repositório da UFRR."""

from urllib.parse import urljoin
from bs4 import BeautifulSoup
from .generic import GenericParser


class UFRRParser(GenericParser):
    """
    Parser para o repositório da UFRR.
    """

    async def get_pdf_link(self, url, **kwargs):
        html, url = await self.get_html(url, **kwargs)
        soup = BeautifulSoup(html, "html.parser")
        frame = soup.find("frame", attrs={"name": "mainFrame"})
        if frame:
            frame_url = frame["src"]
            url = urljoin(url, frame_url)
            return url
