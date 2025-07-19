import os
import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run_admin(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://localhost:8088/admin/adminlogin.php")
    page.wait_for_load_state()
    page.get_by_placeholder("Enter email").click()
    page.get_by_placeholder("Enter email").fill("admin@gmail.com")
    page.get_by_placeholder("Enter passsword").click()
    page.get_by_placeholder("Enter passsword").fill("admin123")
    page.get_by_placeholder("Enter passsword").press("Enter")
    page.wait_for_timeout(3000)

    page.context.storage_state(path=f"{folder_name}/Admin.json")
    # ---------------------
    context.close()
    browser.close()

def run_user(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://localhost:8088/user/login.php")
    page.wait_for_load_state()
    page.get_by_placeholder("Enter email").click()
    page.get_by_placeholder("Enter email").click()
    page.get_by_placeholder("Enter email").fill("abc@gmail.com")
    page.get_by_placeholder("Enter passsword").click()
    page.get_by_placeholder("Enter passsword").fill("abc123")
    page.get_by_placeholder("Enter passsword").press("Enter")
    page.wait_for_timeout(3000)

    page.context.storage_state(path=f"{folder_name}/User.json")
    # ---------------------
    context.close()
    browser.close()

def run_Anonymous(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto("http://localhost:8088/rental")

    page.wait_for_load_state()
    page.context.storage_state(path=f"{folder_name}/Anonymous.json")
    # ---------------------
    context.close()
    browser.close()

folder_name = f"../login_state/{os.path.basename(__file__)}"
folder_name = folder_name[:-3]
os.makedirs(folder_name, exist_ok=True)

with sync_playwright() as playwright:
    print("RUNNING AUTOMATIC LOGIN FROM ",__file__)

    run_admin(playwright)
    run_user(playwright)
    run_Anonymous(playwright)

