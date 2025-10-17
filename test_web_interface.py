"""
Web Interface Testing Script
Tests the N8N Workflow Generator web interface using Playwright
"""

import sys
import time

try:
    from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
    print("[OK] Playwright imported successfully")
except ImportError:
    print("[ERROR] Playwright not installed. Install it with:")
    print("  pip install playwright")
    print("  playwright install chromium")
    sys.exit(1)

def test_web_interface():
    """Test the web interface with various prompts"""
    print("\n" + "="*70)
    print("N8N WORKFLOW GENERATOR - WEB INTERFACE TEST")
    print("="*70 + "\n")
    
    with sync_playwright() as p:
        # Launch browser
        print("[*] Launching browser...")
        browser = p.chromium.launch(headless=False)  # Set to True for headless mode
        page = browser.new_page()
        
        try:
            # Navigate to the app
            print("[*] Opening http://localhost:5000...")
            page.goto("http://localhost:5000", wait_until="networkidle")
            time.sleep(2)
            
            print("[OK] Page loaded successfully\n")
            
            # Test cases
            test_cases = [
                {
                    "name": "Greeting Test (should be rejected)",
                    "prompt": "Hi",
                    "should_succeed": False
                },
                {
                    "name": "Another Greeting Test (should be rejected)",
                    "prompt": "Hello, how are you?",
                    "should_succeed": False
                },
                {
                    "name": "Valid Workflow Request #1",
                    "prompt": "Send email when webhook receives data",
                    "should_succeed": True
                },
                {
                    "name": "Valid Workflow Request #2",
                    "prompt": "Create a workflow that sends Slack notification every day at 9am",
                    "should_succeed": True
                },
                {
                    "name": "Valid Workflow Request #3",
                    "prompt": "Build workflow to save form submissions to Google Sheets",
                    "should_succeed": True
                }
            ]
            
            for i, test in enumerate(test_cases, 1):
                print(f"\n[TEST {i}/{len(test_cases)}] {test['name']}")
                print(f"  Prompt: '{test['prompt']}'")
                
                # Find input field and button
                input_field = page.locator("#promptInput")
                send_button = page.locator("#sendBtn")
                
                # Clear and type prompt
                input_field.fill(test['prompt'])
                time.sleep(0.5)
                
                # Click send button
                send_button.click()
                print("  [*] Sent prompt...")
                
                # Wait for response (up to 60 seconds for workflow generation)
                try:
                    # Wait for either success or error message
                    page.wait_for_selector(".message.bot", timeout=60000)
                    time.sleep(1)
                    
                    # Get all bot messages
                    bot_messages = page.locator(".message.bot").all()
                    if bot_messages:
                        latest_message = bot_messages[-1]
                        message_text = latest_message.text_content()
                        
                        # Check if it matches expected result
                        if test['should_succeed']:
                            if "Workflow generated successfully" in message_text or "download" in message_text.lower():
                                print("  [OK] Test passed - Workflow generated successfully")
                                
                                # Try to find download button
                                download_btn = latest_message.locator(".download-btn")
                                if download_btn.count() > 0:
                                    print("  [OK] Download button present")
                            else:
                                print(f"  [WARNING] Expected success but got: {message_text[:200]}")
                        else:
                            # Should fail (greeting/off-topic)
                            if "workflow generator assistant" in message_text.lower() or "describe" in message_text.lower():
                                print("  [OK] Test passed - Prompt correctly rejected")
                            else:
                                print(f"  [WARNING] Expected rejection but got: {message_text[:200]}")
                        
                        print(f"  Response preview: {message_text[:150]}...")
                    
                except PlaywrightTimeout:
                    print("  [ERROR] Timeout waiting for response")
                
                # Small delay between tests
                time.sleep(2)
            
            print("\n" + "="*70)
            print("TESTING COMPLETE")
            print("="*70)
            print("\n[*] Keeping browser open for manual inspection...")
            print("[*] Press Ctrl+C to close browser and exit")
            
            # Keep browser open for manual inspection
            try:
                time.sleep(300)  # Keep open for 5 minutes
            except KeyboardInterrupt:
                print("\n[*] Closing browser...")
            
        except Exception as e:
            print(f"\n[ERROR] Test failed: {e}")
            import traceback
            traceback.print_exc()
        
        finally:
            browser.close()
            print("[*] Browser closed")

if __name__ == "__main__":
    test_web_interface()
