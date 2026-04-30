import os
from dotenv import load_dotenv

# load_dotenv() is brilliant because it looks for a local .env file first. 
# If it doesn't find one (like when running on the GitHub cloud server), 
# it fails silently and lets the system's environment variables take over!
load_dotenv()

GITHUB_API_BASE_URL = "https://api.github.com"
GITHUB_WEB_BASE_URL = "https://github.com"

# The names inside os.getenv() MUST perfectly match the names in your YAML file and local .env
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
GITHUB_PASSWORD = os.getenv("GITHUB_PASSWORD")
GITHUB_PAT = os.getenv("GITHUB_PAT")

# Fail early and loudly if the token is missing
if not GITHUB_PAT:
    raise ValueError("CRITICAL: GITHUB_PAT environment variable is missing. Check your .env file or GitHub Secrets!")