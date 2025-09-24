import os
import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run_admin(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://localhost:8085/scp/login.php")
    
    # Wait for the form to load completely
    page.wait_for_timeout(3000)
    
    # Try multiple selector strategies for osTicket admin login
    try:
        # First try: direct input selectors
        page.fill("input[name='userid']", "adminuser")
        page.fill("input[name='passwd']", "admin123")
    except:
        try:
            # Second try: ID-based selectors
            page.fill("#userid", "adminuser")
            page.fill("#passwd", "admin123")
        except:
            # Third try: placeholder-based selectors
            page.get_by_placeholder("Username", exact=False).fill("adminuser")
            page.get_by_placeholder("Password", exact=False).fill("admin123")
    
    # Submit form
    try:
        page.get_by_role("button", name="Log In").click()
    except:
        try:
            page.click("button[type='submit']")
        except:
            try:
                page.click("input[type='submit']")
            except:
                page.press("input[name='passwd']", "Enter")
    
    # Wait for redirect after login
    page.wait_for_timeout(5000)
    
    # Check if login was successful (osTicket redirects to index.php)
    if "index.php" in page.url or "Staff Control Panel" in page.title():
        print("✅ Admin login successful!")
        page.context.storage_state(path=f"{folder_name}/Admin.json")
    else:
        print(f"❌ Admin login failed. URL: {page.url}")

    context.close()
    browser.close()

def run_agent(playwright: Playwright) -> None:
    """Run for agent role (if exists)"""
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://localhost:8085/scp/login.php")
    
    page.wait_for_timeout(3000)
    
    # For now, use admin credentials as we only have admin user
    # In a real scenario, you would create separate agent accounts
    try:
        page.fill("input[name='userid']", "adminuser")
        page.fill("input[name='passwd']", "admin123")
    except:
        try:
            page.fill("#userid", "adminuser")
            page.fill("#passwd", "admin123")
        except:
            page.get_by_placeholder("Username", exact=False).fill("adminuser")
            page.get_by_placeholder("Password", exact=False).fill("admin123")

    try:
        page.get_by_role("button", name="Log In").click()
    except:
        try:
            page.click("button[type='submit']")
        except:
            try:
                page.click("input[type='submit']")
            except:
                page.press("input[name='passwd']", "Enter")
    
    page.wait_for_timeout(5000)
    
    # Check if login was successful
    if "index.php" in page.url or "Staff Control Panel" in page.title():
        print("✅ Agent login successful!")
        page.context.storage_state(path=f"{folder_name}/Agent.json")
    else:
        print(f"❌ Agent login failed. URL: {page.url}")

    context.close()
    browser.close()

def run_user(playwright: Playwright) -> None:
    """Run for regular user (client side)"""
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://localhost:8085/")  # Client side - no login required
    
    page.wait_for_timeout(3000)
    print("✅ User (client) access saved!")
    page.context.storage_state(path=f"{folder_name}/User.json")

    context.close()
    browser.close()

def run_anonymous(playwright: Playwright) -> None:
    """Run for anonymous user"""
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://localhost:8085")
    
    page.wait_for_timeout(3000)
    print("✅ Anonymous access saved!")
    page.context.storage_state(path=f"{folder_name}/Anonymous.json")
    
    context.close()
    browser.close()

folder_name = f"../login_state/{os.path.basename(__file__)}"
folder_name = folder_name[:-3]
os.makedirs(folder_name, exist_ok=True)

def main(config):
    """Main function called by fuzzer.py with config parameter"""
    with sync_playwright() as playwright:
        print("RUNNING AUTOMATIC LOGIN FROM ", __file__)

        run_admin(playwright)
        run_agent(playwright)
        run_user(playwright)
        run_anonymous(playwright)

# When run directly (not imported by fuzzer)
if __name__ == "__main__":
    with sync_playwright() as playwright:
        print("RUNNING AUTOMATIC LOGIN FROM ", __file__)

        run_admin(playwright)
        run_agent(playwright)
        run_user(playwright)
        run_anonymous(playwright)