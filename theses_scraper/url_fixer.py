"""Módulo com funções para corrigir e verificar URLs"""

from urllib.parse import urlparse
from functools import reduce

_DENY_LIST = {
    "",
    "localhost:8080",
    "localhost:443",
    "152.92.4.120",
    "link.springer.com",
    "dx.doi.org.br",
    "sucupira.capes.gov.br",
    "linktr.ee",
    "orcid.org",
    "lattes.cnpg.br",
    "orcid. org",
    "www.youtube.com",
    "dx.doi.org.",
    "dx.doi.org",
    "lattes.cnpq.br",
    "orcid",
    "youtu.be",
    "drive.google.com",
    "dx,doi.org",
    "lattes,cnpq.br",
    "dx:doi.org",
    "dx.org",
    "dx;xoi.org",
    "onlinelibrary.wiley.com",
    "buscatextual.cnpq.br",
    "bdtccs.furg.br:8080",
    "wwws.cnpq.br",
    "Iattes.cníci.br",
    "lattes.cnp q.br",
    "www.abpnrevista.org.br",
    "www.sciencedirect.com",
    "sistemas.usp.br",
    "www.movisaberesefazeresmigrantes.com",
    "sitios.anhembi.br",
    "www.bd.bibl.ita.br",
    "tede.inatel.br:8080",
    "riu.ufam.edu.br",
    "www.teses.ufc.br",
    "rubi.casaruibarbosa.gov.br",
    "repositorio.ismt.pt",
    "dspace.ismt.pt",
    "teses.ufrj.br",
    "www.uff.br",
    "app.uff.br",
    "tede.fecap.br",
    "tede.fecap.br:8080",
    "www2.unifesp.br",
    "www.egn.mar.mil.br",
    "repositorioinstitucional.uea.edu.br",
    "bibliotecadigital.unec.edu.br",
    "repositorio.santamariasaude.pt",
    "www.defesa.gov.br",
    "teses2.ufrj.br",
    "ufba.academia.edu",
    "biotecnologia.ufba.br",
    "repositorio.faema.edu.br:8000",
    "ppgss.ufsc.br",
    "unesp.primo.exlibrisgroup.com",
    "www.obrasraras.fiocruz.br",
}

_REPLACEMENTS = {
    "repositorio.lnec.pt:8080": "repositorio.lnec.pt",
    "http://tede2.usc.br:8080": "https://tede2.usc.br:8443",
    "tede2.usc.br:8443/tede/handle/tede": "tede2.usc.br:8443/handle/tede",
    "tede2.pucgoias.edu.br/tede/handle/tede": "tede2.pucgoias.edu.br/handle/tede",
    "bibliotecatede.uninove.br/tede/handle/tede": "bibliotecatede.uninove.br/handle/tede",
    "dspace.unila.edu.br/123456789": "dspace.unila.edu.br/handle/123456789",
    "tede.bc.uepb.edu.br/tede/jspui": "tede.bc.uepb.edu.br/jspui",
    "repositorio.idp.edu.br/123456789": "repositorio.idp.edu.br/handle/123456789",
    "bdtd.ueg.br/tede/handle/tede": "bdtd.ueg.br/handle/tede",
    "repositorio.unifesp.br/xmlui": "repositorio.unifesp.br",
    "repositorio.ufpa.br/jspui/2011": "repositorio.ufpa.br/jspui/handle/2011",
    "repositorio.ufpa.br/handle": "repositorio.ufpa.br/jspui/handle",
    "repositorio.ufpa.br/jspui/handle2011": "repositorio.ufpa.br/jspui/handle/2011",
    "https://repositorio.ifba.edu.br": "http://repositorio.ifba.edu.br",
    "https://rigeo.cprm.gov.br": "http://rigeo.cprm.gov.br",
    "dspace.unipampa.edu.br:8080": "dspace.unipampa.edu.br",
    "repositorio.unilab.edu.br:8080": "repositorio.unilab.edu.br",
    "bd.bibl.ita.br": "bdita.bibl.ita.br",
    "teste.tede.unifacs.br:8080": "tede.unifacs.br",
    "http://repositorio.ifap.edu.br": "https://repositorio.ifap.edu.br",
    "repositorio.ifap.edu.br:8080": "repositorio.ifap.edu.br",
    "http://repositorio.ufal.br": "http://www.repositorio.ufal.br",
    "bibliodigital.unijui.edu.br:8080": "bibliodigital.unijui.edu.br",
    "bibliodigital.unijui.edu.br/xmlui": "bibliodigital.unijui.edu.br",
    "vkali40.ucs.br:8080": "repositorio.ucs.br",
    "10.1.0.96:8080": "repositorio.ifba.edu.br",
    "191.252.194.60": "repositorio.fdv.br",
    "prod.repositorio.ufscar.br": "repositorio.ufscar.br",
    "www7.bahiana.edu.br": "repositorio.bahiana.edu.br",
    "ri.ucsal.br:8080": "ri.ucsal.br",
    "ri.ucsal.br/jspui": "ri.ucsal.br",
    "10.0.217.128:8080": "tede.upf.br",
    "lrepositorio.ufra.edu.br": "repositorio.ufra.edu.br",
    "repositorio.ufra.edu.br/jspui//jspui": "repositorio.ufra.edu.br/jspui",
    "repositorio.ufra.edu.br/handle": "repositorio.ufra.edu.br/jspui/handle",
    "www.repositorio.fjp.mg.gov.br": "repositorio.fjp.mg.gov.br",
    "rigeoh.cprm.gov.br": "rigeo.cprm.gov.br",
    "200.129.163.131:8080": "tede.ufam.edu.br",
    "200.136.52.105": "repositorio.ipen.br",
    "200.129.209.58:8080": "repositorio.ufgd.edu.br/jspui",
    "repositorio.ufgd.edu.br/jspui/jspui": "repositorio.ufgd.edu.br/jspui",
    "200.129.209.58": "repositorio.ufgd.edu.br",
    "www.repositorio.ufrb.edu.br": "ri.ufrb.edu.br",
    "repositorio.faema.edu.br:8000": "repositorio.unifaema.edu.br",
    "www.repositorio.ufba.br": "repositorio.ufba.br",
    "acervo.ufvjm.edu.br": "repositorio.ufvjm.edu.br",
    "repositorio.ufvjm.edu.br:8080": "repositorio.ufvjm.edu.br",
    "repositorio.ufvjm.edu.br/jspui": "repositorio.ufvjm.edu.br",
    "repositorio.cruzeirodosul.edu.br:8080": "repositorio.cruzeirodosul.edu.br",
    "repositorio.cruzeirodosul.edu.br": "repositorio.cruzeirodosul.edu.br/jspui",
    "repositorio.cruzeirodosul.edu.br/jspui/jspui": "repositorio.cruzeirodosul.edu.br/jspui",
    "tede2.unisagrado.edu.br:8080": "tede2.unisagrado.edu.br:8443",
    "http://repositorio.ufes.br": "https://repositorio.ufes.br",
    "tede.utp.br:8080": "tede.utp.br",
    "tede.unioeste.br:8080/tede": "tede.unioeste.br",
    "tedebc.ufma.br/jspui/handle/tede/tede": "tedebc.ufma.br/jspui/handle/tede",
    "www.repositorio.uniceub.br": "repositorio.uniceub.br/jspui",
    "repositorio.uniceub.br/jspui/jspui": "repositorio.uniceub.br/jspui",
    "www.repositorio.insper.edu.br": "repositorio.insper.edu.br",
    "tede2.uefs.br:8080/handle/tede/tede": "tede2.uefs.br:8080/handle/tede",
    "repositorio.unb.br": "repositorio.unb.br/jspui",
    "repositorio.unb.br/jspui/jspui": "repositorio.unb.br/jspui",
    "dspace.idp.edu.br:8080/xmlui": "repositorio.idp.edu.br",
    "purl.net/esepf/handle": "hdl.handle.net",
    "http://repositorio.ufba.br": "https://repositorio.ufba.br",
}


def update_url(url: str) -> str:
    """
    Atualiza uma URL para a versão correta, considerando um conjunto de regras pré-definidas.

    Args:
        url (str): A URL a ser corrigida.

    Returns:
        str: A URL corrigida conforme as regras.

    Examples:
        >>> update_url("http://tede2.usc.br:8080")
        'https://tede2.usc.br:8443'
    """
    return reduce(
        lambda updated_url, target: updated_url.replace(target, _REPLACEMENTS[target]),
        _REPLACEMENTS,
        url,
    )


def is_denied(url: str) -> bool:
    """Verifica se a url está na lista de urls não permitidas"""
    base_url = url.split("/")[2]
    return base_url in _DENY_LIST


def is_valid_url(url):
    """Verifica se a url é válida"""
    if " " in url:
        return False
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False
