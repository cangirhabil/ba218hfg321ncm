import os
import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run_admin(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://localhost:8084/")
    page.get_by_role("link", name="Log in").click()
    page.locator("#ajax_loginuser").fill("admin")
    page.locator("#ajax_loginpass").click()
    page.locator("#ajax_loginpass").fill("admin123")
    page.get_by_role("button", name="Log in").click()
    page.wait_for_timeout(3000)
#    page.goto("http://localhost:8084/")

#    page.wait_for_load_state()
#    page.pause()
    page.context.storage_state(path=f"{folder_name}/Admin.json")

    # ---------------------
    context.close()
    browser.close()

def run_2(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://localhost:8084/")
    page.get_by_role("link", name="Log in").click()
    page.locator("#ajax_loginuser").fill("standard_user")
    page.locator("#ajax_loginpass").click()
    page.locator("#ajax_loginpass").fill("user123")
    page.get_by_role("button", name="Log in").click()
    page.wait_for_timeout(3000)
#    page.goto("http://localhost:8084/")

#    page.wait_for_load_state()
#    page.pause()
    page.context.storage_state(path=f"{folder_name}/StandardUser.json")
    # ---------------------
    context.close()
    browser.close()

def run_Anonymous(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://localhost:8084/")

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
    run_2(playwright)
    run_Anonymous(playwright)

