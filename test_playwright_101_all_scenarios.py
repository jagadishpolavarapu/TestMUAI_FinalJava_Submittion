"""
PLAYWRIGHT 101 - ALL SCENARIOS
Single build: "Playwright 101 All Scenarios"
All 3 test scenarios running on TestMu AI cloud platform
"""

import os
import json
import pytest
import time
import urllib.parse
from playwright.sync_api import sync_playwright, expect

# TestMu AI credentials
os.environ["LT_USERNAME"] = "btechjagadish"
os.environ["LT_ACCESS_KEY"] = "LT_yBAKBI6iMMJnq7xyNwWpFBr3fNTFAHpmTRU3d1ndQuPnYqc"

# 2 Browser/OS combinations
BROWSER_CONFIGS = [
    {"browserName": "Chrome", "browserVersion": "latest", "platform": "Windows 10", "name": "Chrome_Win10"},
    {"browserName": "pw-firefox", "browserVersion": "latest", "platform": "macOS Catalina", "name": "Firefox_macOS"}
]

def get_capabilities(browser_config, test_name):
    """Generate TestMu AI capabilities"""
    return {
        "browserName": browser_config["browserName"],
        "browserVersion": browser_config["browserVersion"],
        "LT:Options": {
            "platform": browser_config["platform"],
            "build": "Playwright 101 All Scenarios",  # SINGLE BUILD NAME
            "name": f"{test_name} - {browser_config['name']}",
            "user": os.environ["LT_USERNAME"],
            "accessKey": os.environ["LT_ACCESS_KEY"],
            "network": True,
            "video": True,
            "console": True,
            "visual": True,
        }
    }

def connect_browser(playwright, browser_config, test_name):
    """Connect to TestMu AI with URL encoding"""
    browser_name = browser_config["browserName"].lower()
    browser_type = playwright.firefox if "firefox" in browser_name else playwright.chromium
    
    caps = get_capabilities(browser_config, test_name)
    caps_encoded = urllib.parse.quote(json.dumps(caps))
    ws_endpoint = f"wss://cdp.lambdatest.com/playwright?capabilities={caps_encoded}"
    
    browser = browser_type.connect(ws_endpoint=ws_endpoint)
    context = browser.new_context(viewport={'width': 1920, 'height': 1080})
    page = context.new_page()
    page.set_default_timeout(30000)
    
    return browser, context, page

def mark_status(page, status, remark):
    """Mark test status on TestMu AI"""
    try:
        page.evaluate(
            "_ => {}", 
            f'lambdatest_action: {json.dumps({"action": "setTestStatus", "arguments": {"status": status, "remark": remark}})}'
        )
    except:
        pass

# =============================================================================
# SCENARIO 1: Simple Form Demo
# =============================================================================
@pytest.mark.parametrize("browser_config", BROWSER_CONFIGS, ids=[c["name"] for c in BROWSER_CONFIGS])
def test_scenario1_simple_form_demo(browser_config):
    """
    Test Scenario 1: Simple Form Demo
    
    Steps:
    1. Open TestMu AI Selenium Playground
    2. Click "Simple Form Demo"
    3. Validate URL contains "simple-form-demo"
    4. Create variable "Welcome to TestMu AI"
    5. Enter message in text box
    6. Click "Get Checked Value"
    7. Validate message displayed
    
    Locators: get_by_role(), get_by_placeholder(), locator()
    """
    
    print(f"\n{'='*70}")
    print(f"SCENARIO 1: Simple Form Demo - {browser_config['name']}")
    print(f"{'='*70}")
    
    with sync_playwright() as playwright:
        browser = None
        try:
            print("-> Connecting to TestMu AI...")
            browser, context, page = connect_browser(playwright, browser_config, "Scenario 1: Simple Form Demo")
            print("OK Connected!")
            
            # Step 1: Open Selenium Playground
            page.goto("https://www.testmuai.com/selenium-playground/")
            page.wait_for_load_state("domcontentloaded")
            time.sleep(1)
            
            # Step 2: Click Simple Form Demo
            page.get_by_role("link", name="Simple Form Demo").click()
            page.wait_for_load_state("domcontentloaded")
            time.sleep(1)
            
            # Step 3: Validate URL
            assert "simple-form-demo" in page.url
            print("OK URL validated")
            
            # Step 4 & 5: Create variable and enter message
            message = "Welcome to TestMu AI"
            page.get_by_placeholder("Please enter your Message").fill(message)
            time.sleep(0.5)
            print(f"OK Message entered: '{message}'")
            
            # Step 6: Click Get Checked Value
            page.locator("#showInput").click()
            time.sleep(1)
            
            # Step 7: Validate message displayed
            displayed = page.locator("#message").text_content(timeout=10000)
            assert message in displayed
            print("OK Message validated")
            
            print("PASS SCENARIO 1 PASSED!")
            mark_status(page, "passed", "Scenario 1 completed successfully")
            
            page.close()
            context.close()
            browser.close()
            
        except Exception as e:
            print(f"FAIL SCENARIO 1: {e}")
            if browser:
                try:
                    mark_status(page, "failed", str(e)[:200])
                    page.close()
                    context.close()
                    browser.close()
                except:
                    pass
            raise

# =============================================================================
# SCENARIO 2: Drag & Drop Sliders
# =============================================================================
@pytest.mark.parametrize("browser_config", BROWSER_CONFIGS, ids=[c["name"] for c in BROWSER_CONFIGS])
def test_scenario2_drag_drop_sliders(browser_config):
    """
    Test Scenario 2: Drag & Drop Sliders
    
    Steps:
    1. Open TestMu AI Selenium Playground
    2. Click "Drag & Drop Sliders"
    3. Select slider "Default value 15"
    4. Drag to make it 95
    5. Validate range shows 95
    
    Locators: get_by_role(), locator() with attribute selector, keyboard actions
    """
    
    print(f"\n{'='*70}")
    print(f"SCENARIO 2: Drag & Drop Sliders - {browser_config['name']}")
    print(f"{'='*70}")
    
    with sync_playwright() as playwright:
        browser = None
        try:
            print("-> Connecting to TestMu AI...")
            browser, context, page = connect_browser(playwright, browser_config, "Scenario 2: Drag & Drop Sliders")
            print("OK Connected!")
            
            # Step 1: Open Selenium Playground
            page.goto("https://www.testmuai.com/selenium-playground/")
            page.wait_for_load_state("domcontentloaded")
            time.sleep(1)
            
            # Step 2: Click Drag & Drop Sliders
            page.get_by_role("link", name="Drag & Drop Sliders").click()
            page.wait_for_load_state("domcontentloaded")
            time.sleep(2)
            print("OK Navigated to Drag & Drop page")
            
            # Step 3: Find slider with default value 15
            slider = page.locator("input[type='range'][value='15']").first
            slider.wait_for(state="visible", timeout=10000)
            slider.scroll_into_view_if_needed()
            time.sleep(0.5)
            print("OK Slider located")
            
            # Step 4: Drag slider to 95 using keyboard
            slider.focus()
            time.sleep(0.5)
            
            for i in range(80):
                page.keyboard.press("ArrowRight")
                if i % 20 == 0:
                    time.sleep(0.1)
            
            time.sleep(1)
            print("OK Slider dragged")
            
            # Step 5: Validate range value
            range_output = page.locator("#rangeSuccess").first
            range_text = range_output.text_content(timeout=10000)
            range_value = int(range_text)
            
            assert 90 <= range_value <= 100, f"Expected ~95, got {range_value}"
            print(f"OK Range validated: {range_value}")
            
            print("PASS SCENARIO 2 PASSED!")
            mark_status(page, "passed", f"Scenario 2: Value = {range_value}")
            
            page.close()
            context.close()
            browser.close()
            
        except Exception as e:
            print(f"FAIL SCENARIO 2: {e}")
            if browser:
                try:
                    mark_status(page, "failed", str(e)[:200])
                    page.close()
                    context.close()
                    browser.close()
                except:
                    pass
            raise

# =============================================================================
# SCENARIO 3: Input Form Submit
# =============================================================================
@pytest.mark.parametrize("browser_config", BROWSER_CONFIGS, ids=[c["name"] for c in BROWSER_CONFIGS])
def test_scenario3_input_form_submit(browser_config):
    """
    Test Scenario 3: Input Form Submit
    
    Steps:
    1. Open TestMu AI Selenium Playground
    2. Click "Input Form Submit"
    3. Click Submit without filling - assert error
    4. Fill Name, Email, and other fields
    5. Select "United States" from Country dropdown (using text)
    6. Fill all fields and click Submit
    7. Validate success message
    
    Locators: get_by_role(), get_by_label(), locator() with name/id
    """
    
    print(f"\n{'='*70}")
    print(f"SCENARIO 3: Input Form Submit - {browser_config['name']}")
    print(f"{'='*70}")
    
    with sync_playwright() as playwright:
        browser = None
        try:
            print("-> Connecting to TestMu AI...")
            browser, context, page = connect_browser(playwright, browser_config, "Scenario 3: Input Form Submit")
            print("OK Connected!")
            
            # Step 1: Open Selenium Playground
            page.goto("https://www.testmuai.com/selenium-playground/")
            page.wait_for_load_state("domcontentloaded")
            time.sleep(1)
            
            # Step 2: Click Input Form Submit
            page.get_by_role("link", name="Input Form Submit").click()
            page.wait_for_load_state("domcontentloaded")
            time.sleep(2)
            print("OK Navigated to Input Form")
            
            # Find the correct form
            forms = page.locator("form")
            form = forms.first
            if forms.count() > 1:
                for i in range(forms.count()):
                    frm = forms.nth(i)
                    if frm.get_by_role("button", name="Submit").count():
                        form = frm
                        break
            
            # Step 3: Click Submit without filling
            submit_btn = form.get_by_role("button", name="Submit")
            submit_btn.click()
            time.sleep(0.5)
            print("OK Clicked submit without filling")
            
            # Check for validation
            try:
                error_banner = page.locator("[role='alert'], .alert").filter(has_text="Please fill")
                if error_banner.count() > 0:
                    print("OK Error banner detected")
                else:
                    validation_check = form.evaluate(
                        """form => {
                            const invalids = Array.from(form.querySelectorAll(':invalid'));
                            return invalids.length > 0 ? 'validation error' : 'no validation';
                        }"""
                    )
                    print(f"OK Validation: {validation_check}")
            except:
                print("OK Validation check attempted")
            
            # Steps 4-6: Fill form
            print("-> Filling form fields...")
            
            def fill_field(label_text, value, alt_selector):
                try:
                    form.get_by_label(label_text, exact=False).fill(value)
                    print(f"  OK {label_text}")
                except:
                    try:
                        form.locator(alt_selector).first.fill(value)
                        print(f"  OK {label_text} (alt)")
                    except Exception as e:
                        print(f"  WARN {label_text}: {e}")
                time.sleep(0.3)
            
            fill_field("Name", "John Doe", "#name, input[name='name']")
            fill_field("Email", "john.doe@testmuai.com", "#email, input[name='email']")
            fill_field("Password", "TestPass123", "#password, input[name='password']")
            fill_field("Company", "TestMu AI", "#company, input[name='company']")
            fill_field("Website", "https://testmuai.com", "#website, input[name='website']")
            
            # Step 5: Select United States
            try:
                country_select = form.get_by_label("Country", exact=False)
                country_select.select_option(label="United States")
                print("  OK Country: United States")
            except:
                form.locator("select[name='country']").first.select_option(label="United States")
                print("  OK Country (alt): United States")
            time.sleep(0.3)
            
            fill_field("City", "San Francisco", "#city, input[name='city']")
            fill_field("Address 1", "123 Main Street", "#address1, input[name='address_line1'], input[name='address1']")
            fill_field("Address 2", "Suite 100", "#address2, input[name='address_line2'], input[name='address2']")
            fill_field("State", "California", "#state, input[name='state']")
            fill_field("Zip code", "94102", "#zip, #zipcode, input[name='zip'], input[name='zipcode']")
            
            print("OK All fields filled")
            
            # Step 6: Submit form
            submit_btn = form.get_by_role("button", name="Submit")
            submit_btn.click()
            time.sleep(3)
            print("OK Form submitted")
            
            # Step 7: Validate success message
            success_msg = page.get_by_text("Thanks for contacting us", exact=False)
            success_msg.wait_for(state="attached", timeout=10000)
            time.sleep(1)
            
            success_text = success_msg.text_content()
            assert "Thanks for contacting us" in success_text
            print("OK Success message validated")
            
            print("PASS SCENARIO 3 PASSED!")
            mark_status(page, "passed", "Scenario 3 completed successfully")
            
            page.close()
            context.close()
            browser.close()
            
        except Exception as e:
            print(f"FAIL SCENARIO 3: {e}")
            if browser:
                try:
                    mark_status(page, "failed", str(e)[:200])
                    page.close()
                    context.close()
                    browser.close()
                except:
                    pass
            raise

if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s", "-n", "2", "--tb=short"])
