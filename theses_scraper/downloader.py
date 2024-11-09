"""Módulo para realizar o download de documentos PDF e Word."""

from pathlib import Path

from .utils import http_utils


class DocumentDownloader:
    """Classe para realizar o download de documentos PDF e Word."""

    def __init__(self, save_path: str):
        self.save_path = Path(save_path)
        self.save_path.mkdir(parents=True, exist_ok=True)

    def download(self, url: str, file_name: str = None):
        """Faz o download de um documento e o salva no diretório especificado."""
        response = http_utils.get(url, follow_redirects=True)
        if not response:
            print(f"Falha ao acessar o documento em {url}")
            return

        accepted_types = {
            "application/pdf": "pdf",
            "application/msword": "doc",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "docx",
        }

        file_type = http_utils.get_file_type(response)

        if file_type not in accepted_types:
            print(f"Tipo de arquivo não suportado: {file_type}")
            return

        file_name = Path(str(response.url)).name
        if not file_name.endswith(f".{accepted_types[file_type]}"):
            file_name += f".{accepted_types[file_type]}"
        file_path = self.save_path / file_name
        with open(file_path, "wb") as file:
            file.write(response.content)
        print(f"Documento salvo em {file_path}")
