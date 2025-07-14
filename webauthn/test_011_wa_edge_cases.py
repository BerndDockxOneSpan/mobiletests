import pytest

from shared.passkey_util import HardwarePasskeyUtil
from webauthn.webauthn_util import WebauthnUtil


@pytest.mark.browser
def test_011(wa_util: WebauthnUtil, pk_util: HardwarePasskeyUtil):
    """Test registration with multiple pin retry attempts."""
    # Fill the username and click register
    wa_util.fill_username(username="multi_retry_test")
    wa_util.click_register_button()

    # Start registration flow
    pk_util.do_registration_flow_until_pin_input()

    # Try wrong pin multiple times
    for attempt in range(3):
        pk_util.enter_pin(pin="0000")  # Wrong pin
        
        # Check for error message
        error_text = pk_util.wait_for_pin_error_text()
        assert error_text is not None
        
        # If not the last attempt, continue
        if attempt < 2:
            # Cancel and restart pin entry for next attempt
            pk_util.cancel_pin_input()
            # Restart the flow
            wa_util.click_register_button()
            pk_util.do_registration_flow_until_pin_input()

    # After multiple failures, cancel the operation
    pk_util.cancel_pin_input()


@pytest.mark.browser
def test_011_pin_success_after_failure(wa_util: WebauthnUtil, pk_util: HardwarePasskeyUtil):
    """Test successful pin entry after initial failure."""
    # Fill the username and click register
    wa_util.fill_username(username="retry_success_test")
    wa_util.click_register_button()

    # Start registration flow
    pk_util.do_registration_flow_until_pin_input()

    # Try wrong pin first
    pk_util.enter_pin(pin="9876")  # Wrong pin
    error_text = pk_util.wait_for_pin_error_text()
    assert error_text is not None

    # Cancel and try again with correct pin
    pk_util.cancel_pin_input()
    
    # Restart the flow
    wa_util.click_register_button()
    pk_util.do_registration_flow_until_pin_input()
    
    # Now use correct pin
    pk_util.enter_pin()  # Default correct pin
    pk_util.wait_for_user_presence_request()
    pk_util.provide_user_presence()

    wa_util.verify_registered_success()


@pytest.mark.browser
def test_011_key_state_persistence(wa_util: WebauthnUtil, pk_util: HardwarePasskeyUtil):
    """Test hardware key state persistence across operations."""
    # Test that key maintains proper state between operations
    wa_util.fill_username(username="state_test")
    wa_util.click_register_button()
    
    # Complete registration
    pk_util.do_registration_flow()
    wa_util.verify_registered_success()
    
    # Immediately try authentication to test key state transition
    wa_util.fill_username(username="state_test")
    wa_util.click_authenticate_button()
    pk_util.do_authentication_flow()
    wa_util.verify_logged_in()


@pytest.mark.browser  
def test_011_user_presence_timing(wa_util: WebauthnUtil, pk_util: HardwarePasskeyUtil):
    """Test hardware key user presence timing requirements."""
    # Fill the username and click register
    wa_util.fill_username(username="presence_timing_test")
    wa_util.click_register_button()

    # Start registration flow
    pk_util.do_registration_flow_until_pin_input()
    pk_util.enter_pin()
    
    # Test key behavior with delayed user presence
    pk_util.wait_for_user_presence_request()
    
    # Wait a few seconds before providing presence (test key patience)
    import time
    time.sleep(5)
    
    pk_util.provide_user_presence()
    wa_util.verify_registered_success()


@pytest.mark.browser
def test_011_multiple_key_operations(wa_util: WebauthnUtil, pk_util: HardwarePasskeyUtil):
    """Test hardware key behavior with multiple rapid operations."""
    # Test key's ability to handle multiple operations in sequence
    operations = ["op1", "op2", "op3"]
    
    for op in operations:
        # Register
        wa_util.fill_username(username=f"multi_{op}")
        wa_util.click_register_button()
        pk_util.do_registration_flow()
        wa_util.verify_registered_success()
        
        # Authenticate
        wa_util.fill_username(username=f"multi_{op}")
        wa_util.click_authenticate_button()
        pk_util.do_authentication_flow()
        wa_util.verify_logged_in()
        
        # Cleanup
        wa_util.delete_credentials()
        wa_util.log_out()
        
        # Small delay between operations to test key recovery
        import time
        time.sleep(1)
