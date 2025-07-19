import os
import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run_admin(playwright: Playwright, config) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://localhost:8088/wp-admin")
    page.get_by_label("Username or Email Address").click()
    page.get_by_label("Username or Email Address").fill("admin")
    page.get_by_label("Password", exact=True).click()
    page.get_by_label("Password", exact=True).fill("admin1234")
    page.get_by_label("Password", exact=True).press("Enter")

    page.wait_for_timeout(5000);
    page.goto("http://localhost:8088/")
    # page.get_by_role("banner").get_by_role("link", name="Fuzzer target").click()

    config.homepages['Admin'] = page.url
    page.context.storage_state(path=f"{folder_name}/Admin.json")

    # ---------------------
    context.close()
    browser.close()

def run_2(playwright: Playwright, config) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto("http://localhost:8088/wp-admin")
    page.get_by_label("Username or Email Address").click()
    page.get_by_label("Username or Email Address").fill("editor")
    page.get_by_label("Password", exact=True).click()
    page.get_by_label("Password", exact=True).fill("editor123")
    page.get_by_label("Password", exact=True).press("Enter")
    
    page.wait_for_timeout(5000);
    # page.get_by_role("banner").get_by_role("link", name="Fuzzer target").click()

    config.homepages['Editor'] = page.url
    page.context.storage_state(path=f"{folder_name}/Editor.json")
    # ---------------------
    context.close()
    browser.close()

def run_3(playwright: Playwright, config) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://localhost:8088/wp-admin")
    page.get_by_label("Username or Email Address").click()
    page.get_by_label("Username or Email Address").fill("author")
    page.get_by_label("Password", exact=True).click()
    page.get_by_label("Password", exact=True).fill("author123")
    page.get_by_label("Password", exact=True).press("Enter")
    
    page.wait_for_timeout(3000);
    # page.get_by_role("banner").get_by_role("link", name="Fuzzer target").click()

    config.homepages['Author'] = page.url
    page.context.storage_state(path=f"{folder_name}/Author.json")
    # ---------------------
    context.close()
    browser.close()

def run_4(playwright: Playwright, config) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://localhost:8088/wp-admin")
    page.get_by_label("Username or Email Address").click()
    page.get_by_label("Username or Email Address").fill("contributor")
    page.get_by_label("Password", exact=True).click()
    page.get_by_label("Password", exact=True).fill("contributor123")
    page.get_by_label("Password", exact=True).press("Enter")

    
    page.wait_for_timeout(3000);
    # page.get_by_role("banner").get_by_role("link", name="Fuzzer target").click()

    config.homepages['Contributor'] = page.url
    page.context.storage_state(path=f"{folder_name}/Contributor.json")
    # ---------------------
    context.close()
    browser.close()

def run_5(playwright: Playwright, config) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://localhost:8088/wp-admin")
    page.get_by_label("Username or Email Address").click()
    page.get_by_label("Username or Email Address").fill("subscriber")
    page.get_by_label("Password", exact=True).click()
    page.get_by_label("Password", exact=True).fill("subscriber123")
    page.get_by_label("Password", exact=True).press("Enter")
    
    page.wait_for_timeout(3000);
    # page.get_by_role("banner").get_by_role("link", name="Fuzzer target").click()

    config.homepages['Subscriber'] = page.url
    page.context.storage_state(path=f"{folder_name}/Subscriber.json")
    # ---------------------
    context.close()
    browser.close()

def run_6(playwright: Playwright, config) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto("http://localhost:8088/wp-admin")
    page.get_by_label("Username or Email Address").click()
    page.get_by_label("Username or Email Address").fill("test")
    page.get_by_label("Password", exact=True).click()
    page.get_by_label("Password", exact=True).fill("test123")
    page.get_by_label("Password", exact=True).press("Enter")
    
    page.wait_for_timeout(3000);
    # page.get_by_role("banner").get_by_role("link", name="Fuzzer target").click()

    config.homepages['User'] = page.url
    page.context.storage_state(path=f"{folder_name}/User.json")
    # ---------------------
    context.close()
    browser.close()


def run_Anonymous(playwright: Playwright, config) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://localhost:8088/")

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
        run_6(playwright,config)
        run_Anonymous(playwright,config)
