import os
import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run_admin(playwright: Playwright, config) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://localhost:8088/admin.php")
    page.get_by_placeholder("admin name").click()
    page.get_by_placeholder("admin name").fill("admin")
    page.get_by_placeholder("admin password").click()
    page.get_by_placeholder("admin password").fill("admin")
    page.get_by_placeholder("admin password").press("Enter")

    page.wait_for_timeout(3000);

    config.homepages['Admin'] = page.url
    page.context.storage_state(path=f"{folder_name}/Admin.json")

    # ---------------------
    context.close()
    browser.close()

def run_2(playwright: Playwright, config) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto("http://localhost:8088/login.php")
    page.get_by_placeholder("Enter your email").click()
    page.get_by_placeholder("Enter your email").fill("user@local.co")
    page.get_by_placeholder("Enter your password").click()
    page.get_by_placeholder("Enter your password").fill("fuzzer")
    page.get_by_placeholder("Enter your password").press("Enter")
    
    page.wait_for_timeout(3000);

    config.homepages['LeaveManager'] = page.url
    page.context.storage_state(path=f"{folder_name}/User.json")
    # ---------------------
    context.close()
    browser.close()


def run_Anonymous(playwright: Playwright, config) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://localhost:8088/login.php")

    page.context.storage_state(path=f"{folder_name}/Anonymous.json")
    # ---------------------
    context.close()
    browser.close()

folder_name = f"../login_state/{os.path.basename(__file__)}"
folder_name = folder_name[:-3]
os.makedirs(folder_name, exist_ok=True)

def main(config):
    with sync_playwright() as playwright:
        print("RUNNING AUTOMATIC LOGIN FROM ",__file__)

        run_admin(playwright,config)
        run_2(playwright,config)
        run_Anonymous(playwright,config)
