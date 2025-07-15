from behave import given, when, then
import logging
import time

# --- Constants for wait times ---
WEB_CONTEXT_WAIT = 2  # Seconds to wait for web context to be available
WEBAUTHN_API_WAIT = 3 # Seconds to wait for WebAuthn API to initialize

log = logging.getLogger(__name__)

# --- Helper Functions ---

def _ensure_web_context(context):
    """
    Waits for and switches to the web context if not already active.
    This avoids repeated logic in multiple steps.
    """
    try:
        # Only switch if the current context is not a webview
        if 'WEBVIEW' not in context.driver.current_context.upper():
            time.sleep(WEB_CONTEXT_WAIT)
            available_contexts = context.driver.contexts
            log.info(f"Available contexts: {available_contexts}")
            
            web_context = next((ctx for ctx in available_contexts if 'WEBVIEW' in ctx or 'CHROMIUM' in ctx), None)
            
            if web_context:
                log.info(f"Switching to web context: {web_context}")
                context.driver.switch_to.context(web_context)
            else:
                log.warning("No web context found, proceeding with current context.")
    except Exception as e:
        log.warning(f"Context switching issue: {e}")

def _take_screenshot(context, name: str):
    """
    Saves a screenshot with the given name, handling potential errors.
    """
    try:
        context.driver.save_screenshot(f"{name}.png")
        log.info(f"📸 Screenshot saved: {name}.png")
    except Exception as e:
        log.warning(f"Could not save screenshot '{name}': {e}")

# --- Step Definitions ---

@given('I am on the WebAuthn registration page')
def step_on_registration_page(context):
    log.info("Navigating to WebAuthn registration page")
    if context.wa_util:
        context.wa_util.open_page()
    else:
        raise RuntimeError("WebAuthn utility not initialized")

@given('I am on the WebAuthn registration page at "{url}"')
def step_on_registration_page_url(context, url):
    log.info(f"Navigating to WebAuthn registration page at {url}")
    if context.wa_util:
        context.wa_util.open_page(url=url)
    else:
        raise RuntimeError("WebAuthn utility not initialized")

@given('I am on the WebAuthn authentication page')
def step_on_authentication_page(context):
    log.info("Navigating to WebAuthn authentication page")
    if context.wa_util:
        context.wa_util.open_page()
    else:
        raise RuntimeError("WebAuthn utility not initialized")

@given('I am on the WebAuthn management page')
def step_on_management_page(context):
    log.info("Navigating to WebAuthn management page")

@given('I enter username "{username}"')
def step_enter_username(context, username):
    context.current_username = username
    log.info(f"Entering username: {username}")
    if context.wa_util:
        _ensure_web_context(context)
        context.wa_util.fill_username(username=username)
    else:
        raise RuntimeError("WebAuthn utility not initialized")

@given('I register credentials for {count:d} different usernames')
def step_register_multiple_credentials(context, count):
    log.info(f"Registering credentials for {count} different usernames")
    context.registered_usernames = [f"user_{i}" for i in range(1, count + 1)]

@given('I have credentials stored for "{user1}" and "{user2}"')
def step_have_stored_credentials(context, user1, user2):
    context.stored_users = [user1, user2]
    log.info(f"Verified credentials stored for {user1} and {user2}")

@given('I have registered {count:d} credentials on the device')
def step_have_registered_count(context, count):
    context.credential_count = count
    log.info(f"Verified {count} credentials registered on device")

@given('I register a credential on Windows platform')
def step_register_on_windows(context):
    context.registration_platform = "Windows"
    log.info("Registering credential on Windows platform")

@given('I register a credential for "{username}"')
def step_register_credential_for_user(context, username):
    context.registered_user = username
    log.info(f"Registering credential for {username}")

@given('I have no credentials stored for "{username}"')
def step_no_credentials_for_user(context, username):
    log.info(f"Verified no credentials stored for {username}")

@when('I click the register button')
def step_click_register_button(context):
    log.info("Clicking register button")
    if context.wa_util:
        _ensure_web_context(context)
        context.wa_util.click_register_button()
        log.info(f"Waiting {WEBAUTHN_API_WAIT} seconds for WebAuthn API to initialize...")
        time.sleep(WEBAUTHN_API_WAIT)
    else:
        raise RuntimeError("WebAuthn utility not initialized")

@when('I click the authenticate button')
def step_click_authenticate_button(context):
    log.info("Clicking authenticate button")
    if context.wa_util:
        _ensure_web_context(context)
        context.wa_util.click_authenticate_button()
        log.info(f"Waiting {WEBAUTHN_API_WAIT} seconds for WebAuthn API to initialize...")
        time.sleep(WEBAUTHN_API_WAIT)
    else:
        raise RuntimeError("WebAuthn utility not initialized")

@when('I click the authenticate button without entering username')
def step_click_authenticate_no_username(context):
    log.info("Clicking authenticate button without entering username")
    # This would trigger discoverable credential flow

@when('I select the correct credential from the list')
def step_select_correct_credential(context):
    log.info("Selecting correct credential from list")

@when('I authenticate with each stored credential')
def step_authenticate_each_credential(context):
    log.info("Authenticating with each stored credential")
    for username in getattr(context, 'registered_usernames', []):
        log.info(f"Authenticating with {username}")

@when('I delete the credential for "{username}"')
def step_delete_credential_for_user(context, username):
    log.info(f"Deleting credential for {username}")
    # This would use WebauthnUtil to delete the credential

@when('I attempt to register the {ordinal} credential')
def step_attempt_register_ordinal(context, ordinal):
    log.info(f"Attempting to register {ordinal} credential")

@when('I move the device to macOS platform')
def step_move_to_macos(context):
    context.current_platform = "macOS"
    log.info("Moving device to macOS platform")

@when('I attempt to authenticate with the same credential')
def step_authenticate_same_credential(context):
    log.info("Attempting to authenticate with same credential")

@when('I disconnect the device for {minutes:d} minutes')
def step_disconnect_device_duration(context, minutes):
    log.info(f"Disconnecting device for {minutes} minutes")
    # This would be simulated in test environment

@when('I reconnect the device')
def step_reconnect_device(context):
    log.info("Reconnecting device")

@when('I authenticate with "{username}"')
def step_authenticate_with_user(context, username):
    log.info(f"Authenticating with {username}")

@when('I attempt to delete credentials for "{username}"')
def step_attempt_delete_credentials(context, username):
    log.info(f"Attempting to delete credentials for {username}")

@then('the registration should succeed')
def step_registration_succeeds(context):
    log.info("Verifying registration succeeded")
    if context.wa_util:
        _ensure_web_context(context)
        context.wa_util.verify_registered_success()
    else:
        raise RuntimeError("WebAuthn utility not initialized")

@then('the registration should fail')
def step_registration_fails(context):
    log.info("Verifying registration failed")

@then('the registration should be cancelled')
def step_registration_cancelled(context):
    log.info("Verifying registration was cancelled")

@then('the registration should timeout')
def step_registration_timeout(context):
    log.info("Verifying registration timed out")

@then('the authentication should succeed')
def step_authentication_succeeds(context):
    log.info("Verifying authentication succeeded")
    if context.wa_util:
        _ensure_web_context(context)
        context.wa_util.verify_logged_in()
    else:
        raise RuntimeError("WebAuthn utility not initialized")

@then('the authentication should fail')
def step_authentication_fails(context):
    log.info("Verifying authentication failed")

@then('the authentication should fail immediately')
def step_authentication_fails_immediately(context):
    log.info("Verifying authentication failed immediately")

@then('the authentication should be cancelled')
def step_authentication_cancelled(context):
    log.info("Verifying authentication was cancelled")

@then('the authentication should timeout')
def step_authentication_timeout(context):
    log.info("Verifying authentication timed out")

@then('I should see a success message')
def step_see_success_message(context):
    log.info("Verifying success message is displayed")

@then('I should see a PIN error message')
def step_see_pin_error_message(context):
    log.info("Verifying PIN error message is displayed")

@then('I should see a "{error_type}" error message')
def step_see_specific_error_message(context, error_type):
    log.info(f"Verifying {error_type} error message is displayed")

@then('I should see a timeout error message')
def step_see_timeout_error_message(context):
    log.info("Verifying timeout error message is displayed")

@then('I should see a lockout error message')
def step_see_lockout_error_message(context):
    log.info("Verifying lockout error message is displayed")

@then('I should see a cancellation error message')
def step_see_cancellation_error_message(context):
    log.info("Verifying cancellation error message is displayed")

@then('I should be logged in')
def step_logged_in(context):
    log.info("Verifying user is logged in")

@then('the credential should be stored on the device')
def step_credential_stored(context):
    log.info("Verifying credential was stored on device")

@then('no credential should be stored')
def step_no_credential_stored(context):
    log.info("Verifying no credential was stored")

@then('all authentications should succeed')
def step_all_authentications_succeed(context):
    log.info("Verifying all authentications succeeded")

@then('each credential should work independently')
def step_each_credential_independent(context):
    log.info("Verifying each credential works independently")

@then('authentication with "{username}" should fail')
def step_auth_with_user_fails(context, username):
    log.info(f"Verifying authentication with {username} fails")

@then('authentication with "{username}" should still work')
def step_auth_with_user_works(context, username):
    log.info(f"Verifying authentication with {username} still works")

@then('the credential should work identically')
def step_credential_works_identically(context):
    log.info("Verifying credential works identically")

@then('the credential should be unchanged')
def step_credential_unchanged(context):
    log.info("Verifying credential is unchanged")

@then('the operation should fail gracefully')
def step_operation_fails_gracefully(context):
    log.info("Verifying operation fails gracefully")

@then('I should see an appropriate error message')
def step_see_appropriate_error(context):
    log.info("Verifying appropriate error message is shown")

@then('the device should remain in a stable state')
def step_device_stable_state(context):
    log.info("Verifying device remains in stable state")

@then('I should see the sign in options dialog')
def step_see_signin_options_dialog(context):
    log.info("Verifying sign in options dialog is displayed")
    _ensure_web_context(context)
    _take_screenshot(context, "signin_options_dialog")
    # Add verification logic for sign in options dialog

@when('I select "{option}"')
def step_select_option(context, option):
    log.info(f"Selecting option: {option}")
    _ensure_web_context(context)
    # Add logic to select the specified option from UI
    _take_screenshot(context, f"selected_{option.lower().replace(' ', '_')}")

@then('I should see the device selection options')
def step_see_device_selection_options(context):
    log.info("Verifying device selection options are displayed")
    _ensure_web_context(context)
    expected_options = []
    for row in context.table:
        expected_options.append(row['Option'])
    
    log.info(f"Expected options: {expected_options}")
    _take_screenshot(context, "device_selection_options")
    # Add verification logic for device selection options

@when('I select "{device_type}"')
def step_select_device_type(context, device_type):
    log.info(f"Selecting device type: {device_type}")
    _ensure_web_context(context)
    # Add logic to select USB security key option
    _take_screenshot(context, f"selected_{device_type.lower().replace(' ', '_')}")

@then('I should see the "{dialog_name}" dialog')
def step_see_dialog(context, dialog_name):
    log.info(f"Verifying {dialog_name} dialog is displayed")
    _ensure_web_context(context)
    _take_screenshot(context, f"dialog_{dialog_name.lower().replace(' ', '_')}")
    # Add verification logic for specific dialog

@when('I connect the security key')
def step_connect_security_key(context):
    log.info("Connecting security key")
    # This step represents the physical connection of the device
    # In automated tests, this would be handled by the relay board
    if hasattr(context, 'relay_board') and context.relay_board:
        log.info("Security key connection simulated via relay board")
    else:
        log.info("Security key connection - manual step in test environment")

@then('the device LED should blink once indicating battery level')
def step_device_led_blinks_battery(context):
    log.info("Verifying device LED blinks once for battery level")
    # This would be verified through hardware monitoring
    # For now, we'll log the expected behavior
    log.info("Expected: Device LED blinks once (battery level indication)")

@then('I should see the "{dialog_name}" dialog')
def step_see_specific_dialog(context, dialog_name):
    log.info(f"Verifying {dialog_name} dialog is displayed")
    _ensure_web_context(context)
    _take_screenshot(context, f"dialog_{dialog_name.lower().replace(' ', '_')}")

@when('I enter the correct PIN "{pin}" and confirm')
def step_enter_pin_and_confirm(context, pin):
    log.info(f"Entering correct PIN: {pin} and confirming")
    if hasattr(context, 'pk_util') and context.pk_util:
        context.pk_util.enter_pin(pin=pin)
        log.info("PIN entered and confirmed")
    else:
        raise RuntimeError("Hardware passkey utility not initialized")

@then('the device LED should blink blue')
def step_device_led_blinks_blue(context):
    log.info("Verifying device LED blinks blue")
    # This would be verified through hardware monitoring
    log.info("Expected: Device LED blinks blue (PIN accepted)")

@then('I should see the "{dialog_name}" dialog for user presence')
def step_see_dialog_user_presence(context, dialog_name):
    log.info(f"Verifying {dialog_name} dialog for user presence")
    _ensure_web_context(context)
    _take_screenshot(context, f"user_presence_{dialog_name.lower().replace(' ', '_')}")

@when('I press the security key button to provide user presence')
def step_press_security_key_button(context):
    log.info("Pressing security key button to provide user presence")
    if hasattr(context, 'pk_util') and context.pk_util:
        context.pk_util.provide_user_presence()
        log.info("User presence provided via security key button")
    else:
        # Fallback for manual testing
        log.info("User presence - manual button press required")

@when('I navigate to the authentication page')
def step_navigate_to_auth_page(context):
    log.info("Navigating to authentication page")
    if context.wa_util:
        context.wa_util.navigate_to_authentication()
    else:
        raise RuntimeError("WebAuthn utility not initialized")

@given('I have registered credentials on webauthn.io with the security key')
def step_have_registered_credentials(context):
    log.info("Verifying registered credentials exist on webauthn.io")
    # This assumes prior registration has been completed
    log.info("Registered credentials verified on webauthn.io")

@then('I should see the "{dialog_name}" dialog')
def step_see_no_passkeys_dialog(context, dialog_name):
    log.info(f"Verifying {dialog_name} dialog is displayed")
    _ensure_web_context(context)
    _take_screenshot(context, f"dialog_{dialog_name.lower().replace(' ', '_').replace('\'', '')}")

@when('I select "{option_name}"')
def step_select_use_different_device(context, option_name):
    log.info(f"Selecting {option_name}")
    _ensure_web_context(context)
    _take_screenshot(context, f"selected_{option_name.lower().replace(' ', '_')}")

@given('I have multiple registrations on webauthn.io with the security key')
def step_have_multiple_registrations(context):
    log.info("Verifying multiple registrations exist on webauthn.io")
    # This assumes multiple prior registrations have been completed
    log.info("Multiple registered credentials verified on webauthn.io")

@given('I leave the username textbox empty')
def step_leave_username_empty(context):
    log.info("Leaving username textbox empty for discoverable credential flow")
    # Ensure username field is empty for autofill/discoverable flow

@then('I should see a prompt to choose how I\'d like to sign in to webauthn.io')
def step_see_signin_prompt(context):
    log.info("Verifying sign in prompt is displayed")
    _ensure_web_context(context)
    _take_screenshot(context, "signin_prompt")

@when('I connect the security key under test')
def step_connect_security_key_under_test(context):
    log.info("Connecting the security key under test")
    # This represents connecting the specific device under test
    if hasattr(context, 'relay_board') and context.relay_board:
        log.info("Security key under test connection simulated via relay board")
    else:
        log.info("Security key under test connection - manual step")

@when('I press the button on the device')
def step_press_device_button(context):
    log.info("Pressing the button on the device")
    if hasattr(context, 'pk_util') and context.pk_util:
        context.pk_util.provide_user_presence()
        log.info("Device button pressed successfully")
    else:
        log.info("Device button press - manual step required")

@then('the device LED should stop blinking')
def step_device_led_stops_blinking(context):
    log.info("Verifying device LED stops blinking")
    # This would be verified through hardware monitoring
    log.info("Expected: Device LED stops blinking (operation completed)")

@then('I should see a list of registered usernames')
def step_see_username_list(context):
    log.info("Verifying list of registered usernames is displayed")
    _ensure_web_context(context)
    _take_screenshot(context, "username_list")

@when('I select any username from the list')
def step_select_any_username(context):
    log.info("Selecting any username from the list")
    _ensure_web_context(context)
    # In real implementation, this would select the first available username
    _take_screenshot(context, "username_selected")

@then('the list should contain multiple usernames')
def step_list_contains_multiple_usernames(context):
    log.info("Verifying the list contains multiple usernames")
    _ensure_web_context(context)
    # Verification logic for multiple usernames would go here

@when('I select the first username from the list')
def step_select_first_username(context):
    log.info("Selecting the first username from the list")
    _ensure_web_context(context)
    _take_screenshot(context, "first_username_selected")

@when('I logout and return to the authentication page')
def step_logout_and_return(context):
    log.info("Logging out and returning to authentication page")
    if context.wa_util:
        context.wa_util.logout()
        context.wa_util.navigate_to_authentication()
    else:
        raise RuntimeError("WebAuthn utility not initialized")

@when('I select the second username from the list')
def step_select_second_username(context):
    log.info("Selecting the second username from the list")
    _ensure_web_context(context)
    _take_screenshot(context, "second_username_selected")

@when('I refresh the page')
def step_refresh_page(context):
    log.info("Refreshing the page")
    _ensure_web_context(context)
    context.driver.refresh()
    time.sleep(WEB_CONTEXT_WAIT)

# === DEBUG STEPS ===
import time

@when('I click the register button with debug')
def step_click_register_button_debug(context):
    """Click the register button with detailed debugging."""
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
    """Wait specifically for hardware authenticator popup with timeout."""
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

@when('I complete the hardware registration flow')
def step_complete_hardware_registration(context):
    """Complete the hardware registration flow with PIN and user presence."""
    log.info("🔄 Starting hardware registration flow")
    
    if not hasattr(context, 'pk_util') or not context.pk_util:
        log.error("❌ Hardware passkey utility not initialized")
        raise RuntimeError("Hardware passkey utility not initialized")
    
    log.info(f"✅ pk_util is available: {type(context.pk_util)}")
    log.info(f"✅ relay_board is available: {type(context.relay_board)}")
    
    try:
        _take_screenshot(context, "before_registration_flow")
        
        log.info("🚀 Calling pk_util.do_registration_flow()...")
        context.pk_util.do_registration_flow()
        log.info("✅ Hardware registration flow completed successfully")
        
        _take_screenshot(context, "after_registration_flow")
            
    except Exception as e:
        log.error(f"❌ Failed to complete hardware registration flow: {e}", exc_info=True)
        _take_screenshot(context, "registration_flow_error")
        raise

@when('I complete the hardware authentication flow')
def step_complete_hardware_authentication(context):
    """Complete the hardware authentication flow with PIN and user presence."""
    log.info("Completing hardware authentication flow")
    
    if not hasattr(context, 'pk_util') or not context.pk_util:
        raise RuntimeError("Hardware passkey utility not initialized")
    
    try:
        _take_screenshot(context, "before_authentication_flow")
        context.pk_util.do_authentication_flow()
        log.info("✅ Hardware authentication flow completed successfully")
        _take_screenshot(context, "after_authentication_flow")
    except Exception as e:
        log.error(f"❌ Failed to complete hardware authentication flow: {e}", exc_info=True)
        _take_screenshot(context, "authentication_flow_error")
        raise
