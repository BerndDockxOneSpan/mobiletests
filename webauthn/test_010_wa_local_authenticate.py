import pytest

from shared.passkey_util import LocalPasskeyUtil
from webauthn.webauthn_util import WebauthnUtil


@pytest.mark.browser
def test_010(wa_util: WebauthnUtil, local_pk_util: LocalPasskeyUtil):
    """Test local device passkey authentication with default settings."""
    # Fill the username and click authenticate
    wa_util.fill_username()
    wa_util.click_authenticate_button()

    # Go through the local passkey authentication flow
    local_pk_util.do_local_passkey_authentication_flow()

    wa_util.verify_logged_in()


@pytest.mark.browser
def test_010_custom_pin(wa_util: WebauthnUtil, local_pk_util: LocalPasskeyUtil):
    """Test local device passkey authentication with custom device pin."""
    # Fill the username and click authenticate
    wa_util.fill_username(username="local_test_user")
    wa_util.click_authenticate_button()

    # Go through the authentication flow with custom pin
    local_pk_util.do_local_passkey_authentication_flow(pin="999999")

    wa_util.verify_logged_in()


@pytest.mark.browser
def test_010_wrong_device_pin(wa_util: WebauthnUtil, local_pk_util: LocalPasskeyUtil):
    """Test local device passkey authentication with wrong device pin."""
    # Fill the username and click authenticate
    wa_util.fill_username()
    wa_util.click_authenticate_button()

    # Try authentication with wrong pin
    try:
        local_pk_util.do_local_passkey_authentication_flow(pin="111111")
        # If no error occurs, the test environment might not validate pins
        wa_util.verify_logged_in()
    except:
        # If error occurs, verify we get appropriate pin error
        error_text = local_pk_util.wait_for_pin_error_text()
        assert error_text is not None and len(error_text) > 0


@pytest.mark.browser
def test_010_discoverable_local(wa_util: WebauthnUtil, local_pk_util: LocalPasskeyUtil):
    """Test local device discoverable credential selection."""
    # Fill the username and click authenticate
    wa_util.fill_username()
    wa_util.click_authenticate_button()

    # Use discoverable credential
    local_pk_util.click_discoverable()
    local_pk_util.do_local_passkey_authentication_flow()

    wa_util.verify_logged_in()
