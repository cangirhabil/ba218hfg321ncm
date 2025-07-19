import os
import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run_admin(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://localhost:8083/")
    page.get_by_label("Login").click()
    page.get_by_label("Username or email address *").click()
    page.get_by_label("Username or email address *").fill("admin")
    page.get_by_label("Password *Required").click()
    page.get_by_label("Password *Required").fill("admin123")
    page.get_by_label("Remember me").check()
    page.get_by_role("button", name="Log in").click()

    page.context.storage_state(path=f"{folder_name}/Admin.json")

    # ---------------------
    context.close()
    browser.close()

def run_2(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://localhost:8083/")
    page.get_by_label("Login").click()
    page.get_by_label("Username or email address *").click()
    page.get_by_label("Username or email address *").fill("manager")
    page.get_by_label("Password *Required").click()
    page.get_by_label("Password *Required").fill("manager123")
    page.get_by_text("Remember me").click()
    page.get_by_role("button", name="Log in").click()

    page.context.storage_state(path=f"{folder_name}/ShopManager.json")
    # ---------------------
    context.close()
    browser.close()

def run_3(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://localhost:8083/")
    page.get_by_label("Login").click()
    page.get_by_label("Username or email address *").click()
    page.get_by_label("Username or email address *").fill("author")
    page.get_by_label("Password *Required").click()
    page.get_by_label("Password *Required").fill("author123")
    page.get_by_text("Remember me").click()
    page.get_by_role("button", name="Log in").click()

    page.context.storage_state(path=f"{folder_name}/Author.json")
    # ---------------------
    context.close()
    browser.close()

def run_4(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://localhost:8083/")
    page.get_by_label("Login").click()
    page.get_by_label("Username or email address *").click()
    page.get_by_label("Username or email address *").fill("subscriber")
    page.get_by_label("Password *Required").click()
    page.get_by_label("Password *Required").fill("subscriber123")
    page.locator("label").filter(has_text="Remember me").click()
    page.get_by_role("button", name="Log in").click()

    page.context.storage_state(path=f"{folder_name}/Subscriber.json")
    # ---------------------
    context.close()
    browser.close()

def run_5(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://localhost:8083/")
    page.get_by_label("Login").click()
    page.get_by_label("Username or email address *").click()
    page.get_by_label("Username or email address *").fill("customer")
    page.get_by_label("Password *Required").click()
    page.get_by_label("Password *Required").fill("customer123")
    page.locator("label").filter(has_text="Remember me").click()
    page.get_by_role("button", name="Log in").click()

    page.context.storage_state(path=f"{folder_name}/Customer.json")
    # ---------------------
    context.close()
    browser.close()

def run_Anonymous(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://localhost:8083/")

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
    run_3(playwright)
    run_4(playwright)
    run_5(playwright)
    run_Anonymous(playwright)

