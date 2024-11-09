"""Módulo para extrair links de PDFs da biblioteca Maxwell."""

from bs4 import BeautifulSoup

from .generic import GenericParser


class MaxwellParser(GenericParser):
    """Parser específico para extrair links de PDFs da biblioteca Maxwell (Puc-Rio)."""

    async def get_pdf_link(self, url: str, **kwargs) -> str | list[str] | None:
        """
        Extrai o link do PDF da página.
        """
        html, url = await self.get_html(url, **kwargs)
        soup = BeautifulSoup(html, "html.parser")
        pdf_links = self.extract_pdf_links(soup)
        return pdf_links

    def extract_pdf_links(self, soup: BeautifulSoup) -> list[str] | None:
        """Extrai os links de PDFs da página."""
        select = soup.find("select", {"id": "file"})
        links = None
        if select:
            options = select.find_all("option", value=lambda v: v)
            links = [
                a["href"]
                for a in soup.find_all(
                    "a", href=lambda a: a and "pdf" in a.lower()
                )
            ]
            return links if len(options) == len(links) else None
        return links
