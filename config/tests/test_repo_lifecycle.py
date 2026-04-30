from config.env_data import GITHUB_USERNAME, GITHUB_PASSWORD
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage

def test_github_repo_lifecycle(login_page: LoginPage, dashboard_page: DashboardPage, test_repository: str) -> None:
    """
    Hybrid E2E Test: 
    Validates that a repository created via the backend API 
    successfully renders on the frontend UI dashboard.
    """
    
    # STEP A & D (The Fixture Magic)
    # By simply requesting 'test_repository', Pytest ran the API creation step.
    # It handed us the unique repo name, and it is already queued up to 
    # automatically delete it via API when this test finishes.
    repo_name = test_repository 
    
    print(f"\n[TEST START] Validating UI for repository: {repo_name}")

    # STEP B: UI Login
    # We call the injected Playwright login page
    login_page.login(username=GITHUB_USERNAME, password=GITHUB_PASSWORD)

    # STEP C: UI Validation
    # We call the injected Playwright dashboard page to verify the backend data
    is_visible = dashboard_page.is_repository_visible(
        owner_username=GITHUB_USERNAME, 
        repo_name=repo_name
    )
    
    # The final assertion
    assert is_visible, f"CRITICAL: Repository '{repo_name}' did not render on the UI!"
    print("[TEST PASSED] The hybrid lifecycle completed successfully.")