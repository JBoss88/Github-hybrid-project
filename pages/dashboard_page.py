from pages.base_page import BasePage

class DashboardPage(BasePage):
    """
    Page Object Model for the GitHub logged-in Dashboard.
    Contains actions for navigating the user's repositories and verifying UI states.
    """

    def __init__(self, page):
        super().__init__(page)
        
        # --- Static Locators ---
        # The main dashboard feed container (used to prove the login was successful)
        self.dashboard_feed = ".feed-left-sidebar"
        
        # The filter input box above the repository list in the left sidebar
        self.repo_filter_input = "input[aria-label='Find a repository…'] >> nth=0"

    def is_repository_visible(self, owner_username: str, repo_name: str) -> bool:
        """
        Searches the dashboard sidebar for a specific repository and returns True if visible.
        Uses a dynamic locator based on the expected href attribute.
        """
        print(f"UI Action: Verifying visibility of repository '{repo_name}'...")
        
        # 1. First, ensure the dashboard has actually loaded
        self.wait_for_visible(self.dashboard_feed)
        
        # 2. Type the repo name into the sidebar filter to clear out the noise
        self.fill_text(self.repo_filter_input, repo_name)
        
        # 3. Construct the Dynamic Locator
        # GitHub creates links using the format: /username/repository-name
        expected_href = f"/{owner_username}/{repo_name}"
        dynamic_repo_locator = f"a[href='{expected_href}'] >> nth=0"
        
        # 4. Wait for it to become visible using your BasePage method
        # If it's not found within the timeout, this will naturally raise an exception
        # and fail the test—which is exactly what we want in a UI validation failure.
        is_visible = self.wait_for_visible(dynamic_repo_locator)
        
        if is_visible:
            print(f"UI Action: Success! Repository '{repo_name}' is visible on the dashboard.")
            
        return is_visible