"""Módulo com a fábrica de parsers."""

from .generic import GenericParser
from .maxwell import MaxwellParser
from .sophia import SophiaParser
from .dynamic_parser import DynamicContentParser
from .ufrr import UFRRParser
from .cespu import CESPUParser


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
                "ufvjm.edu.br",
                "patua.iec.gov.br",
                "repositorio.esenfc.pt",
                "repositorio.unifesp.br",
                "ipen.br",
            ]
        ):
            return DynamicContentParser()
        elif "bdtd.ufrr.br" in url:
            return UFRRParser()
        elif "repositorio.cespu.pt" in url:
            return CESPUParser()
        return GenericParser()
