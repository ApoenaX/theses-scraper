# teses-download

1. Instalar dependências do projet
```sh
git clone https://github.com/AcademicAI/teses-download.git
pip install .
```

2. Passar lista de [urls](https://gist.github.com/jessicacardoso/d711ed26a1c33555085d7d470d55bd45) da plataforma e diretório para salvar pdfs.
```sh
python -m teses_download "urls.txt" "./Trabalhos/"
```