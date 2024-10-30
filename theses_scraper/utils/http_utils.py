"""
Módulo com funções utilitárias para requisições HTTP.
"""

import httpx


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


def get_file_type(response: httpx.Response) -> str:
    """Obtém o tipo de conteúdo do cabeçalho de resposta."""
    return response.headers.get("Content-Type", "").lower()


def is_pdf(url: str) -> bool:
    """Verifica se a URL redireciona para um conteúdo PDF."""
    try:
        response = httpx.head(url, follow_redirects=True)
        content_type = get_file_type(response)
        return "application/pdf" in content_type
    except httpx.RequestError:
        return False
