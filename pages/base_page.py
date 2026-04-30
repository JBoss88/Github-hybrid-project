from playwright.sync_api import Page, expect

class BasePage:
    """
    A generic wrapper around Playwright's Page object.
    Contains standard UI interactions to keep test files clean and readable.
    """

    def __init__(self, page: Page):
        # We inject the Playwright Page object into the class
        self.page = page

    def navigate(self, url: str):
        print(f"UI Action: Navigating to {url}")
        self.page.goto(url)

    def click_el(self, selector: str):
        print(f"UI Action: Clicking element -> {selector}")
        # Playwright automatically waits for actionability (visible, stable, etc.)
        self.page.locator(selector).click()

    def fill_text(self, selector: str, text: str):
        print(f"UI Action: Typing '{text}' into -> {selector}")
        self.page.locator(selector).fill(text)

    def wait_for_visible(self, selector: str, timeout: int = 10000):
        """
        Explicitly waits for an element to appear on the screen.
        Helpful for asserting that an action (like logging in) was successful.
        """
        print(f"UI Action: Waiting for visibility of -> {selector}")
        element = self.page.locator(selector)
        
        # Using Playwright's built-in web-first assertions
        expect(element).to_be_visible(timeout=timeout)
        return True