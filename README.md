[![uv][uv-badge]](https://github.com/astral-sh/uv)
[![Python 3.12][python-badge]](https://www.python.org/)
# theses-scraper

Script para fazer download das teses e dissertações em repositórios de universidades brasileiras. No momento, o script suporta alguns repositórios específicos, mas a ideia é expandir para outros repositórios.

## Início Rápido
1. Instalar dependências do projeto
```sh
git clone https://github.com/ApoenaX/theses-scraper.git
cd theses-scraper && pip install .
```

## Usando a bilioteca


1. Download de um trabalho
```python
from theses_scraper.parsers import ParserFactory
from theses_scraper.downloader import DocumentDownloader

url = "https://monografias.ufma.br/jspui/handle/123456789/3510"

parser = ParserFactory.get_parser(url)
document: str | list[str] = parser.get_pdf_link(url)

downloader = DocumentDownloader("./data")
downloader.download(document)
```


[uv-badge]: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json
[python-badge]: https://img.shields.io/badge/python-3.12-blue

