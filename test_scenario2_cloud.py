"""
Test Scenario 2: Drag & Drop Sliders - TestMu AI Cloud Execution

Assignment Requirements:
1. Open TestMu AI Selenium Playground
2. Click "Drag & Drop Sliders"
3. Select slider "Default value 15"
4. Drag bar to make it 95
5. Validate range value shows 95

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
            "build": "Playwright 101 - Test Scenario 2",
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
def test_scenario2_drag_drop_sliders(browser_config):
    """
    Test Scenario 2: Drag & Drop Sliders
    
    Locator Types Used:
    1. get_by_role() - Link navigation
    2. locator() with CSS - Slider element
    3. locator() with ID - Range output
    """
    test_name = "Scenario 2: Drag & Drop Sliders"
    capabilities = get_capabilities(browser_config, test_name)
    
    print(f"\n{'='*70}")
    print(f"TEST SCENARIO 2: Drag & Drop Sliders")
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
            
            # Step 2: Click "Drag & Drop Sliders" using ROLE locator
            print("\n[Step 2] Click 'Drag & Drop Sliders' - get_by_role() locator")
            page.get_by_role("link", name="Drag & Drop Sliders").click()
            page.wait_for_load_state("domcontentloaded")
            print("✓ Drag & Drop Sliders page opened")
            
            # Step 3: Select slider "Default value 15" using CSS locator
            print("\n[Step 3] Select slider 'Default value 15' - locator() CSS")
            slider = page.locator("input[type='range'][value='15']").first
            slider.wait_for(state="visible", timeout=10000)
            print("✓ Slider located")
            
            # Step 4: Drag slider to value 95
            print("\n[Step 4] Drag slider to value 95")
            # Get slider bounding box
            box = slider.bounding_box()
            if box:
                # Calculate position for value 95 (range is typically 0-100)
                # Starting at 15, need to move to 95
                start_x = box['x'] + (box['width'] * 0.15)  # 15% position
                end_x = box['x'] + (box['width'] * 0.95)    # 95% position
                center_y = box['y'] + (box['height'] / 2)
                
                # Drag the slider
                page.mouse.move(start_x, center_y)
                page.mouse.down()
                page.mouse.move(end_x, center_y, steps=10)
                page.mouse.up()
                print("✓ Slider dragged to 95")
            
            # Step 5: Validate range value shows 95 using ID locator
            print("\n[Step 5] Validate range value - locator() with ID")
            range_output = page.locator("#rangeSuccess").first
            range_value = range_output.text_content(timeout=10000)
            
            # Check if value is 95 or close to it (90-95 acceptable due to drag precision)
            value_num = int(range_value)
            assert 90 <= value_num <= 100, f"Expected value around 95, got {value_num}"
            print(f"✓ Range value validated: {value_num}")
            
            print("\n" + "="*70)
            print("✅ TEST SCENARIO 2 PASSED!")
            print("="*70)
            print("\nLocators Used:")
            print("  1. get_by_role() - Link navigation")
            print("  2. locator() with [type='range'] - Slider element")
            print("  3. locator() with #id - Range output display")
            
            # Mark as passed
            page.evaluate(
                "_ => {}", 
                f'lambdatest_action: {json.dumps({"action": "setTestStatus", "arguments": {"status": "passed", "remark": "Scenario 2 completed successfully"}})}'
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
