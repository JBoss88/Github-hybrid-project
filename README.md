# GitHub Hybrid Testing Framework

A hybrid test automation framework that combines **REST API testing** and **Playwright UI testing** in a single pytest workflow. API calls handle fast, reliable setup and teardown while Playwright validates the resulting UI state — eliminating slow, brittle UI-only test scaffolding.

---

## How It Works

The core idea is the `test_repository` fixture in `conftest.py`:

1. **API Setup** — Creates a private GitHub repo instantly via the GitHub REST API
2. **Session Injection** — Playwright skips the login flow entirely by loading a pre-saved `auth.json` browser state, dropping directly onto the authenticated dashboard
3. **UI Test** — Verifies the new repo appears on the dashboard
4. **API Teardown** — Deletes the repo via API after the test completes, pass or fail

This pattern keeps tests fast and stateless without relying on pre-existing test data or slow UI login flows.

---

## Project Structure

```
├── api_clients/
│   ├── base_client.py          # Generic HTTP client (requests wrapper)
│   └── github_api.py           # GitHub-specific API methods
├── config/
│   └── env_data.py             # Loads env vars and base URLs
├── models/
│   └── repo_model.py           # Pydantic model for API response validation
├── pages/
│   ├── base_page.py            # Base Page Object with shared Playwright helpers
│   └── dashboard_page.py       # GitHub dashboard page interactions
├── tests/
│   └── test_repo_lifecycle.py  # Main hybrid E2E test
├── .github/
│   └── workflows/
│       └── test_execution.yml  # GitHub Actions CI pipeline
├── conftest.py                 # Pytest fixtures (API client, page objects, lifecycle)
├── generate_auth.py            # One-time script to capture and save browser auth state
├── requirements.txt
└── .env                        # Not committed — see setup below
```

---

## Setup

**1. Clone and create a virtual environment**
```bash
git clone <repo-url>
cd Github-hybrid-project
python -m venv .venv
source .venv/bin/activate
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
playwright install chromium
```

**3. Configure environment variables**

Create a `.env` file in the project root:
```
GITHUB_TOKEN=your_personal_access_token
GITHUB_USERNAME=your_github_username
GITHUB_PASSWORD=your_github_password
```

The PAT requires `repo` scope to create and delete repositories.

**4. Generate auth state (one-time)**

Run this once to capture your authenticated browser session:
```bash
python generate_auth.py
```

This opens a headed browser, logs into GitHub, and saves the session cookies to `auth.json`. If GitHub prompts for 2FA, complete it manually within the 60-second window. The resulting `auth.json` is used by all subsequent test runs to skip the login flow entirely.

---

## Running Tests

```bash
# Run all tests
pytest

# Run with visible browser
pytest --headed

# Run with verbose output
pytest -v -s
```

---

## CI/CD

The GitHub Actions workflow (`.github/workflows/test_execution.yml`) runs on every push and pull request to `main`, and can also be triggered manually from the Actions tab.

The pipeline requires three repository secrets:

| Secret | Description |
|---|---|
| `GH_TOKEN` | GitHub PAT with `repo` scope |
| `GH_USERNAME` | GitHub username |
| `GH_PASSWORD` | GitHub password |
| `AUTH_JSON_DATA` | Contents of your local `auth.json` file |

Playwright screenshots are captured on test failure and uploaded as a downloadable artifact named `playwright-failure-screenshots`.

---

## Tech Stack

| Tool | Purpose |
|---|---|
| `pytest` | Test runner and fixture management |
| `playwright` + `pytest-playwright` | Browser automation and UI assertions |
| `requests` | GitHub REST API calls |
| `pydantic` | API response validation |
| `python-dotenv` | Environment variable management |
