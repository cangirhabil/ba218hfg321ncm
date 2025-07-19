import os
import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run_admin(playwright: Playwright, config) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://localhost:8081/adminopenc/")
    page.get_by_placeholder("Username").click()
    page.get_by_placeholder("Username").fill("admin")
    page.get_by_placeholder("Password").click()
    page.get_by_placeholder("Password").fill("admin123")
    # page.get_by_role("button", name=" Login").click()
    page.get_by_placeholder("Password").press("Enter")
    page.wait_for_timeout(3000);
    # page.get_by_role("link", name="John Doe   John Doe ").click()

    config.homepages['Admin'] = page.url
    page.context.storage_state(path=f"{folder_name}/Admin.json")

    # ---------------------
    context.close()
    browser.close()

def run_2(playwright: Playwright, config) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://localhost:8081/adminopenc/")
    page.get_by_placeholder("Username").click()
    page.get_by_placeholder("Username").fill("cataloger")
    page.get_by_placeholder("Password").click()
    page.get_by_placeholder("Password").fill("cataloger123")
    # page.get_by_role("button", name=" Login").click()
    page.get_by_placeholder("Password").press("Enter")
    page.wait_for_timeout(3000);

    config.homepages['Cataloger'] = page.url
    page.context.storage_state(path=f"{folder_name}/Cataloger.json")
    # ---------------------
    context.close()
    browser.close()

def run_3(playwright: Playwright, config) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://localhost:8081/adminopenc/")
    page.get_by_placeholder("Username").click()
    page.get_by_placeholder("Username").fill("market")
    page.get_by_placeholder("Password").click()
    page.get_by_placeholder("Password").fill("market123")
    page.get_by_placeholder("Password").press("Enter")
    page.wait_for_timeout(3000);

    config.homepages['Marketing'] = page.url
    page.context.storage_state(path=f"{folder_name}/Marketing.json")
    # ---------------------
    context.close()
    browser.close()

def run_4(playwright: Playwright, config) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://localhost:8081/index.php?route=account/login&language=en-gb")
    page.get_by_placeholder("E-Mail Address").click()
    page.get_by_placeholder("E-Mail Address").fill("customer@local.co")
    page.get_by_placeholder("Password").click()
    page.get_by_placeholder("Password").fill("customer123")
    page.get_by_placeholder("Password").press("Enter")
    page.wait_for_timeout(3000);

    config.homepages['Customer'] = page.url
    page.context.storage_state(path=f"{folder_name}/Customer.json")
    # ---------------------
    context.close()
    browser.close()

def run_Anonymous(playwright: Playwright, config) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://localhost:8081/")

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
        run_3(playwright,config)
        run_4(playwright,config)
        run_Anonymous(playwright,config)
