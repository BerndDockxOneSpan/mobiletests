#!/usr/bin/env python3
"""
Test script to verify context handling in Gherkin vs pytest
"""

import sys
import os
import time
import logging

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from shared.appium_util import DriverController
from webauthn.webauthn_util import WebauthnUtil
from appium import webdriver
from appium.options.android import UiAutomator2Options

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
log = logging.getLogger(__name__)

def test_context_handling():
    """Test if we can properly handle web context switching"""
    
    log.info("🔄 Starting context handling test...")
    
    # Setup Appium driver
    base_capabilities = {
        'platformName': 'Android',
        'automationName': 'uiautomator2',
        'deviceName': 'Android',
        'nativeWebScreenshot': True,
        'browserName': 'Chrome'
    }
    
    appium_server_url = 'http://localhost:4723'
    
    try:
        # Create Appium driver
        driver = webdriver.Remote(
            appium_server_url, 
            options=UiAutomator2Options().load_capabilities(base_capabilities)
        )
        
        log.info("✅ Appium driver created successfully")
        
        # Create controller and WebAuthn utility
        controller = DriverController(driver)
        wa_util = WebauthnUtil(controller)
        
        log.info("✅ WebAuthn utility created")
        
        # Open the page
        log.info("🌐 Opening WebAuthn page...")
        wa_util.open_page()
        
        # Wait a bit for the page to load
        time.sleep(3)
        
        # Check available contexts
        log.info("🔍 Checking available contexts...")
        available_contexts = driver.contexts
        log.info(f"Available contexts: {available_contexts}")
        
        # Look for a web context
        web_context = None
        for ctx in available_contexts:
            if 'WEBVIEW' in ctx or 'CHROMIUM' in ctx:
                web_context = ctx
                break
        
        if web_context:
            log.info(f"✅ Found web context: {web_context}")
            log.info(f"🔄 Switching to web context...")
            driver.switch_to.context(web_context)
            log.info("✅ Successfully switched to web context")
            
            # Now try to fill the username
            log.info("✏️ Attempting to fill username...")
            wa_util.fill_username(username="context_test")
            log.info("✅ Successfully filled username!")
            
        else:
            log.error("❌ No web context found!")
            
        # Save a screenshot
        driver.save_screenshot("context_test_screenshot.png")
        log.info("📸 Screenshot saved: context_test_screenshot.png")
        
    except Exception as e:
        log.error(f"❌ Test failed: {e}")
        import traceback
        log.error(f"Full traceback: {traceback.format_exc()}")
        return False
    
    finally:
        try:
            driver.quit()
            log.info("🚪 Driver closed")
        except:
            pass
    
    log.info("✅ Context handling test completed")
    return True

if __name__ == "__main__":
    test_context_handling()
