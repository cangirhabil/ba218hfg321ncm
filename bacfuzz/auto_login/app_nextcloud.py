import os
import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run_admin(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://localhost:8084/login")
    
    # Use get_by_label like WordPress WCFM example
    page.get_by_label("Account name or email").click()
    page.get_by_label("Account name or email").fill("admin")
    page.get_by_label("Password", exact=True).click()
    page.get_by_label("Password", exact=True).fill("admin123")
    page.get_by_role("button", name="Log in").click()
    
    page.context.storage_state(path=f"{folder_name}/Admin.json")

    # ---------------------
    context.close()
    browser.close()

def run_2(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://localhost:8084/login")
    
    page.get_by_label("Account name or email").click()
    page.get_by_label("Account name or email").fill("testuser")
    page.get_by_label("Password", exact=True).click()
    page.get_by_label("Password", exact=True).fill("testuser123.")
    page.get_by_role("button", name="Log in").click()

    page.context.storage_state(path=f"{folder_name}/User.json")
    # ---------------------
    context.close()
    browser.close()

def run_3(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://localhost:8084/login")
    
    page.get_by_label("Account name or email").click()
    page.get_by_label("Account name or email").fill("editor")
    page.get_by_label("Password", exact=True).click()
    page.get_by_label("Password", exact=True).fill("editor1234.")
    page.get_by_role("button", name="Log in").click()

    page.context.storage_state(path=f"{folder_name}/Editor.json")
    # ---------------------
    context.close()
    browser.close()

def run_4(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://localhost:8084/login")
    
    page.get_by_label("Account name or email").click()
    page.get_by_label("Account name or email").fill("viewer")
    page.get_by_label("Password", exact=True).click()
    page.get_by_label("Password", exact=True).fill("viewer123.")
    page.get_by_role("button", name="Log in").click()

    page.context.storage_state(path=f"{folder_name}/Viewer.json")
    # ---------------------
    context.close()
    browser.close()

def run_Anonymous(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://localhost:8084")

    page.context.storage_state(path=f"{folder_name}/Anonymous.json")
    # ---------------------
    context.close()
    browser.close()

folder_name = f"../login_state/{os.path.basename(__file__)}"
folder_name = folder_name[:-3]
os.makedirs(folder_name, exist_ok=True)

with sync_playwright() as playwright:
    print("RUNNING AUTOMATIC LOGIN FROM ", __file__)

    run_admin(playwright)
    run_2(playwright)
    run_3(playwright)
    run_4(playwright)
    run_Anonymous(playwright)