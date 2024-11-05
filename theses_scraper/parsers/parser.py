"""
This module contains the abstract class ParserRepository, which defines
the methods that must be implemented by the parsers classes.
"""

from abc import ABC, abstractmethod


class Parser(ABC):
    """
    Abstract class that defines the methods that must be implemented by the parsers classes.
    """

    @abstractmethod
    # retorna o html da página e a url final
    async def get_html(self, url: str, **kwargs) -> tuple[str, str]:
        """
        Obtém o HTML da página e a URL final.
        """

    @abstractmethod
    async def get_pdf_link(self, url: str, **kwargs) -> str | list[str] | None:
        """
        Extrai o link do PDF da página.
        """
