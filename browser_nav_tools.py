import asyncio
from contextlib import asynccontextmanager
from playwright.async_api import async_playwright, Playwright
from livekit.agents import function_tool

CDP_URL = "http://localhost:9222"

@asynccontextmanager
async def get_playwright_context():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(CDP_URL)
        context = browser.contexts[0]
        page = context.pages[0]
        try:
            yield p, browser, context, page
        finally:
            await p.stop()

@function_tool()
async def navigate(url: str):
    """
    Navigate to a webpage on chrome. Do not use if you are already on the page.

    Args:
         url: The url of the page to navigate to

    Returns:
        Confirmation of which website you navigated to
    """
    async with get_playwright_context() as (_, browser, context, page):
        await page.goto(url)
        title = await page.title()
        return f"Navigated to {url} (title: {title})"

@function_tool()
async def click_text(text: str):
    """
    Click on an element on the page, via the text that the element shows.
    This tool is not limited to text boxes or text fields. It may be a video field, or an email.
    The text argument will likely be quite small. If it is large and you get an error, try shortening it and trying again.

    Args:
        text: The text of the element you are trying to click

    Returns:
        Confirmation of the element you clicked on, if successful.
    """
    async with get_playwright_context() as (_, _, _, page):
        await page.get_by_text(text).click(timeout=5000)
        return f"Clicked '{text}'"

@function_tool()
async def type_into(selector: str, text: str):
    """
    Allows you to type into an input field

    Args:
        selector: The element you are trying to type into

    Returns:
        Confirmation of what you typed and which element you typed into.
    """
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(CDP_URL)
        context = browser.contexts[0]
        page = context.pages[0]
        await page.fill(selector, text)
        return f"Typed '{text}' into {selector}"
@function_tool()
async def get_accessibility_tree():
    """
    Allows you to get a snapshot of the page's elements in yaml string format.
    Extremely important in identifying the elements on the page so you do not have to guess what you are looking at.
    The snapshot is quite large, so parse through it effectively to get what is necessary.
    Use this function before clicking on an element on the page or whenever you need "vision" of the page.

    Returns:
        The aria_snapshot of the current page as a string, but in yaml format
    """
    async with get_playwright_context() as (_, _, _, page):
        return await page.locator("body").aria_snapshot()


# ----------------------------
# Test sequence
# ----------------------------
# async def main():
#     print(await navigate("https://example.com"))
#     print(await click_text("More information"))
#     print(await navigate("https://google.com"))
#     print(await type_into("textarea[name=q]", "hello world"))
#     ax_tree = await get_accessibility_tree()
#     print("Accessibility snapshot keys:", ax_tree.keys())
#
# asyncio.run(main())
