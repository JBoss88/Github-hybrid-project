# generate_auth.py
from playwright.sync_api import sync_playwright
from config.env_data import GITHUB_USERNAME, GITHUB_PASSWORD

def generate_session_cookies():
    print("Starting session generation...")
    with sync_playwright() as p:
        # We run this headed so you can manually click 2FA if GitHub asks!
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        page.goto("https://github.com/login")
        page.fill("input[name='login']", GITHUB_USERNAME)
        page.fill("input[name='password']", GITHUB_PASSWORD)
        page.click("input[type='submit']")

        print("Waiting for dashboard to load (Handle 2FA manually if prompted)...")
        # We give it 60 seconds just in case you need to type an email code
        page.wait_for_selector(".feed-left-sidebar", timeout=60000)

        # THE MAGIC TRICK: Save the authenticated state!
        context.storage_state(path="auth.json")
        print("Success! VIP wristband saved to auth.json")
        
        browser.close()

if __name__ == "__main__":
    generate_session_cookies()