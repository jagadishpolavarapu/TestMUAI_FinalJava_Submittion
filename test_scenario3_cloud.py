"""
Test Scenario 3: Input Form Submit - TestMu AI Cloud Execution

Assignment Requirements:
1. Open TestMu AI Selenium Playground
2. Click "Input Form Submit"
3. Click Submit without filling - assert error message
4. Fill Name, Email, and other fields
5. Select "United States" from Country dropdown (using text property)
6. Fill all fields and click Submit
7. Validate success message "Thanks for contacting us, we will get back to you shortly."

Execution:
- Parallel execution on 2+ browser/OS combinations
- Multiple locator types
- All capabilities enabled (network, video, console, screenshots)
"""

import os
import json
import pytest
from playwright.sync_api import sync_playwright, expect

# TestMu AI credentials
os.environ["LT_USERNAME"] = "btechjagadish"
os.environ["LT_ACCESS_KEY"] = "LT_yBAKBI6iMMJnq7xyNwWpFBr3fNTFAHpmTRU3d1ndQuPnYqc"

# Browser/OS combinations
BROWSER_CONFIGS = [
    {"browserName": "Chrome", "browserVersion": "latest", "platform": "Windows 10", "name": "Chrome_Win10"},
    {"browserName": "pw-firefox", "browserVersion": "latest", "platform": "macOS Catalina", "name": "Firefox_macOS"}
]

def get_capabilities(browser_config, test_name):
    """TestMu AI capabilities with all features enabled"""
    return {
        "browserName": browser_config["browserName"],
        "browserVersion": browser_config["browserVersion"],
        "LT:Options": {
            "platform": browser_config["platform"],
            "build": "Playwright 101 - Test Scenario 3",
            "name": f"{test_name} - {browser_config['name']}",
            "user": os.environ["LT_USERNAME"],
            "accessKey": os.environ["LT_ACCESS_KEY"],
            "network": True,
            "video": True,
            "console": True,
            "visual": True,
            "tunnel": False,
        }
    }

@pytest.mark.parametrize("browser_config", BROWSER_CONFIGS, ids=[c["name"] for c in BROWSER_CONFIGS])
def test_scenario3_input_form_submit(browser_config):
    """
    Test Scenario 3: Input Form Submit
    
    Locator Types Used:
    1. get_by_role() - Link and button navigation
    2. get_by_placeholder() - Input fields
    3. locator() with name - Form fields
    4. locator() with CSS - Success message
    """
    test_name = "Scenario 3: Input Form Submit"
    capabilities = get_capabilities(browser_config, test_name)
    
    print(f"\n{'='*70}")
    print(f"TEST SCENARIO 3: Input Form Submit")
    print(f"Browser: {browser_config['browserName']} | OS: {browser_config['platform']}")
    print(f"{'='*70}")
    
    with sync_playwright() as playwright:
        browser_name = browser_config["browserName"].lower()
        if "chrome" in browser_name or "edge" in browser_name:
            browser_type = playwright.chromium
        elif "firefox" in browser_name:
            browser_type = playwright.firefox
        else:
            browser_type = playwright.chromium
        
        ws_endpoint = f"wss://cdp.lambdatest.com/playwright?capabilities={json.dumps(capabilities)}"
        
        try:
            print("→ Connecting to TestMu AI platform...")
            browser = browser_type.connect(ws_endpoint=ws_endpoint)
            context = browser.new_context(viewport={'width': 1920, 'height': 1080})
            page = context.new_page()
            page.set_default_timeout(30000)
            print("✓ Connected to TestMu AI!")
            
            # Step 1: Open TestMu AI Selenium Playground
            print("\n[Step 1] Open TestMu AI Selenium Playground")
            page.goto("https://www.testmuai.com/selenium-playground/")
            page.wait_for_load_state("domcontentloaded")
            print("✓ Selenium Playground opened")
            
            # Step 2: Click "Input Form Submit" using ROLE locator
            print("\n[Step 2] Click 'Input Form Submit' - get_by_role() locator")
            page.get_by_role("link", name="Input Form Submit").click()
            page.wait_for_load_state("domcontentloaded")
            print("✓ Input Form Submit page opened")
            
            # Step 3: Click Submit without filling - assert error
            print("\n[Step 3] Click Submit without filling - expect validation error")
            submit_button = page.get_by_role("button", name="Submit")
            submit_button.click()
            
            # Check for HTML5 validation or error message
            name_input = page.locator("input[name='name']")
            validation_message = name_input.evaluate("el => el.validationMessage")
            assert validation_message or "fill" in validation_message.lower(), "Expected validation error"
            print(f"✓ Validation error detected: '{validation_message}'")
            
            # Step 4: Fill Name, Email, and other fields
            print("\n[Step 4] Fill form fields - using multiple locators")
            
            # Fill Name using name attribute
            print("  → Fill Name field - locator() with [name]")
            page.locator("input[name='name']").fill("John Doe")
            
            # Fill Email using name attribute
            print("  → Fill Email field - locator() with [name]")
            page.locator("input[name='email']").fill("john.doe@testmuai.com")
            
            # Fill Password using name attribute
            print("  → Fill Password field - locator() with [name]")
            page.locator("input[name='password']").fill("TestPass123!")
            
            # Fill Company using name attribute
            print("  → Fill Company field - locator() with [name]")
            page.locator("input[name='company']").fill("TestMu AI")
            
            # Fill Website using name attribute
            print("  → Fill Website field - locator() with [name]")
            page.locator("input[name='website']").fill("https://www.testmuai.com")
            
            print("✓ Basic fields filled")
            
            # Step 5: Select "United States" from Country dropdown using text property
            print("\n[Step 5] Select 'United States' from dropdown - locator() CSS")
            country_select = page.locator("select[name='country']")
            country_select.select_option(label="United States")
            print("✓ Country selected: United States")
            
            # Step 6: Fill remaining fields
            print("\n[Step 6] Fill remaining fields")
            
            # Fill City
            page.locator("input[name='city']").fill("San Francisco")
            
            # Fill Address 1
            page.locator("input[name='address_line1']").fill("123 Main Street")
            
            # Fill Address 2
            page.locator("input[name='address_line2']").fill("Suite 100")
            
            # Fill State
            page.locator("input[name='state']").fill("California")
            
            # Fill Zip Code
            page.locator("input[name='zip']").fill("94102")
            
            print("✓ All fields filled")
            
            # Step 7: Click Submit button
            print("\n[Step 7] Click Submit button - get_by_role() locator")
            submit_button.click()
            print("✓ Form submitted")
            
            # Step 8: Validate success message
            print("\n[Step 8] Validate success message - locator() CSS")
            success_message = page.locator(".success-msg, .alert-success, p.success").first
            success_text = success_message.text_content(timeout=10000)
            
            expected_message = "Thanks for contacting us, we will get back to you shortly"
            assert expected_message.lower() in success_text.lower(), f"Expected success message, got: {success_text}"
            print(f"✓ Success message validated: '{success_text}'")
            
            print("\n" + "="*70)
            print("✅ TEST SCENARIO 3 PASSED!")
            print("="*70)
            print("\nLocators Used:")
            print("  1. get_by_role() - Navigation and buttons")
            print("  2. locator() with [name] - Form input fields")
            print("  3. locator() with select - Dropdown selection")
            print("  4. locator() with CSS class - Success message")
            
            # Mark as passed
            page.evaluate(
                "_ => {}", 
                f'lambdatest_action: {json.dumps({"action": "setTestStatus", "arguments": {"status": "passed", "remark": "Scenario 3 completed successfully"}})}'
            )
            
            page.close()
            context.close()
            browser.close()
            
            print(f"\n🎉 PASSED on {browser_config['name']}")
            print("📊 View results: https://automation.lambdatest.com/")
            
        except Exception as e:
            print(f"\n❌ FAILED: {e}")
            try:
                page.evaluate(
                    "_ => {}", 
                    f'lambdatest_action: {json.dumps({"action": "setTestStatus", "arguments": {"status": "failed", "remark": str(e)[:200]}})}'
                )
                page.close()
                context.close()
                browser.close()
            except:
                pass
            raise

if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s", "-n", "2"])
