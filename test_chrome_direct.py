"""
Direct Chrome test for WebAuthn registration flow
This bypasses Appium and tests directly in Chrome browser
"""
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

def test_webauthn_chrome():
    """Test WebAuthn registration directly in Chrome"""
    
    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--enable-web-bluetooth")
    chrome_options.add_argument("--enable-webauthn-ctap2-support")
    chrome_options.add_argument("--enable-webauthn-testing-api")
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    
    print("🚀 Starting Chrome browser...")
    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 10)
    
    try:
        # Navigate to WebAuthn.io
        print("🌐 Opening webauthn.io...")
        driver.get("https://webauthn.io/")
        
        # Wait for page to load
        time.sleep(3)
        print("✅ Page loaded")
        
        # Take a screenshot
        driver.save_screenshot("chrome_webauthn_loaded.png")
        print("📸 Screenshot saved: chrome_webauthn_loaded.png")
        
        # Find and fill username
        print("📝 Filling username...")
        username_box = wait.until(EC.presence_of_element_located((By.ID, "input-email")))
        username_box.clear()
        username_box.send_keys("chrome_test_user")
        print("✅ Username filled")
        
        # Take screenshot after username
        driver.save_screenshot("chrome_username_filled.png")
        print("📸 Screenshot saved: chrome_username_filled.png")
        
        # Click register button
        print("🔘 Clicking register button...")
        register_button = driver.find_element(By.ID, "register-button")
        register_button.click()
        print("✅ Register button clicked")
        
        # Wait for WebAuthn popup or response
        print("⏳ Waiting for WebAuthn prompt...")
        time.sleep(5)  # Give time for WebAuthn prompt to appear
        
        # Take screenshot to see what happens
        driver.save_screenshot("chrome_after_register_click.png")
        print("📸 Screenshot saved: chrome_after_register_click.png")
        
        # Check if any error messages appear
        try:
            error_element = driver.find_element(By.CLASS_NAME, "alert-danger")
            if error_element.is_displayed():
                print(f"❌ Error found: {error_element.text}")
        except:
            print("ℹ️  No error messages found")
        
        # Check for success
        try:
            success_element = driver.find_element(By.CLASS_NAME, "alert-success")
            if success_element.is_displayed():
                print(f"✅ Success: {success_element.text}")
        except:
            print("ℹ️  No success message found")
        
        # Check page title and current URL
        print(f"📄 Page title: {driver.title}")
        print(f"🔗 Current URL: {driver.current_url}")
        
        # Wait a bit more to see if anything happens
        print("⏳ Waiting additional time for any popups...")
        time.sleep(10)
        
        # Final screenshot
        driver.save_screenshot("chrome_final_state.png")
        print("📸 Final screenshot saved: chrome_final_state.png")
        
        print("✅ Test completed successfully")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        driver.save_screenshot("chrome_error_state.png")
        print("📸 Error screenshot saved: chrome_error_state.png")
        
    finally:
        print("🔚 Closing browser...")
        driver.quit()

if __name__ == "__main__":
    test_webauthn_chrome()
