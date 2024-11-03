"""Módulo com o parser genérico para repositórios institucionais."""

import re
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from theses_scraper.utils import http_utils
from .parser import Parser


class GenericParser(Parser):
    """
    Parser para repositórios institucionais genéricos.
    """

    def get_html(self, url: str, **kwargs) -> tuple[str, str]:
        """
        Obtém o HTML da página e a URL final.
        """
        response = http_utils.get(url, **kwargs)
        return response.content, str(response.url)

    def get_pdf_link(self, url: str, **kwargs) -> str | list[str] | None:
        """
        Extrai o link do PDF da página.
        """
        if url.endswith(".pdf"):
            return url
        if http_utils.is_pdf(url):
            return url
        html, url = self.get_html(url, **kwargs)
        soup = BeautifulSoup(html, "html.parser")
        if pdf_url := self.find_meta_pdf_url(soup, url):
            return pdf_url
        return self.extract_pdf_url_from_soup(soup, url)

    @staticmethod
    def find_meta_pdf_url(soup: BeautifulSoup, base_url: str) -> str | None:
        """Busca o link PDF na tag meta, se existir."""
        meta_tag = soup.find("meta", {"name": "citation_pdf_url"})
        if meta_tag:
            pdf_url = meta_tag.get("content")
            return GenericParser.normalize_localhost_url(pdf_url, base_url)

    @staticmethod
    def normalize_localhost_url(pdf_url: str, base_url: str) -> str:
        """
        Substitui 'localhost' no URL pelo domínio da URL base.

        Parâmetros:
            pdf_url (str): URL do PDF a ser corrigida.
            base_url (str): URL base do repositório.

        Retorna:
            str: URL do PDF corrigida.
        """
        parsed_url = urlparse(pdf_url)
        if parsed_url.hostname == "localhost":
            base_netloc = urlparse(base_url).netloc
            pdf_url = pdf_url.replace(f"localhost:{parsed_url.port}", base_netloc)
        return pdf_url

    @staticmethod
    def extract_pdf_url_from_soup(soup: BeautifulSoup, base_url: str) -> str | None:
        """Extrai o link do PDF a partir de um objeto BeautifulSoup."""
        if pdf_url := GenericParser.find_meta_pdf_url(soup, base_url):
            return pdf_url

        pdf_patterns = [
            {"tag": "object", "attr": "data", "mime_type": "application/pdf"},
            {"tag": "a", "attr": "href", "pattern": r"/Busca/Download\?codigoArquivo="},
            {"tag": "a", "attr": "href", "pattern": r"/bitstream.*\.pdf$"},
            {
                "tag": "a",
                "attr": "href",
                "pattern": r"download.php\?(id_ficheiro|codigo)=",
            },
            {"tag": "a", "attr": "href", "pattern": r"auth-sophia/exibicao"},
        ]

        for pattern in pdf_patterns:
            if pdf_url := GenericParser.find_pdf_url_by_pattern(
                soup, base_url, **pattern
            ):
                return pdf_url

    @staticmethod
    def find_pdf_url_by_pattern(
        soup: BeautifulSoup,
        base_url: str,
        tag: str,
        attr: str,
        pattern: str = None,
        mime_type: str = None,
    ) -> str | None:
        """Busca uma URL de PDF usando padrões específicos."""
        search_filter = {attr: re.compile(pattern)} if pattern else {}
        if mime_type:
            search_filter["type"] = mime_type
        link = soup.find(tag, search_filter)
        return urljoin(base_url, link.get(attr)) if link else None
