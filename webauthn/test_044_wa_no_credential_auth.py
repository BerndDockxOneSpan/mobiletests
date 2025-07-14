import time
import pytest

from shared.passkey_util import HardwarePasskeyUtil
from webauthn.webauthn_data import WebAuthnText
from webauthn.webauthn_util import WebauthnUtil


@pytest.mark.browser
def test_044(wa_util: WebauthnUtil, pk_util: HardwarePasskeyUtil):
    """Test hardware key behavior when authenticating with no saved credential."""
    # Use a username that definitely has no saved credential
    wa_util.fill_username(username="nonexistent_user_12345")
    wa_util.click_authenticate_button()

    # The system should immediately show an error without involving the hardware key
    # since no credential exists for this username
    error_text = wa_util.wait_for_error_text()
    assert WebAuthnText.NO_CREDENTIALS in error_text


@pytest.mark.browser
def test_044_fresh_user_no_credential(wa_util: WebauthnUtil):
    """Test authentication attempt with completely fresh username."""
    # Try to authenticate with a user that has never been registered
    wa_util.fill_username(username="fresh_test_user_never_registered")
    wa_util.click_authenticate_button()

    # Should get no credentials error immediately
    error_text = wa_util.wait_for_error_text()
    assert WebAuthnText.NO_CREDENTIALS in error_text


@pytest.mark.browser  
def test_044_deleted_credential_auth(wa_util: WebauthnUtil, pk_util: HardwarePasskeyUtil):
    """Test authentication after credential has been deleted."""
    username = "deleted_credential_test"
    
    # First register a credential
    wa_util.fill_username(username=username)
    wa_util.click_register_button()
    pk_util.do_registration_flow()
    wa_util.verify_registered_success()

    # Authenticate successfully to verify credential exists
    wa_util.fill_username(username=username)
    wa_util.click_authenticate_button()
    pk_util.do_authentication_flow()
    wa_util.verify_logged_in()

    # Delete the credential
    wa_util.delete_credentials()
    wa_util.log_out()

    # Now try to authenticate with the deleted credential
    wa_util.fill_username(username=username)
    wa_util.click_authenticate_button()
    
    # Should get no credentials error
    error_text = wa_util.wait_for_error_text()
    assert WebAuthnText.NO_CREDENTIALS in error_text


@pytest.mark.browser
def test_044_case_sensitive_username(wa_util: WebauthnUtil, pk_util: HardwarePasskeyUtil):
    """Test if username case sensitivity affects credential lookup."""
    username = "CaseSensitiveTest"
    
    # Register with specific case
    wa_util.fill_username(username=username)
    wa_util.click_register_button()
    pk_util.do_registration_flow()
    wa_util.verify_registered_success()
    time.sleep(2)  # Wait for a moment before trying to authenticate
    # Try to authenticate with different case
    wa_util.fill_username(username=username.lower())  # "casesensitivetest"
    wa_util.click_authenticate_button()
    
    # Username lookup should be case sensitive, so different case should fail
    # Should get no credentials error immediately without hardware key interaction
    error_text = wa_util.wait_for_error_text()
    assert WebAuthnText.NO_CREDENTIALS in error_text
    
    # Clean up - authenticate with correct case to delete credential
    wa_util.fill_username(username=username)
    wa_util.click_authenticate_button()
    pk_util.do_authentication_flow()
    wa_util.verify_logged_in()
    wa_util.delete_credentials()
    wa_util.log_out()
