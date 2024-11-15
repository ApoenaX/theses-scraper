"""
Módulo com funções utilitárias para requisições HTTP.
"""

import httpx


async def get(url: str, **kwargs) -> httpx.Response:
    """
    Executa uma requisição HTTP GET e retorna a resposta.

    Args:
        url (str): URL do recurso.
        **kwargs: Args adicionais para `httpx.Client`.

    Returns:
        httpx.Response: Resposta da requisição.
    """
    async with httpx.AsyncClient(**kwargs) as client:
        response = await client.get(url)
        response.raise_for_status()
        return response


def get_file_type(response: httpx.Response) -> str:
    """Obtém o tipo de conteúdo do cabeçalho de resposta."""
    return response.headers.get("Content-Type", "").lower()


async def is_pdf(url: str) -> bool:
    """Verifica se a URL redireciona para um conteúdo PDF."""
    try:
        async with httpx.AsyncClient(
            timeout=10, verify=False, follow_redirects=True
        ) as client:
            response = await client.head(url)
            content_type = get_file_type(response)
        return "application/pdf" in content_type
    except httpx.RequestError:
        return False


async def resolve_final_url(url: str) -> str:
    """
    Resolve o URL final seguindo redirecionamentos.

    Parâmetros:
        url (str): O URL a ser resolvido.

    Retorna:
        str: O URL final após todos os redirecionamentos.
    """
    try:
        async with httpx.AsyncClient(
            follow_redirects=True, timeout=10, verify=False
        ) as client:
            response = await client.head(url)
            return str(response.url)
    except httpx.RequestError as e:
        print(f"Erro ao resolver a URL {url}: {e}")
        return url  # Retorna a URL original em caso de erro
