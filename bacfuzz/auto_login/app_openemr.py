import os
import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run_admin(playwright: Playwright,config) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://localhost:8098/interface/login/login.php?site=default")
    page.get_by_placeholder("Username").click()
    page.get_by_placeholder("Username").fill("adminadminadmin")
    page.get_by_placeholder("Password").click()
    page.get_by_placeholder("Password").fill("admin12345678")
    page.get_by_role("button", name="Login").click()
#    with page.expect_popup() as page1_info:
#        page.get_by_role("link", name="Main Menu Logo").click()
#    page1 = page1_info.value
#    page1.close()
    page.get_by_text("Messages").click()

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
    page.goto("http://localhost:8098/interface/login/login.php?site=default")
    page.get_by_placeholder("Username").click()
    page.get_by_placeholder("Username").fill("accounting")
    page.get_by_placeholder("Password").click()
    page.get_by_placeholder("Password").fill("Accounting123!")
    page.get_by_role("button", name="Login").click()
    page.locator("#mainMenu").get_by_text("Calendar").click()
    page.get_by_text("Finder").click()

    config.homepages['Accounting'] = page.url
    page.wait_for_load_state()
    page.context.storage_state(path=f"{folder_name}/Accounting.json")
    # ---------------------
    context.close()
    browser.close()

def run_3(playwright: Playwright,config) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://localhost:8098/interface/login/login.php?site=default")
    page.get_by_placeholder("Username").click()
    page.get_by_placeholder("Username").fill("clinician")
    page.get_by_placeholder("Password").click()
    page.get_by_placeholder("Password").fill("Clinician123!")
    page.get_by_role("button", name="Login").click()
    page.get_by_text("Finder").click()

    config.homepages['Clinician'] = page.url
    page.wait_for_load_state()
    page.context.storage_state(path=f"{folder_name}/Clinician.json")
    # ---------------------
    context.close()
    browser.close()

def run_4(playwright: Playwright,config) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://localhost:8098/interface/login/login.php?site=default")
    page.get_by_placeholder("Username").click()
    page.get_by_placeholder("Username").fill("frontoffice")
    page.get_by_placeholder("Password").click()
    page.get_by_placeholder("Password").fill("Frontoffice123!")
    page.get_by_role("button", name="Login").click()
    page.get_by_text("Finder").click()

    config.homepages['FrontOffice'] = page.url
    page.wait_for_load_state()
    page.context.storage_state(path=f"{folder_name}/FrontOffice.json")
    # ---------------------
    context.close()
    browser.close()

def run_5(playwright: Playwright,config) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://localhost:8098/interface/login/login.php?site=default")
    page.get_by_placeholder("Username").click()
    page.get_by_placeholder("Username").fill("standarduser")
    page.get_by_placeholder("Password").click()
    page.get_by_placeholder("Password").fill("User12345678!")
    page.get_by_role("button", name="Login").click()
    page.get_by_text("Finder").click()

    config.homepages['StandardUser'] = page.url
    page.wait_for_load_state()
    page.context.storage_state(path=f"{folder_name}/StandardUser.json")
    # ---------------------
    context.close()
    browser.close()

def run_Anonymous(playwright: Playwright,config) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto("http://localhost:8098/")

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
