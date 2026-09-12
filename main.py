import os
import sys
import subprocess
import time
import json
import shutil
from playwright.sync_api import sync_playwright


def close_chrome():
    """Close any running Chrome instances."""
    print("Closing any running Chrome instances...")
    # Use /T to kill the entire process tree
    subprocess.run(
        ["taskkill", "/F", "/T", "/IM", "chrome.exe"],
        capture_output=True, text=True
    )
    time.sleep(3)

    # Clean up lock files
    user_data_dir = os.path.join(
        os.environ.get("LOCALAPPDATA", ""), "Google", "Chrome", "User Data"
    )
    for lock_file in ["SingletonLock", "SingletonSocket", "SingletonCookie"]:
        lock_path = os.path.join(user_data_dir, lock_file)
        if os.path.exists(lock_path):
            try:
                os.remove(lock_path)
            except Exception:
                pass


def find_chrome():
    """Find Chrome executable on the system."""
    chrome_paths = [
        os.path.join(os.environ.get("PROGRAMFILES", ""), "Google", "Chrome", "Application", "chrome.exe"),
        os.path.join(os.environ.get("PROGRAMFILES(X86)", ""), "Google", "Chrome", "Application", "chrome.exe"),
        os.path.join(os.environ.get("LOCALAPPDATA", ""), "Google", "Chrome", "Application", "chrome.exe"),
    ]
    for path in chrome_paths:
        if os.path.exists(path):
            return path
    return None


def find_profile():
    """Find the correct Chrome profile directory."""
    user_data_dir = os.path.join(
        os.environ.get("LOCALAPPDATA", ""), "Google", "Chrome", "User Data"
    )
    profile_dir = "Default"
    try:
        local_state_path = os.path.join(user_data_dir, "Local State")
        if os.path.exists(local_state_path):
            with open(local_state_path, "r", encoding="utf-8") as f:
                local_state = json.load(f)
            info_cache = local_state.get("profile", {}).get("info_cache", {})
            for key, value in info_cache.items():
                name = value.get("name", "").lower()
                if "muhammad" in name:
                    profile_dir = key
                    break
    except Exception as e:
        print(f"Could not read Chrome profiles, using Default: {e}")
    return user_data_dir, profile_dir


def prepare_temp_profile(real_user_data_dir, profile_dir, temp_dir):
    """
    Copy essential session/cookie files from the real Chrome profile
    to a clean single-profile directory. This avoids the multi-profile
    broker process that blocks Playwright.
    """
    # Clean old temp profile
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir, ignore_errors=True)

    dst_profile = os.path.join(temp_dir, "Default")
    src_profile = os.path.join(real_user_data_dir, profile_dir)

    # Copy network cookies (Chrome 96+)
    src_network = os.path.join(src_profile, "Network")
    dst_network = os.path.join(dst_profile, "Network")
    if os.path.exists(src_network):
        os.makedirs(dst_network, exist_ok=True)
        for f in ["Cookies", "Cookies-journal"]:
            s = os.path.join(src_network, f)
            if os.path.exists(s):
                try:
                    shutil.copy2(s, os.path.join(dst_network, f))
                except Exception:
                    pass

    # Copy direct profile files (cookies, login, preferences)
    os.makedirs(dst_profile, exist_ok=True)
    for f in ["Cookies", "Cookies-journal",
              "Login Data", "Login Data-journal",
              "Web Data", "Web Data-journal",
              "Preferences", "Secure Preferences"]:
        s = os.path.join(src_profile, f)
        if os.path.exists(s):
            try:
                shutil.copy2(s, os.path.join(dst_profile, f))
            except Exception:
                pass

    # Copy Local State (contains the encryption key for cookies)
    src_local_state = os.path.join(real_user_data_dir, "Local State")
    if os.path.exists(src_local_state):
        with open(src_local_state, "r", encoding="utf-8") as f:
            state = json.load(f)
        # Keep only os_crypt (encryption key) to avoid multi-profile triggers
        new_state = {"os_crypt": state.get("os_crypt", {})}
        with open(os.path.join(temp_dir, "Local State"), "w", encoding="utf-8") as f:
            json.dump(new_state, f)

    print(f"Session copied to: {temp_dir}")


def run_automation(prompt_text: str, image_path: str = None, user_data: dict = None) -> str:
    if user_data:
        context_str = f"User Context:\nName: {user_data.get('name')}\nEmail: {user_data.get('email')}\nDistrict: {user_data.get('district')}\nPostal Code: {user_data.get('postal_code')}\nStreet: {user_data.get('street')}\n\n"
        prompt_text = context_str + f"User Request: {prompt_text}"
    chrome_exe = find_chrome()
    if not chrome_exe:
        raise Exception("ERROR: Could not find Chrome installation.")

    print(f"Using Chrome at: {chrome_exe}")

    user_data_dir, profile_dir = find_profile()
    print(f"Using profile: {profile_dir}")

    # Prepare a clean single-profile directory with your session cookies
    project_dir = os.path.dirname(os.path.abspath(__file__))
    temp_profile_dir = os.path.join(project_dir, "chrome_profile")
    prepare_temp_profile(user_data_dir, profile_dir, temp_profile_dir)

    try:
        with sync_playwright() as p:
            print("Launching Chrome...")
            context = p.chromium.launch_persistent_context(
                user_data_dir=temp_profile_dir,
                executable_path=chrome_exe,
                headless=False,
                args=[
                    "--start-maximized",
                    "--disable-blink-features=AutomationControlled",
                    "--no-first-run",
                    "--no-default-browser-check",
                ],
                ignore_default_args=["--enable-automation"],
                no_viewport=True,
                timeout=60000,
            )

            # Inject cookies from cookie.json to bypass "verify it's you"
            cookie_file = os.path.join(project_dir, "cookie.json")
            if os.path.exists(cookie_file):
                print("Injecting cookies from cookie.json...")
                try:
                    with open(cookie_file, "r", encoding="utf-8") as f:
                        cookies = json.load(f)
                        valid_cookies = []
                        for c in cookies:
                            # Map properties for Playwright compatibility
                            if "expirationDate" in c:
                                c["expires"] = c.pop("expirationDate")
                            ss = c.get("sameSite")
                            if ss == "no_restriction":
                                c["sameSite"] = "None"
                            elif ss == "lax":
                                c["sameSite"] = "Lax"
                            elif ss == "strict":
                                c["sameSite"] = "Strict"
                            else:
                                if "sameSite" in c:
                                    del c["sameSite"]
                            for k in ["id", "hostOnly", "session", "storeId"]:
                                if k in c:
                                    del c[k]
                            valid_cookies.append(c)
                        context.add_cookies(valid_cookies)
                        print(f"Successfully injected {len(valid_cookies)} cookies.")
                except Exception as e:
                    print(f"Failed to load cookies: {e}")

            page = context.pages[0] if context.pages else context.new_page()

            # Go directly to Gemini
            print("Opening https://gemini.google.com/app ...")
            page.goto("https://gemini.google.com/app", wait_until="domcontentloaded", timeout=60000)
            print("Gemini loaded!")
            time.sleep(3)

            # Step 1: Click prompt input area
            print("Clicking on prompt input...")
            input_xpath = "//div[@aria-label='Enter a prompt for Gemini']//p"
            page.wait_for_selector(input_xpath, timeout=30000)
            page.locator(input_xpath).click()

            # Step 2: Type the prompt
            print(f"Typing prompt: '{prompt_text}'")
            page.keyboard.type(prompt_text)

            # Step 3: Upload files (system_prompt.md and optionally the image)
            files_to_upload = [os.path.join(project_dir, "system_prompt.md")]
            if image_path and os.path.exists(image_path):
                files_to_upload.append(image_path)
                
            print(f"Uploading files: {files_to_upload}")
            try:
                # Most robust way: target the hidden file input directly
                page.locator("input[type='file']").set_input_files(files_to_upload)
            except Exception:
                # Fallback to UI clicks using more robust locators
                page.locator("button[aria-label='Upload & tools']").click()
                time.sleep(1)
                with page.expect_file_chooser() as fc_info:
                    page.locator("text=Upload files").first.click()
                fc_info.value.set_files(files_to_upload)
                
            print("Files attached!")
            time.sleep(3)

            # Step 4: Click send (arrow_upward)
            print("Clicking send button...")
            time.sleep(1)
            page.locator("//mat-icon[@data-mat-icon-name='arrow_upward']").click()

            # Step 5: Wait for response
            print("Waiting ~20 seconds for Gemini to respond...")
            time.sleep(20)

            # Step 6: Extract response text
            print("Extracting response text...")
            elements = page.locator("message-content")
            if elements.count() > 0:
                result_text = elements.nth(elements.count() - 1).inner_text()
            else:
                result_text = page.locator("body").inner_text()

            # Step 7: Save to data.txt in project root
            output_path = os.path.join(project_dir, "data.txt")
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(result_text)

            print(f"Response saved to {output_path}")
            print("Done!")
            return result_text

    except Exception as e:
        print(f"An error occurred: {e}")
        return f"Error: {e}"


if __name__ == "__main__":
    # Test execution
    res = run_automation("what is it ?", os.path.join(os.path.dirname(os.path.abspath(__file__)), "img", "images.jpg"))
    print("Test Result:", res)
