import pytest
from config.env_data import GITHUB_API_BASE_URL, GITHUB_PAT
from api_clients.github_api import GithubAPI
import time
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from playwright.sync_api import Page

# --- 1. API Initialization ---

@pytest.fixture(scope="session")
def api_client():
    """
    Instantiates the GitHub API client once for the entire test session.
    Scope='session' means it doesn't waste time rebuilding this object for every single test.
    """
    print("\n[SETUP] Initializing GitHub API Client...")
    return GithubAPI(base_url=GITHUB_API_BASE_URL, token=GITHUB_PAT)


# --- 2. Page Object Initialization ---

@pytest.fixture
def login_page(page: Page) -> LoginPage:
    """
    Takes Playwright's built-in 'page' fixture and wraps it in our custom LoginPage object.
    """
    return LoginPage(page)

@pytest.fixture
def dashboard_page(page: Page) -> DashboardPage:
    """
    Takes Playwright's built-in 'page' fixture and wraps it in our custom DashboardPage object.
    """
    return DashboardPage(page)


# --- 3. The Lifecycle Fixture (The Hybrid Magic) ---

@pytest.fixture
def test_repository(api_client: GithubAPI):
    """
    The ultimate hybrid fixture. 
    1. Uses the API to instantly create a unique repository.
    2. Yields the repository name to the UI test.
    3. Uses the API to instantly delete it when the UI test finishes (pass or fail).
    """
    # SETUP: Create a completely unique repo name using a timestamp
    unique_repo_name = f"auto-test-repo-{int(time.time())}"
    
    print(f"\n[SETUP] Creating test repository: {unique_repo_name}")
    api_client.create_private_repo(unique_repo_name)
    
    # YIELD: Pause here and hand the repo name over to the actual UI test
    yield unique_repo_name 
    
    # TEARDOWN: The UI test finished. Clean up the database!
    print(f"\n[TEARDOWN] Deleting test repository: {unique_repo_name}")
    api_client.delete_repo(unique_repo_name)