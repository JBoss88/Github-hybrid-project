# GitHub Hybrid Testing Framework

A hybrid test automation framework that combines **REST API testing** and **Playwright UI testing** in a single pytest workflow. API calls handle fast, reliable setup and teardown while Playwright validates the resulting UI state — eliminating slow, brittle UI-only test scaffolding.

---

## How It Works

The core idea is the `test_repository` fixture in `conftest.py`:

1. **API Setup** — Creates a private GitHub repo instantly via the GitHub REST API
2. **UI Test** — Playwright logs into GitHub and verifies the new repo appears on the dashboard
3. **API Teardown** — Deletes the repo via API after the test completes, pass or fail

This pattern keeps tests fast and stateless without relying on pre-existing test data.

---

## Project Structure

```
├── api_clients/
│   ├── base_client.py       # Generic HTTP client (requests wrapper)
│   └── github_api.py        # GitHub-specific API methods
├── config/
│   ├── env_data.py          # Loads env vars and base URLs
│   └── tests/
│       └── test_repo_lifecycle.py  # Main hybrid E2E test
├── models/
│   └── repo_model.py        # Pydantic model for API response validation
├── pages/
│   ├── base_page.py         # Base Page Object with shared Playwright helpers
│   ├── login_page.py        # GitHub login page interactions
│   └── dashboard_page.py    # GitHub dashboard page interactions
├── conftest.py              # Pytest fixtures (API client, page objects, lifecycle)
├── requirements.txt
└── .env                     # Not committed — see setup below
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
GITHUB_PASSWORD=your_github_password
```

The PAT requires `repo` scope to create and delete repositories.

---

## Running Tests

```bash
# Run all tests
pytest

# Run with visible browser
pytest --headed
```

---

## Tech Stack

| Tool | Purpose |
|---|---|
| `pytest` | Test runner and fixture management |
| `playwright` + `pytest-playwright` | Browser automation and UI assertions |
| `requests` | GitHub REST API calls |
| `pydantic` | API response validation |
| `python-dotenv` | Environment variable management |
