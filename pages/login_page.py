from pages.base_page import BasePage

class LoginPage(BasePage):
    """
    Page Object Model for the GitHub Login Screen.
    Contains locators and actions specific to authenticating a user via the UI.
    """

    def __init__(self, page):
        # Pass the Playwright page object up to the BasePage
        super().__init__(page)
        
        # --- Locators ---
        # These are the actual CSS selectors used by GitHub's login page
        self.username_input = "#login_field"
        self.password_input = "#password"
        self.submit_button = "input[name='commit']"

    def login(self, username: str, password: str):
        """
        Executes the full login flow.
        """
        print(f"UI Action: Starting login flow for user '{username}'...")
        
        # 1. Navigate directly to the login screen
        self.navigate("https://github.com")
        
        # 2. Wait for the page to load by ensuring the username box is visible
        self.wait_for_visible(self.username_input)
        
        # 3. Enter credentials
        self.fill_text(self.username_input, username)
        self.fill_text(self.password_input, password)
        
        # 4. Submit the form
        self.click_el(self.submit_button)
        
        print("UI Action: Login form submitted.")