import os
import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run_admin(playwright: Playwright, config) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://localhost:8088/")
    page.get_by_label("Username / E-mail").click()
    page.get_by_label("Username / E-mail").fill("admin")
    page.get_by_label("Password").click()
    page.get_by_label("Password").fill("admin123")
    page.get_by_label("Password").press("Enter")

    page.wait_for_timeout(5000);
    # page.locator("#header_infos #header_logo").click()

    config.homepages['Admin'] = page.url

    page.wait_for_load_state()
    page.context.storage_state(path=f"{folder_name}/Admin.json")

    # ---------------------
    context.close()
    browser.close()

def run_2(playwright: Playwright, config) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://localhost:8088/")
    page.get_by_label("Username / E-mail").click()
    page.get_by_label("Username / E-mail").fill("manager")
    page.get_by_label("Password").click()
    page.get_by_label("Password").fill("manager123")
    page.get_by_label("Password").press("Enter")

    page.wait_for_timeout(5000);
    # page.locator("#header_infos #header_logo").click()

    config.homepages['Manager'] = page.url

    page.wait_for_load_state()
    page.context.storage_state(path=f"{folder_name}/Manager.json")
    # ---------------------
    context.close()
    browser.close()

def run_3(playwright: Playwright, config) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://localhost:8088/")
    page.get_by_label("Username / E-mail").click()
    page.get_by_label("Username / E-mail").fill("uploader")
    page.get_by_label("Password").click()
    page.get_by_label("Password").fill("uploader123")
    page.get_by_label("Password").press("Enter")

    page.wait_for_timeout(5000);
    # page.locator("#header_infos #header_logo").click()

    config.homepages['Uploader'] = page.url

    page.wait_for_load_state()
    page.context.storage_state(path=f"{folder_name}/Uploader.json")
    # ---------------------
    context.close()
    browser.close()

def run_4(playwright: Playwright, config) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto("http://localhost:8088/")
    page.get_by_label("Username / E-mail").click()
    page.get_by_label("Username / E-mail").fill("client")
    page.get_by_label("Password").click()
    page.get_by_label("Password").fill("client123")
    page.get_by_label("Password").press("Enter")

    page.wait_for_timeout(5000);
    # page.locator("#header_infos #header_logo").click()

    config.homepages['Client'] = page.url

    page.wait_for_load_state()
    page.context.storage_state(path=f"{folder_name}/Client.json")
    # ---------------------
    context.close()
    browser.close()

def run_Anonymous(playwright: Playwright, config) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto("http://localhost:8088")
    config.homepages['Anonymous'] = page.url

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
        run_2(playwright,config)
        run_3(playwright,config)
        run_4(playwright,config)
        run_Anonymous(playwright,config)
