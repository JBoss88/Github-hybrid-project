from config.env_data import GITHUB_USERNAME
from pages.dashboard_page import DashboardPage

# We removed 'login_page' and injected the raw Playwright 'page' fixture instead
def test_github_repo_lifecycle(page, dashboard_page: DashboardPage, test_repository: str) -> None:
    """
    Hybrid E2E Test: 
    Validates that a repository created via the backend API 
    successfully renders on the frontend UI dashboard.
    """
    
    repo_name = test_repository 
    print(f"\n[TEST START] Validating UI for repository: {repo_name}")

    # STEP B: Direct Navigation (Bypassing Login)
    # The browser already has the auth.json cookies injected by conftest.py
    # Going to the homepage drops us directly onto the authenticated dashboard!
    page.goto("https://github.com")

    # STEP C: UI Validation
    is_visible = dashboard_page.is_repository_visible(
        owner_username=GITHUB_USERNAME, 
        repo_name=repo_name
    )
    
    assert is_visible, f"CRITICAL: Repository '{repo_name}' did not render on the UI!"
    print("[TEST PASSED] The hybrid lifecycle completed successfully.")