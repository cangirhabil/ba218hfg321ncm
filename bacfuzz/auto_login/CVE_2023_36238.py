import os
import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run_admin(playwright: Playwright,config) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://localhost:8088/public/admin/login")
    page.get_by_label("Email").click()
    page.get_by_label("Email").fill("admin@example.com")
    page.get_by_label("Password").click()
    page.get_by_label("Password").fill("admin123")
    page.get_by_label("Password").press("Enter")
    page.wait_for_timeout(3000)

    config.homepages['Admin'] = page.url
    page.wait_for_load_state()
    page.context.storage_state(path=f"{folder_name}/Admin.json")

    # ---------------------
    context.close()
    browser.close()

def run_2(playwright: Playwright,config) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://localhost:8088/public/admin/login")
    page.get_by_label("Email").click()
    page.get_by_label("Email").fill("marketing@example.com")
    page.get_by_label("Password").click()
    page.get_by_label("Password").fill("marketing123")
    page.get_by_label("Password").press("Enter")
    page.wait_for_timeout(3000)

    config.homepages['Marketing'] = page.url
    page.wait_for_load_state()
    page.context.storage_state(path=f"{folder_name}/Marketing.json")
    # ---------------------
    context.close()
    browser.close()

def run_3(playwright: Playwright,config) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://localhost:8088/public/customer/login")
    page.locator("input[name=\"email\"]").click()
    page.locator("input[name=\"email\"]").fill("gencustomer@example.com")
    page.get_by_label("Password").click()
    page.get_by_label("Password").fill("customer123")
    page.get_by_label("Password").press("Enter")
    page.wait_for_timeout(3000)

    config.homepages['GenCustomer'] = page.url
    page.wait_for_load_state()
    page.context.storage_state(path=f"{folder_name}/GenCustomer.json")
    # ---------------------
    context.close()
    browser.close()

def run_4(playwright: Playwright,config) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://localhost:8088/public/customer/login")
    page.locator("input[name=\"email\"]").click()
    page.locator("input[name=\"email\"]").fill("wholesale@example.com")
    page.get_by_label("Password").click()
    page.get_by_label("Password").fill("wholesale123")
    page.get_by_label("Password").press("Enter")
    page.wait_for_timeout(3000)

    config.homepages['WholeSale'] = page.url
    page.wait_for_load_state()
    page.context.storage_state(path=f"{folder_name}/WholeSale.json")
    # ---------------------
    context.close()
    browser.close()

def run_5(playwright: Playwright,config) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://localhost:8088/public/customer/login")
    page.locator("input[name=\"email\"]").click()
    page.locator("input[name=\"email\"]").fill("guest@example.com")
    page.get_by_label("Password").click()
    page.get_by_label("Password").fill("guest123")
    page.get_by_label("Password").press("Enter")
    page.wait_for_timeout(3000)

    config.homepages['Guest'] = page.url
    page.wait_for_load_state()
    page.context.storage_state(path=f"{folder_name}/Guest.json")
    # ---------------------
    context.close()
    browser.close()

def run_Anonymous(playwright: Playwright,config) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto("http://localhost:8088/public")

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
        run_5(playwright,config)
        run_Anonymous(playwright,config)
