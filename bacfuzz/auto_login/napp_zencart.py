import os
import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run_admin(playwright: Playwright, config) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://localhost:8081/adminzcfuzz/index.php?cmd=login&camefrom=index.php")
    page.get_by_placeholder("Username").click()
    page.get_by_placeholder("Username").fill("admin")
    page.get_by_placeholder("Admin Password").click()
    page.get_by_placeholder("Admin Password").fill("admin123")
    page.get_by_placeholder("Admin Password").press("Enter")
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
    page.goto("http://localhost:8081/adminzcfuzz/index.php?cmd=login&camefrom=index.php")
    page.get_by_placeholder("Username").click()
    page.get_by_placeholder("Username").fill("order")
    page.get_by_placeholder("Admin Password").click()
    page.get_by_placeholder("Admin Password").fill("order123")
    page.get_by_placeholder("Admin Password").press("Enter")
    page.wait_for_timeout(3000);

    config.homepages['OrderProcessing'] = page.url
    page.context.storage_state(path=f"{folder_name}/OrderProcessing.json")
    # ---------------------
    context.close()
    browser.close()

def run_3(playwright: Playwright, config) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://localhost:8081/")
    page.get_by_role("link", name="Log In").click()
    page.get_by_role("group", name="Returning Customers: Please").get_by_label("Email Address:").click()
    page.get_by_role("group", name="Returning Customers: Please").get_by_label("Email Address:").fill("root@localhost.com")
    page.get_by_role("group", name="Returning Customers: Please").get_by_label("Password:").click()
    page.get_by_role("group", name="Returning Customers: Please").get_by_label("Password:").fill("smith123")
    page.get_by_role("group", name="Returning Customers: Please").get_by_label("Password:").press("Enter")

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
        run_Anonymous(playwright,config)
