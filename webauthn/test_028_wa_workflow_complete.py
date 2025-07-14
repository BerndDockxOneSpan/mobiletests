import pytest

from shared.passkey_util import HardwarePasskeyUtil
from webauthn.webauthn_data import WebAuthnText
from webauthn.webauthn_util import WebauthnUtil


@pytest.mark.browser
def test_028(wa_util: WebauthnUtil, pk_util: HardwarePasskeyUtil):
    """Test complete workflow: register, authenticate, then delete passkey."""
    # Step 1: Register a new passkey
    wa_util.fill_username(username="workflow_test")
    wa_util.click_register_button()
    pk_util.do_registration_flow()
    wa_util.verify_registered_success()

    # Step 2: Authenticate with the registered passkey
    wa_util.fill_username(username="workflow_test")
    wa_util.click_authenticate_button()
    pk_util.do_authentication_flow()
    wa_util.verify_logged_in()

    # Step 3: Delete the credential
    wa_util.delete_credentials()
    wa_util.log_out()

    # Step 4: Verify the credential was deleted
    wa_util.fill_username(username="workflow_test")
    wa_util.click_authenticate_button()
    error_text = wa_util.wait_for_error_text()
    assert WebAuthnText.NO_CREDENTIALS in error_text


@pytest.mark.browser
def test_028_multiple_users(wa_util: WebauthnUtil, pk_util: HardwarePasskeyUtil):
    """Test workflow with multiple different usernames."""
    usernames = ["user1", "user2", "test@example.com"]
    
    for username in usernames:
        # Register each user
        wa_util.fill_username(username=username)
        wa_util.click_register_button()
        pk_util.do_registration_flow()
        wa_util.verify_registered_success()

        # Authenticate each user
        wa_util.fill_username(username=username)
        wa_util.click_authenticate_button()
        pk_util.do_authentication_flow()
        wa_util.verify_logged_in()

        # Clean up - delete credentials and log out
        wa_util.delete_credentials()
        wa_util.log_out()


@pytest.mark.browser
def test_028_register_then_failed_auth(wa_util: WebauthnUtil, pk_util: HardwarePasskeyUtil):
    """Test register successfully, then fail authentication with wrong pin."""
    # Register successfully
    wa_util.fill_username(username="fail_auth_test")
    wa_util.click_register_button()
    pk_util.do_registration_flow()
    wa_util.verify_registered_success()

    # Try to authenticate with wrong pin
    wa_util.fill_username(username="fail_auth_test")
    wa_util.click_authenticate_button()
    
    # Enter wrong pin during authentication
    pk_util.enter_pin(pin="9999")  # Wrong pin
    
    # Should get pin error
    error_text = pk_util.wait_for_pin_error_text()
    assert error_text is not None and len(error_text) > 0
