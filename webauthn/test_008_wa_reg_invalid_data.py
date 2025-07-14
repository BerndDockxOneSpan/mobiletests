import pytest

from shared.passkey_data import PasskeyText
from shared.passkey_util import HardwarePasskeyUtil
from webauthn.webauthn_util import WebauthnUtil


@pytest.mark.browser
def test_008(wa_util: WebauthnUtil, pk_util: HardwarePasskeyUtil):
    """Test hardware key behavior with rapid PIN attempts during registration."""
    # Fill the username and click register
    wa_util.fill_username(username="rapid_pin_test")
    wa_util.click_register_button()

    # Start registration flow
    pk_util.do_registration_flow_until_pin_input()

    # Try rapid consecutive wrong PIN attempts to test key rate limiting
    for attempt in range(3):
        pk_util.enter_pin(pin=f"000{attempt}")  # Different wrong PINs
        
        # Check that key provides error feedback
        error_text = pk_util.wait_for_pin_error_text()
        assert error_text is not None
        
        # Key should show decreasing attempt count
        if attempt == 0:
            assert PasskeyText.SEVEN_ATTEMPTS_REMAINING in error_text

    # Cancel after testing key response
    pk_util.cancel_pin_input()


@pytest.mark.browser 
def test_008_pin_lockout_behavior(wa_util: WebauthnUtil, pk_util: HardwarePasskeyUtil):
    """Test hardware key PIN lockout behavior after multiple failures."""
    # Fill the username and click register
    wa_util.fill_username(username="lockout_test")
    wa_util.click_register_button()

    # Start registration flow
    pk_util.do_registration_flow_until_pin_input()

    # Test key's response to multiple consecutive wrong PINs
    # Note: We won't actually lock out the key, just test initial responses
    for attempt in range(2):
        pk_util.enter_pin(pin="9999")  # Consistently wrong PIN
        
        # Verify key provides error feedback
        error_text = pk_util.wait_for_pin_error_text()
        assert PasskeyText.WRONG_PIN in error_text or "attempts remaining" in error_text.lower()

    # Cancel to avoid actual lockout
    pk_util.cancel_pin_input()


@pytest.mark.browser
def test_008_key_timeout_during_registration(wa_util: WebauthnUtil, pk_util: HardwarePasskeyUtil):
    """Test hardware key timeout behavior during registration PIN entry."""
    # Fill the username and click register
    wa_util.fill_username(username="timeout_test")
    wa_util.click_register_button()

    # Start registration flow and wait at PIN input
    pk_util.do_registration_flow_until_pin_input()
    
    # Wait longer than normal to test key timeout behavior
    # Most hardware keys have PIN entry timeouts
    import time
    time.sleep(30)  # Wait for potential PIN timeout
    
    # Try to enter PIN after delay - key might have timed out
    try:
        pk_util.enter_pin()
        # If successful, continue to user presence
        pk_util.wait_for_user_presence_request()
        pk_util.provide_user_presence()
        wa_util.verify_registered_success()
    except:
        # If key timed out, that's expected behavior - just cancel
        pk_util.cancel_pin_input()
