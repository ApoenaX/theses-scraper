import requests
import pathlib
from bs4 import BeautifulSoup
import tenacity
from rich.progress import track
from rich.console import Console
from tenacity import stop_after_attempt, wait_fixed, wait_random


@tenacity.retry(
    stop=stop_after_attempt(5),
    wait=wait_fixed(5) + wait_random(0, 5),
)
def download_pdf(url: str, id: int, output_dir: str) -> str | None:
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0",
        "Accept": "application/pdf, */*;q=0.1",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://sucupira.capes.gov.br",
        "Connection": "keep-alive",
        "Referer": url,
        "Accept-Language": "pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Host": "sucupira.capes.gov.br",
    }

    output_dir = pathlib.Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    with requests.session() as session:
        r = session.get(url)
        soup = BeautifulSoup(r.text, "html.parser")

        form = soup.find("form", id="download")

        if not form:
            return None

        form_data = {
            i.get("name"): i.get("value") for i in form.find_all("input")
        }
        form_data[
            "download:link_download_arquivo"
        ] = "download:link_download_arquivo"

        pdf_name = soup.find("a", id="download:link_download_arquivo")
        pdf_name = pdf_name.get_text() if pdf_name else ""

        if not pdf_name:
            return None

        filepath = output_dir / f"{id}-{pdf_name}.pdf"

        resp = session.post(
            url, data=form_data, stream=True, headers=headers, timeout=7
        )
        with open(filepath, "wb") as f:
            f.write(resp.content)

        return str(filepath)


def download_multiple_pdfs(urls: list[str], output_dir: str) -> list:
    console = Console()
    console.print(f"Percorrendo {len(urls)} urls...")
    downloaded = []
    for url in track(urls, description="Baixando arquivos..."):
        current_id = url.split("=")[-1]
        try:
            filepath = download_pdf(url, current_id, output_dir)
            downloaded.append(filepath)
        except requests.exceptions.ConnectionError:
            console.log(f"Connection error: {url}", style="bold red")
        except requests.exceptions.Timeout:
            console.log(f"Timeout error: {url}", style="bold red")
        except requests.exceptions.HTTPError:
            console.log(f"HTTP error: {url}", style="bold red")
        except requests.exceptions.RequestException:
            console.log(f"Request error: {url}", style="bold red")
        except Exception as e:
            console.log(f"Unknown error: {url} - {e}", style="bold red")
    return downloaded
