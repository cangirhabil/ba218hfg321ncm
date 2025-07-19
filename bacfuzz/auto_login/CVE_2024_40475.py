import os
import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run_admin(playwright: Playwright, config) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://localhost:8088/rental")
    page.wait_for_load_state()
    # page.get_by_role("menuitem", name="Login").click()
    page.get_by_placeholder("Username").click()
    page.get_by_placeholder("Username").fill("mayuri.infospace@gmail.com")
    page.get_by_placeholder("Password").click()
    page.get_by_placeholder("Password").fill("rootadmin")
    page.get_by_placeholder("Password").press("Enter")
    page.wait_for_timeout(3000)

    config.homepages['Admin'] = page.url
    page.context.storage_state(path=f"{folder_name}/Admin.json")
    # ---------------------
    context.close()
    browser.close()

def run_Anonymous(playwright: Playwright, config) -> None:
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

def main(config):
    with sync_playwright() as playwright:
        print("RUNNING AUTOMATIC LOGIN FROM ",__file__)

        run_admin(playwright,config)
        run_Anonymous(playwright,config)

