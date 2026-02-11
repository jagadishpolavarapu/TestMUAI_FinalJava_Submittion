"""
Test Scenario 1: Simple Form Demo - TestMu AI Cloud Execution

Assignment Requirements:
1. Open TestMu AI's Selenium Playground
2. Click "Simple Form Demo"
3. Validate URL contains "simple-form-demo"
4. Create variable "Welcome to TestMu AI"
5. Enter message in text box
6. Click "Get Checked Value"
7. Validate message displayed

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
            "build": "Playwright 101 - Test Scenario 1",
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
def test_scenario1_simple_form_demo(browser_config):
    """
    Test Scenario 1: Simple Form Demo
    
    Locator Types Used:
    1. get_by_role() - ARIA role-based locator
    2. get_by_placeholder() - Placeholder locator
    3. locator() - CSS selector
    """
    test_name = "Scenario 1: Simple Form Demo"
    capabilities = get_capabilities(browser_config, test_name)
    
    print(f"\n{'='*70}")
    print(f"TEST SCENARIO 1: Simple Form Demo")
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
            
            # Step 2: Click "Simple Form Demo" using ROLE locator
            print("\n[Step 2] Click 'Simple Form Demo' - get_by_role() locator")
            page.get_by_role("link", name="Simple Form Demo").click()
            page.wait_for_load_state("domcontentloaded")
            print("✓ Simple Form Demo clicked")
            
            # Step 3: Validate URL contains "simple-form-demo"
            print("\n[Step 3] Validate URL contains 'simple-form-demo'")
            current_url = page.url
            assert "simple-form-demo" in current_url, f"URL validation failed: {current_url}"
            print(f"✓ URL validated: {current_url}")
            
            # Step 4: Create variable for message
            print("\n[Step 4] Create variable for message")
            message = "Welcome to TestMu AI"
            print(f"✓ Variable created: '{message}'")
            
            # Step 5: Enter message using PLACEHOLDER locator
            print("\n[Step 5] Enter message - get_by_placeholder() locator")
            message_input = page.get_by_placeholder("Please enter your Message")
            message_input.fill(message)
            print(f"✓ Message entered: '{message}'")
            
            # Step 6: Click "Get Checked Value" using CSS locator
            print("\n[Step 6] Click 'Get Checked Value' - locator() CSS selector")
            page.locator("#showInput").click()
            print("✓ Button clicked")
            
            # Step 7: Validate message displayed using CSS locator
            print("\n[Step 7] Validate message displayed - locator() CSS selector")
            message_display = page.locator("#message")
            displayed_text = message_display.text_content(timeout=10000)
            assert message in displayed_text, f"Expected '{message}' but got '{displayed_text}'"
            print(f"✓ Message validated: '{displayed_text}'")
            
            print("\n" + "="*70)
            print("✅ TEST SCENARIO 1 PASSED!")
            print("="*70)
            print("\nLocators Used:")
            print("  1. get_by_role() - Link navigation")
            print("  2. get_by_placeholder() - Input field")
            print("  3. locator() - Button and message display")
            
            # Mark as passed
            page.evaluate(
                "_ => {}", 
                f'lambdatest_action: {json.dumps({"action": "setTestStatus", "arguments": {"status": "passed", "remark": "Scenario 1 completed successfully"}})}'
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
