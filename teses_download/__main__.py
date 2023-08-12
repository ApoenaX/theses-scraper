import argparse
from .download import download_multiple_pdfs
from .cache import create_cache


def main():
    parser = argparse.ArgumentParser(
        description="Baixe arquivos de teses e dissertações da CAPES"
    )
    parser.add_argument(
        "input_file",
        type=str,
        help="Arquivo de entrada com os links para download",
    )
    parser.add_argument(
        "output_dir",
        type=str,
        help="Diretório de saída para os arquivos baixados",
    )
    parser.add_argument(
        "--cache",
        type=str,
        help="Caminho para o diretório de cache",
    )
    args = parser.parse_args()

    if args.cache:
        cache = create_cache(path=args.cache)
    else:
        cache = create_cache()

    with open(args.input_file, "r") as f:
        urls = f.read().splitlines()

    download_multiple_pdfs(urls, args.output_dir, cache)


if __name__ == "__main__":
    main()
