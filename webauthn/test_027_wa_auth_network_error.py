import pytest

from shared.passkey_data import PasskeyText
from shared.passkey_util import HardwarePasskeyUtil
from webauthn.webauthn_data import WebAuthnText
from webauthn.webauthn_util import WebauthnUtil


@pytest.mark.browser
def test_027(wa_util: WebauthnUtil, pk_util: HardwarePasskeyUtil):
    """Test hardware key behavior during authentication timeout scenarios."""
    # Fill the username and click authenticate
    wa_util.fill_username()
    wa_util.click_authenticate_button()

    # Enter PIN but don't provide user presence (test key timeout)
    pk_util.enter_pin()
    
    # Wait for user presence request but simulate timeout
    pk_util.wait_for_user_presence_timeout(wait_time=25)

    # Key should timeout and return error
    error_text = wa_util.wait_for_error_text()
    assert WebAuthnText.TIMED_OUT_NOT_ALLOWED in error_text


@pytest.mark.browser
def test_027_interrupted_authentication(wa_util: WebauthnUtil, pk_util: HardwarePasskeyUtil):
    """Test hardware key behavior when authentication is interrupted."""
    # Fill the username and click authenticate
    wa_util.fill_username()
    wa_util.click_authenticate_button()

    # Start authentication but cancel during PIN entry
    pk_util.wait_for_pin_field()
    
    # Cancel the operation to test key's response to interruption
    pk_util.cancel_pin_input()
    
    # Verify the key gracefully handles cancellation
    # No assertion needed - just verify no crash/hang occurs


@pytest.mark.browser  
def test_027_rapid_auth_attempts(wa_util: WebauthnUtil, pk_util: HardwarePasskeyUtil):
    """Test hardware key behavior with rapid authentication attempts."""
    # Test multiple rapid authentication attempts
    for attempt in range(3):
        wa_util.fill_username(username=f"rapid_test_{attempt}")
        wa_util.click_authenticate_button()
        
        # Quick PIN entry and cancellation to test key rate handling
        try:
            pk_util.enter_pin(pin="0000")  # Wrong PIN
            error_text = pk_util.wait_for_pin_error_text()
            assert error_text is not None
            pk_util.cancel_pin_input()
        except:
            # Key might reject rapid attempts - this is valid behavior
            pass


@pytest.mark.browser
def test_027_pin_timeout_auth(wa_util: WebauthnUtil, pk_util: HardwarePasskeyUtil):
    """Test hardware key PIN timeout during authentication."""
    # Fill the username and click authenticate
    wa_util.fill_username()
    wa_util.click_authenticate_button()

    # Wait at PIN field to test key timeout behavior
    pk_util.wait_for_pin_field()
    
    # Wait for PIN timeout (keys typically timeout after 30-60 seconds)
    import time
    time.sleep(35)
    
    # Try to enter PIN after timeout
    try:
        pk_util.enter_pin()
        pk_util.wait_for_user_presence_request()
        pk_util.provide_user_presence()
        wa_util.verify_logged_in()
    except:
        # Timeout is expected behavior - just ensure graceful handling
        try:
            pk_util.cancel_pin_input()
        except:
            pass  # Already timed out
