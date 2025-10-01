import os
import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run_admin(playwright: Playwright) -> None:
    browser = None
    context = None
    page = None
    
    try:
        browser = playwright.chromium.launch(headless=True)  # Use headless for stability
        context = browser.new_context()
        page = context.new_page()
        
        # Set default timeout
        page.set_default_timeout(30000)
        
        page.goto("http://localhost:8084/login")
        
        # Wait for the form to load completely
        page.wait_for_timeout(3000)
        
        # Wait for login form to be visible
        page.wait_for_selector("input[name='user'], input[placeholder*='name'], input[placeholder*='email']", timeout=15000)
        
        # Try multiple selector strategies for Nextcloud
        login_filled = False
        try:
            # First try: direct input selectors
            if page.locator("input[name='user']").is_visible():
                page.fill("input[name='user']", "admin")
                page.fill("input[name='password']", "admin123")
                login_filled = True
        except Exception as e:
            print(f"[LOGIN] First method failed: {e}")
        
        if not login_filled:
            try:
                # Second try: label-based selectors
                if page.get_by_label("Username").is_visible():
                    page.get_by_label("Username").fill("admin")
                    page.get_by_label("Password").fill("admin123")
                    login_filled = True
            except Exception as e:
                print(f"[LOGIN] Second method failed: {e}")
        
        if not login_filled:
            try:
                # Third try: placeholder-based selectors
                username_field = page.locator("input[placeholder*='name'], input[placeholder*='email']").first
                password_field = page.locator("input[type='password']").first
                
                if username_field.is_visible() and password_field.is_visible():
                    username_field.fill("admin")
                    password_field.fill("admin123")
                    login_filled = True
            except Exception as e:
                print(f"[LOGIN] Third method failed: {e}")
        
        if not login_filled:
            print("[LOGIN] All login methods failed")
            return
        
        # Submit form
        submit_success = False
        try:
            if page.get_by_role("button", name="Log in").is_visible():
                page.get_by_role("button", name="Log in").click()
                submit_success = True
        except Exception as e:
            print(f"[LOGIN] First submit method failed: {e}")
        
        if not submit_success:
            try:
                submit_btn = page.locator("button[type='submit'], input[type='submit']").first
                if submit_btn.is_visible():
                    submit_btn.click()
                    submit_success = True
            except Exception as e:
                print(f"[LOGIN] Second submit method failed: {e}")
        
        if not submit_success:
            try:
                page.locator("input[type='password']").press("Enter")
            except Exception as e:
                print(f"[LOGIN] Enter method failed: {e}")
        
        # Wait for redirect after login
        page.wait_for_timeout(5000)
        
        # Save storage state
        try:
            page.context.storage_state(path=f"{folder_name}/Admin.json")
            print("[LOGIN] Admin login state saved successfully")
        except Exception as e:
            print(f"[LOGIN] Failed to save admin state: {e}")
            
    except Exception as e:
        print(f"[LOGIN] Error in run_admin: {e}")
    finally:
        # Ensure cleanup
        try:
            if context:
                context.close()
        except:
            pass
        try:
            if browser:
                browser.close()
        except:
            pass

def run_2(playwright: Playwright) -> None:
    browser = None
    context = None
    page = None
    
    try:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        page.set_default_timeout(30000)
        page.goto("http://localhost:8084/login")
        page.wait_for_timeout(3000)
        
        page.wait_for_selector("input[name='user'], input[placeholder*='name'], input[placeholder*='email']", timeout=15000)
        
        login_filled = False
        try:
            if page.locator("input[name='user']").is_visible():
                page.fill("input[name='user']", "testuser")
                page.fill("input[name='password']", "TestUser2024!")
                login_filled = True
        except Exception as e:
            print(f"[LOGIN] User first method failed: {e}")
        
        if not login_filled:
            try:
                if page.get_by_label("Username").is_visible():
                    page.get_by_label("Username").fill("testuser")
                    page.get_by_label("Password").fill("TestUser2024!")
                    login_filled = True
            except Exception as e:
                print(f"[LOGIN] User second method failed: {e}")
        
        if not login_filled:
            try:
                username_field = page.locator("input[placeholder*='name'], input[placeholder*='email']").first
                password_field = page.locator("input[type='password']").first
                
                if username_field.is_visible() and password_field.is_visible():
                    username_field.fill("testuser")
                    password_field.fill("TestUser2024!")
                    login_filled = True
            except Exception as e:
                print(f"[LOGIN] User third method failed: {e}")
        
        if not login_filled:
            print("[LOGIN] All user login methods failed")
            return
        
        submit_success = False
        try:
            if page.get_by_role("button", name="Log in").is_visible():
                page.get_by_role("button", name="Log in").click()
                submit_success = True
        except Exception as e:
            print(f"[LOGIN] User first submit failed: {e}")
        
        if not submit_success:
            try:
                submit_btn = page.locator("button[type='submit'], input[type='submit']").first
                if submit_btn.is_visible():
                    submit_btn.click()
                    submit_success = True
            except Exception as e:
                print(f"[LOGIN] User second submit failed: {e}")
        
        if not submit_success:
            try:
                page.locator("input[type='password']").press("Enter")
            except Exception as e:
                print(f"[LOGIN] User enter failed: {e}")
        
        page.wait_for_timeout(5000)
        
        try:
            page.context.storage_state(path=f"{folder_name}/User.json")
            print("[LOGIN] User login state saved successfully")
        except Exception as e:
            print(f"[LOGIN] Failed to save user state: {e}")
            
    except Exception as e:
        print(f"[LOGIN] Error in run_2: {e}")
    finally:
        try:
            if context:
                context.close()
        except:
            pass
        try:
            if browser:
                browser.close()
        except:
            pass

def run_3(playwright: Playwright) -> None:
    browser = None
    context = None
    page = None
    
    try:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        page.set_default_timeout(30000)
        page.goto("http://localhost:8084/login")
        page.wait_for_timeout(3000)
        
        page.wait_for_selector("input[name='user'], input[placeholder*='name'], input[placeholder*='email']", timeout=15000)
        
        login_filled = False
        try:
            if page.locator("input[name='user']").is_visible():
                page.fill("input[name='user']", "editor")
                page.fill("input[name='password']", "EditorPass2024!")
                login_filled = True
        except Exception as e:
            print(f"[LOGIN] Editor first method failed: {e}")
        
        if not login_filled:
            try:
                if page.get_by_label("Username").is_visible():
                    page.get_by_label("Username").fill("editor")
                    page.get_by_label("Password").fill("EditorPass2024!")
                    login_filled = True
            except Exception as e:
                print(f"[LOGIN] Editor second method failed: {e}")
        
        if not login_filled:
            try:
                username_field = page.locator("input[placeholder*='name'], input[placeholder*='email']").first
                password_field = page.locator("input[type='password']").first
                
                if username_field.is_visible() and password_field.is_visible():
                    username_field.fill("editor")
                    password_field.fill("EditorPass2024!")
                    login_filled = True
            except Exception as e:
                print(f"[LOGIN] Editor third method failed: {e}")
        
        if not login_filled:
            print("[LOGIN] All editor login methods failed")
            return
        
        submit_success = False
        try:
            if page.get_by_role("button", name="Log in").is_visible():
                page.get_by_role("button", name="Log in").click()
                submit_success = True
        except Exception as e:
            print(f"[LOGIN] Editor first submit failed: {e}")
        
        if not submit_success:
            try:
                submit_btn = page.locator("button[type='submit'], input[type='submit']").first
                if submit_btn.is_visible():
                    submit_btn.click()
                    submit_success = True
            except Exception as e:
                print(f"[LOGIN] Editor second submit failed: {e}")
        
        if not submit_success:
            try:
                page.locator("input[type='password']").press("Enter")
            except Exception as e:
                print(f"[LOGIN] Editor enter failed: {e}")
        
        page.wait_for_timeout(5000)
        
        try:
            page.context.storage_state(path=f"{folder_name}/Editor.json")
            print("[LOGIN] Editor login state saved successfully")
        except Exception as e:
            print(f"[LOGIN] Failed to save editor state: {e}")
            
    except Exception as e:
        print(f"[LOGIN] Error in run_3: {e}")
    finally:
        try:
            if context:
                context.close()
        except:
            pass
        try:
            if browser:
                browser.close()
        except:
            pass

def run_4(playwright: Playwright) -> None:
    browser = None
    context = None
    page = None
    
    try:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        page.set_default_timeout(30000)
        page.goto("http://localhost:8084/login")
        page.wait_for_timeout(3000)
        
        page.wait_for_selector("input[name='user'], input[placeholder*='name'], input[placeholder*='email']", timeout=15000)
        
        login_filled = False
        try:
            if page.locator("input[name='user']").is_visible():
                page.fill("input[name='user']", "viewer")
                page.fill("input[name='password']", "ViewerPass2024!")
                login_filled = True
        except Exception as e:
            print(f"[LOGIN] Viewer first method failed: {e}")
        
        if not login_filled:
            try:
                if page.get_by_label("Username").is_visible():
                    page.get_by_label("Username").fill("viewer")
                    page.get_by_label("Password").fill("ViewerPass2024!")
                    login_filled = True
            except Exception as e:
                print(f"[LOGIN] Viewer second method failed: {e}")
        
        if not login_filled:
            try:
                username_field = page.locator("input[placeholder*='name'], input[placeholder*='email']").first
                password_field = page.locator("input[type='password']").first
                
                if username_field.is_visible() and password_field.is_visible():
                    username_field.fill("viewer")
                    password_field.fill("ViewerPass2024!")
                    login_filled = True
            except Exception as e:
                print(f"[LOGIN] Viewer third method failed: {e}")
        
        if not login_filled:
            print("[LOGIN] All viewer login methods failed")
            return
        
        submit_success = False
        try:
            if page.get_by_role("button", name="Log in").is_visible():
                page.get_by_role("button", name="Log in").click()
                submit_success = True
        except Exception as e:
            print(f"[LOGIN] Viewer first submit failed: {e}")
        
        if not submit_success:
            try:
                submit_btn = page.locator("button[type='submit'], input[type='submit']").first
                if submit_btn.is_visible():
                    submit_btn.click()
                    submit_success = True
            except Exception as e:
                print(f"[LOGIN] Viewer second submit failed: {e}")
        
        if not submit_success:
            try:
                page.locator("input[type='password']").press("Enter")
            except Exception as e:
                print(f"[LOGIN] Viewer enter failed: {e}")
        
        page.wait_for_timeout(5000)
        
        try:
            page.context.storage_state(path=f"{folder_name}/Viewer.json")
            print("[LOGIN] Viewer login state saved successfully")
        except Exception as e:
            print(f"[LOGIN] Failed to save viewer state: {e}")
            
    except Exception as e:
        print(f"[LOGIN] Error in run_4: {e}")
    finally:
        try:
            if context:
                context.close()
        except:
            pass
        try:
            if browser:
                browser.close()
        except:
            pass

def run_Anonymous(playwright: Playwright) -> None:
    browser = None
    context = None
    page = None
    
    try:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        page.set_default_timeout(30000)
        page.goto("http://localhost:8084/")
        page.wait_for_timeout(3000)
        
        try:
            page.context.storage_state(path=f"{folder_name}/Anonymous.json")
            print("[LOGIN] Anonymous login state saved successfully")
        except Exception as e:
            print(f"[LOGIN] Failed to save anonymous state: {e}")
            
    except Exception as e:
        print(f"[LOGIN] Error in run_Anonymous: {e}")
    finally:
        try:
            if context:
                context.close()
        except:
            pass
        try:
            if browser:
                browser.close()
        except:
            pass

folder_name = f"../login_state/{os.path.basename(__file__)}"
folder_name = folder_name[:-3]
os.makedirs(folder_name, exist_ok=True)

def main(config):
    """Main function called by fuzzer.py with config parameter"""
    with sync_playwright() as playwright:
        print("RUNNING AUTOMATIC LOGIN FROM ", __file__)

        run_admin(playwright)
        run_user(playwright)
        run_editor(playwright)
        run_viewer(playwright)
        run_anonymous(playwright)

def run_user(playwright: Playwright) -> None:
    run_2(playwright)

def run_editor(playwright: Playwright) -> None:
    run_3(playwright)

def run_viewer(playwright: Playwright) -> None:
    run_4(playwright)

def run_anonymous(playwright: Playwright) -> None:
    run_Anonymous(playwright)

# When run directly (not imported by fuzzer)
if __name__ == "__main__":
    with sync_playwright() as playwright:
        print("RUNNING AUTOMATIC LOGIN FROM ", __file__)

        run_admin(playwright)
        run_user(playwright)
        run_editor(playwright)
        run_viewer(playwright)
        run_anonymous(playwright)