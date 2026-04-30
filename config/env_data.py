import os
from dotenv import load_dotenv

# Load environment variables from a local .env file
load_dotenv()

GITHUB_API_BASE_URL = "https://api.github.com"
GITHUB_WEB_BASE_URL = "https://github.com"

GITHUB_USERNAME = "JBoss88"
GITHUB_PASSWORD = os.getenv("GITHUB_PASSWORD")
GITHUB_PAT = os.getenv("GITHUB_TOKEN")

# Fail early and loudly if the token is missing
if not GITHUB_PAT:
    raise ValueError("CRITICAL: GITHUB_TOKEN environment variable is missing. Check your .env file!")