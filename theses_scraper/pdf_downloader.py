"""Módulo para obter o link de PDFs de repositórios institucionais."""

import re
import time
from urllib.parse import urljoin, urlparse
import httpx
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class PDFDownloader:
    """Classe para obter o link de dissertações e
    teses de repositórios institucionais."""

    @staticmethod
    def get(url: str, **kwargs) -> httpx.Response:
        """
        Executa uma requisição HTTP GET e retorna a resposta.

        Args:
            url (str): URL do recurso.
            **kwargs: Args adicionais para `httpx.Client`.

        Returns:
            httpx.Response: Resposta da requisição.
        """
        with httpx.Client(**kwargs) as client:
            response = client.get(url)
            response.raise_for_status()
            return response

    @staticmethod
    def check_redirect_to_pdf(url: str, **kwargs) -> bool:
        """
        Verifica se a URL redireciona para um PDF.

        Args:
            url (str): URL para verificar redirecionamento.
            **kwargs: Args adicionais para a requisição HTTP HEAD.

        Returns:
            bool: True se a URL redireciona para um PDF, False caso contrário.
        """
        with httpx.Client(**kwargs) as client:
            response = client.head(url, follow_redirects=True)
            content_type = response.headers.get("Content-Type", "").lower()
            return "application/pdf" in content_type

    @staticmethod
    def get_pdf_link(url: str, **kwargs) -> str | None:
        """
        Retorna o link de download do PDF conforme o tipo de repositório.

        Args:
            url (str): URL do recurso.
            **kwargs: Args adicionais para o método `get`.

        Returns:
            str | None: URL do PDF ou None se não encontrada.
        """
        if url.endswith(".pdf"):
            return url
        elif PDFDownloader.check_redirect_to_pdf(url, **kwargs):
            return url
        elif "codigo_sophia=" in url:
            return PDFDownloader.get_pdf_url_sophia(url, **kwargs)
        elif "maxwell.vrac.puc-rio.br" in url:
            return PDFDownloader.get_maxwell_pdf_links(url, **kwargs)
        elif any(
            domain in url
            for domain in [
                "web.esenfc.pt",
                "pgsscogna.com.br",
                "repositorio.pgsskroton.com",
                "repositorio.unesp.br",
                "repositorio.esenfc.pt",
                "locus.ufv.br",
                "www.locus.ufv.br",
            ]
        ):
            return PDFDownloader.fetch_with_selenium(url)
        else:
            return PDFDownloader.extract_pdf_from_get(url, **kwargs)

    @staticmethod
    def extract_pdf_from_get(url: str, **kwargs) -> str | None:
        """Extrai o link PDF de uma página acessada via GET."""
        response = PDFDownloader.get(url, **kwargs)
        current_url = str(response.url)
        return PDFDownloader.extract_pdf_url_from_soup(
            BeautifulSoup(response.content, "html.parser"), base_url=current_url
        )

    @staticmethod
    def get_pdf_url_sophia(url: str, **kwargs) -> str | None:
        """
        Gera a URL de download para sistemas baseados no código Sophia.

        Args:
            url (str): URL contendo o parâmetro 'codigo_sophia'.

        Returns:
            str | None: URL do PDF ou None se não encontrada.
        """
        codigo_sophia = PDFDownloader.extract_sophia_code(url)
        if not codigo_sophia:
            return None

        new_url = f"https://{urlparse(url).netloc}/php"
        download_page_url = f"{new_url}/midia.php?tipo=1&codigo={codigo_sophia}"
        response = PDFDownloader.get(download_page_url, **kwargs)

        return PDFDownloader.extract_pdf_url_from_soup(
            BeautifulSoup(response.content, "html.parser"), base_url=download_page_url
        )

    @staticmethod
    def extract_sophia_code(url: str) -> str | None:
        """Extrai o código Sophia da URL."""
        match = re.search(r"codigo_sophia=([^&]+)", url)
        return match.group(1) if match else None

    @staticmethod
    def extract_pdf_url_from_soup(soup: BeautifulSoup, base_url: str) -> str | None:
        """
        Extrai a URL do PDF a partir do HTML.

        Args:
            soup (BeautifulSoup): Objeto BeautifulSoup do HTML.
            base_url (str): URL base para construção de URLs relativas.

        Returns:
            str | None: URL do PDF ou None.
        """
        if pdf_url := PDFDownloader.find_meta_pdf_url(soup, base_url):
            return pdf_url

        pdf_patterns = [
            {"tag": "object", "attr": "data", "type": "application/pdf"},
            {"tag": "a", "attr": "href", "pattern": r"/Busca/Download\?codigoArquivo="},
            {"tag": "a", "attr": "href", "pattern": r"/bitstream.*\.pdf$"},
            {
                "tag": "a",
                "attr": "href",
                "pattern": r"download.php\?(id_ficheiro|codigo)=",
            },
        ]

        for pattern in pdf_patterns:
            if pdf_url := PDFDownloader.find_pdf_url_by_pattern(
                soup, base_url, **pattern
            ):
                return pdf_url

    @staticmethod
    def find_meta_pdf_url(soup: BeautifulSoup, base_url: str) -> str | None:
        """Busca o link PDF na tag meta, se existir."""
        meta_tag = soup.find("meta", {"name": "citation_pdf_url"})
        return urljoin(base_url, meta_tag["content"]) if meta_tag else None

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

    @staticmethod
    def fetch_with_selenium(
        url: str, proxy: str = None, timeout: int = 2
    ) -> str | None:
        """
        Obtém o conteúdo HTML de uma página usando Selenium e extrai o link do PDF.

        Args:
            url (str): URL da página.
            proxy (str): Servidor proxy (opcional).
            timeout (int): Tempo máximo de espera em segundos.

        Returns:
            str | None: Link do PDF ou None.
        """
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        if proxy:
            options.add_argument(f"--proxy-server={proxy}")

        with webdriver.Chrome(options=options) as driver:
            driver.get(url)
            time.sleep(timeout)
            soup = BeautifulSoup(driver.page_source, "html.parser")
            return PDFDownloader.extract_pdf_url_from_soup(
                soup, base_url=driver.current_url
            )

    @staticmethod
    def get_maxwell_pdf_links(url: str, **kwargs) -> list[str] | None:
        """
        Extrai links de arquivos PDF da biblioteca Maxwell a partir de um objeto BeautifulSoup.

        Args:
            url (str): URL da página Maxwell.

        Returns:
            list[str] | None: Lista de URLs dos arquivos PDF encontrados ou
            None se não houver links.
        """
        response = PDFDownloader.get(url, **kwargs)
        soup = BeautifulSoup(response.content, "html.parser")
        select = soup.find("select", {"id": "file"})
        if select:
            options = select.find_all("option", value=lambda v: v)
            links = [
                a["href"]
                for a in soup.find_all("a", href=lambda a: a and "pdf" in a.lower())
            ]
            return links if len(options) == len(links) else None
