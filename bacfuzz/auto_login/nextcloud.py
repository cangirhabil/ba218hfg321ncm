import os
import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run_admin(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://localhost:8084/login")
    
    # Wait for the form to load completely
    page.wait_for_timeout(3000)
    
    # Try multiple selector strategies for Nextcloud
    try:
        # First try: direct input selectors
        page.fill("input[name='user']", "admin")
        page.fill("input[name='password']", "admin123")
    except:
        try:
            # Second try: label-based selectors
            page.get_by_label("Username", exact=True).fill("admin")
            page.get_by_label("Password", exact=True).fill("admin123")
        except:
            # Third try: placeholder-based selectors
            page.get_by_placeholder("Username", exact=True).fill("admin")
            page.get_by_placeholder("Password", exact=True).fill("admin123")
    
    # Submit form
    try:
        page.get_by_role("button", name="Log in").click()
    except:
        try:
            page.click("button[type='submit']")
        except:
            page.click("input[type='submit']")
    
    # Wait for redirect after login
    page.wait_for_timeout(5000)
    page.context.storage_state(path=f"{folder_name}/Admin.json")

    context.close()
    browser.close()

def run_2(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://localhost:8084/login")
    
    page.wait_for_timeout(3000)
    
    try:
        page.fill("input[name='user']", "testuser")
        page.fill("input[name='password']", "testuser123.")
    except:
        try:
            page.get_by_label("Username", exact=True).fill("testuser")
            page.get_by_label("Password", exact=True).fill("testuser123.")
        except:
            page.get_by_placeholder("Username", exact=True).fill("testuser")
            page.get_by_placeholder("Password", exact=True).fill("testuser123.")
    
    try:
        page.get_by_role("button", name="Log in").click()
    except:
        try:
            page.click("button[type='submit']")
        except:
            page.click("input[type='submit']")
    
    page.wait_for_timeout(5000)
    page.context.storage_state(path=f"{folder_name}/User.json")

    context.close()
    browser.close()

def run_3(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://localhost:8084/login")
    
    page.wait_for_timeout(3000)
    
    try:
        page.fill("input[name='user']", "editor")
        page.fill("input[name='password']", "editor1234.")
    except:
        try:
            page.get_by_label("Username", exact=True).fill("editor")
            page.get_by_label("Password", exact=True).fill("editor1234.")
        except:
            page.get_by_placeholder("Username", exact=True).fill("editor")
            page.get_by_placeholder("Password", exact=True).fill("editor1234.")
    
    try:
        page.get_by_role("button", name="Log in").click()
    except:
        try:
            page.click("button[type='submit']")
        except:
            page.click("input[type='submit']")
    
    page.wait_for_timeout(5000)
    page.context.storage_state(path=f"{folder_name}/Editor.json")

    context.close()
    browser.close()

def run_4(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://localhost:8084/login")
    
    page.wait_for_timeout(3000)
    
    try:
        page.fill("input[name='user']", "viewer")
        page.fill("input[name='password']", "viewer123.")
    except:
        try:
            page.get_by_label("Username", exact=True).fill("viewer")
            page.get_by_label("Password", exact=True).fill("viewer123.")
        except:
            page.get_by_placeholder("Username", exact=True).fill("viewer")
            page.get_by_placeholder("Password", exact=True).fill("viewer123.")
    
    try:
        page.get_by_role("button", name="Log in").click()
    except:
        try:
            page.click("button[type='submit']")
        except:
            page.click("input[type='submit']")
    
    page.wait_for_timeout(5000)
    page.context.storage_state(path=f"{folder_name}/Viewer.json")

    context.close()
    browser.close()

def run_Anonymous(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://localhost:8084")

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
        run_user(playwright)
        run_editor(playwright)
        run_viewer(playwright)
        run_anonymous(playwright)

def run_user(playwright: Playwright) -> None:
    run_2(playwright)

def run_editor(playwright: Playwright) -> None:
    run_3(playwright)

def run_viewer(playwright: Playwright) -> None:
    run_4(playwright)

def run_anonymous(playwright: Playwright) -> None:
    run_Anonymous(playwright)

# When run directly (not imported by fuzzer)
if __name__ == "__main__":
    with sync_playwright() as playwright:
        print("RUNNING AUTOMATIC LOGIN FROM ", __file__)

        run_admin(playwright)
        run_user(playwright)
        run_editor(playwright)
        run_viewer(playwright)
        run_anonymous(playwright)