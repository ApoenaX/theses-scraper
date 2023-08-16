[![Packaged with Poetry][poetry-badge]](https://python-poetry.org/)
[![Python 3.11][python-badge]](https://www.python.org/)
# teses-download

Script para fazer download das teses e dissertações da CAPES.

## Início Rápido
1. Instalar dependências do projeto
```sh
git clone https://github.com/AcademicAI/teses-download.git
cd teses-catalogo && pip install .
```

2. Passar lista de [urls](https://gist.github.com/jessicacardoso/d711ed26a1c33555085d7d470d55bd45) da plataforma e diretório para salvar pdfs.
```sh
python -m teses_download "urls.txt" "./Trabalhos/"
```

## Usando a bilioteca


1. Download de várias urls
```python
from teses_download import download
from teses_download import cache

with open("/content/urls.txt", "r") as f:
     urls = f.read().splitlines()

my_cache = cache.create_cache()
download.download_multiple_pdfs(urls,"/content/pdfs", my_cache)
```

2. Download de uma url específica
```python
from teses_download import download

url = "https://sucupira.capes.gov.br/sucupira/public/consultas/coleta/trabalhoConclusao/viewTrabalhoConclusao.xhtml?popup=true&id_trabalho=13398016"
id = int(url.split("=")[-1])
download.download_pdf(url, id, "./diretorio-teste")
```

[poetry-badge]: https://img.shields.io/badge/packaging-poetry-cyan.svg
[python-badge]: https://img.shields.io/badge/python-3.10%20%7C%203.11-blue

