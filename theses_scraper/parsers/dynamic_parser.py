"""Module for SeleniumParser class."""

from playwright.async_api import async_playwright
from .generic import GenericParser


class DynamicContentParser(GenericParser):
    """
    Parser para repositórios que necessitam de JavaScript para carregamento completo.
    """

    async def get_html(self, url: str, **kwargs) -> tuple[str, str]:
        """
        Obtém o HTML da página e a URL final.
        """
        timeout = kwargs.get("timeout", 3)
        proxy = kwargs.get("proxy", None)
        headers = kwargs.get("headers", None)
        user_agent = headers.get("User-Agent") if headers else None

        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch(headless=True, proxy=proxy)
            context = await browser.new_context(user_agent=user_agent)
            page = await context.new_page()
            await page.goto(url)
            await page.wait_for_timeout(timeout * 1000)
            page_content = await page.content()
            current_url = page.url
            await context.close()
            await browser.close()
            return page_content, current_url
