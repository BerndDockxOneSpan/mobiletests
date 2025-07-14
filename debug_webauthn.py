#!/usr/bin/env python3
"""
WebAuthn Hardware Authenticator Diagnostic Script
Helps diagnose why the authenticator popup isn't appearing.
"""

import time
from pathlib import Path
import subprocess

def create_debug_step_definition():
    """Create a debug step that adds more detailed logging and waiting."""
    debug_step = """
@when('I click the register button with debug')
def step_click_register_button_debug(context):
    \"\"\"Click the register button with detailed debugging.\"\"\"
    log.info("=== DEBUG: Starting registration process ===")
    
    if not context.wa_util:
        raise RuntimeError("WebAuthn utility not initialized")
    
    # Take screenshot before clicking
    try:
        context.driver.save_screenshot("debug_before_register.png")
        log.info("Screenshot saved: debug_before_register.png")
    except Exception as e:
        log.info(f"Could not save screenshot: {e}")
    
    # Click register button
    log.info("Clicking register button...")
    context.wa_util.click_register_button()
    
    # Wait a bit for WebAuthn API to start
    log.info("Waiting 3 seconds for WebAuthn API to initialize...")
    time.sleep(3)
    
    # Take screenshot after clicking
    try:
        context.driver.save_screenshot("debug_after_register.png")
        log.info("Screenshot saved: debug_after_register.png")
    except Exception as e:
        log.info(f"Could not save screenshot: {e}")
    
    # Check if any popups appeared
    try:
        from shared.passkey_data import PasskeyLocators
        
        # Look for various possible popup elements
        log.info("Checking for popup elements...")
        
        # Check for "Create passkey" text variations
        create_texts = [
            PasskeyLocators.CREATE_PASSKEY_TEXT_1,
            PasskeyLocators.CREATE_PASSKEY_TEXT_2
        ]
        
        for i, locator in enumerate(create_texts):
            try:
                element = context.driver_controller.find_element_or_none(locator)
                if element:
                    log.info(f"✅ Found CREATE_PASSKEY_TEXT_{i+1}: {element.text}")
                else:
                    log.info(f"❌ CREATE_PASSKEY_TEXT_{i+1} not found")
            except Exception as e:
                log.info(f"❌ Error checking CREATE_PASSKEY_TEXT_{i+1}: {e}")
        
        # Check for "Different device" button
        try:
            diff_device = context.driver_controller.find_element_or_none(PasskeyLocators.DIFFERENT_DEVICE)
            if diff_device:
                log.info(f"✅ Found DIFFERENT_DEVICE button: {diff_device.text}")
            else:
                log.info("❌ DIFFERENT_DEVICE button not found")
        except Exception as e:
            log.info(f"❌ Error checking DIFFERENT_DEVICE: {e}")
            
        # Look for any dialog or popup elements
        try:
            # Common Android popup/dialog indicators
            popup_indicators = [
                "//android.widget.Button",
                "//android.app.Dialog",
                "//*[contains(@text, 'passkey')]",
                "//*[contains(@text, 'security')]", 
                "//*[contains(@text, 'authenticator')]"
            ]
            
            for indicator in popup_indicators:
                try:
                    from shared.locator import Locator, Context
                    locator = Locator(Context.NATIVE, "xpath", indicator)
                    elements = context.driver.find_elements(locator.by, locator.value)
                    if elements:
                        log.info(f"✅ Found {len(elements)} elements matching: {indicator}")
                        for j, elem in enumerate(elements[:3]):  # Show first 3
                            try:
                                log.info(f"   Element {j}: {elem.text}")
                            except:
                                log.info(f"   Element {j}: <no text>")
                    else:
                        log.info(f"❌ No elements found for: {indicator}")
                except Exception as e:
                    log.info(f"❌ Error checking {indicator}: {e}")
                    
        except Exception as e:
            log.info(f"Error during popup detection: {e}")
            
    except Exception as e:
        log.info(f"Error during debug checks: {e}")
    
    log.info("=== DEBUG: Registration process analysis complete ===")

@when('I wait for hardware authenticator popup')
def step_wait_for_hardware_popup(context):
    \"\"\"Wait specifically for hardware authenticator popup with timeout.\"\"\"
    log.info("Waiting for hardware authenticator popup...")
    
    max_wait = 10  # 10 seconds
    wait_interval = 0.5
    waited = 0
    
    from shared.passkey_data import PasskeyLocators
    
    while waited < max_wait:
        try:
            # Check for the main popup indicators
            element = context.driver_controller.find_element_or_none(PasskeyLocators.CREATE_PASSKEY_TEXT_1)
            if element:
                log.info(f"✅ Hardware authenticator popup appeared after {waited:.1f}s")
                return
                
            element = context.driver_controller.find_element_or_none(PasskeyLocators.CREATE_PASSKEY_TEXT_2) 
            if element:
                log.info(f"✅ Hardware authenticator popup appeared after {waited:.1f}s")
                return
                
        except Exception as e:
            log.info(f"Error checking for popup: {e}")
        
        time.sleep(wait_interval)
        waited += wait_interval
        
        if waited % 2 == 0:  # Log every 2 seconds
            log.info(f"Still waiting for popup... ({waited}s elapsed)")
    
    log.info(f"❌ Hardware authenticator popup did not appear after {max_wait}s")
    
    # Take final screenshot
    try:
        context.driver.save_screenshot("debug_popup_timeout.png")
        log.info("Screenshot saved: debug_popup_timeout.png")
    except Exception as e:
        log.info(f"Could not save timeout screenshot: {e}")
    
    raise TimeoutError(f"Hardware authenticator popup did not appear within {max_wait} seconds")
"""
    
    # Write to both step definition files
    step_files = [
        "step_definitions/webauthn_steps.py",
        "features/steps/webauthn_steps.py"
    ]
    
    for step_file in step_files:
        try:
            with open(step_file, 'a', encoding='utf-8') as f:
                f.write("\n# === DEBUG STEPS ===\n")
                f.write("import time\n")
                f.write(debug_step)
            print(f"✅ Added debug steps to {step_file}")
        except Exception as e:
            print(f"❌ Failed to add debug steps to {step_file}: {e}")

def create_debug_feature():
    """Create a simple debug feature file."""
    debug_feature = """Feature: WebAuthn Debug
  Debug WebAuthn hardware authenticator integration

  Background:
    Given I have a DIGIPASS FX7 device connected
    And I am on the WebAuthn registration page

  @debug @hardware @registration
  Scenario: Debug registration flow
    Given I enter username "debug_test"
    When I click the register button with debug
    And I wait for hardware authenticator popup
    Then the registration should succeed
"""
    
    debug_dir = Path("features/debug")
    debug_dir.mkdir(exist_ok=True)
    
    debug_file = debug_dir / "debug.feature"
    try:
        debug_file.write_text(debug_feature, encoding='utf-8')
        print(f"✅ Created debug feature: {debug_file}")
        return str(debug_file)
    except Exception as e:
        print(f"❌ Failed to create debug feature: {e}")
        return None

def main():
    print("🔧 WebAuthn Hardware Authenticator Diagnostic")
    print("=" * 50)
    
    print("\n📝 Adding debug step definitions...")
    create_debug_step_definition()
    
    print("\n📄 Creating debug feature file...")
    debug_file = create_debug_feature()
    
    if debug_file:
        print(f"\n🚀 To run debug test:")
        print(f"behave {debug_file}")
        print(f"\n📸 Debug screenshots will be saved as:")
        print("  - debug_before_register.png")
        print("  - debug_after_register.png") 
        print("  - debug_popup_timeout.png (if timeout occurs)")
        
        print(f"\n💡 This will help identify:")
        print("  1. If WebAuthn API is triggered correctly")
        print("  2. What elements appear after clicking register")
        print("  3. Timing issues with popup appearance")
        print("  4. Hardware authenticator detection problems")
    
if __name__ == "__main__":
    main()
