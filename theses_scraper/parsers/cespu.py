"""Módulo para extrair links de PDFs da biblioteca Maxwell."""

from urllib.parse import urljoin
from bs4 import BeautifulSoup
from .generic import GenericParser


class CESPUParser(GenericParser):
    """Parser específico para extrair links de PDFs do repositório da CESPU."""

    def get_pdf_link(self, url: str, **kwargs) -> str | list[str] | None:
        """
        Extrai o link do PDF da página.
        """
        html, url = self.get_html(url, **kwargs)
        soup = BeautifulSoup(html, "html.parser")
        pdf_links = self.extract_pdf_links(soup, url)
        return pdf_links

    def extract_pdf_links(self, soup: BeautifulSoup, base_url: str) -> list[str] | None:
        """Extrai os links de PDFs da página."""
        links = soup.find_all(
            "a", href=lambda href: href and "/bitstream/handle" in href
        )
        if not links:
            return None
        links = [urljoin(base_url, link["href"]) for link in links]
        return links
