"""Módulo com a fábrica de parsers."""

from .generic import GenericParser
from .maxwell import MaxwellParser
from .sophia import SophiaParser
from .selenium_parser import SeleniumParser
from .ufrr import UFRRParser


class ParserFactory:
    """Fábrica para instanciar parsers específicos com base no domínio da URL."""

    @staticmethod
    def get_parser(url: str):
        """Retorna um parser específico para a URL fornecida."""
        if "maxwell.vrac.puc-rio.br" in url:
            return MaxwellParser()
        elif "codigo_sophia=" in url:
            return SophiaParser()
        elif any(
            domain in url
            for domain in [
                "web.esenfc.pt",
                "repositorio.pgsskroton.com",
                "repositorio.pgsscogna.com.br",
                "repositorio.unesp.br",
                "locus.ufv.br",
                "www.locus.ufv.br",
            ]
        ):
            return SeleniumParser()
        elif "bdtd.ufrr.br" in url:
            return UFRRParser()
        return GenericParser()
