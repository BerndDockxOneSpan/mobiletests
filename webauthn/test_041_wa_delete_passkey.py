import pytest

from shared.passkey_util import HardwarePasskeyUtil
from webauthn.webauthn_data import WebAuthnText
from webauthn.webauthn_util import WebauthnUtil

@pytest.mark.browser
def test_041(wa_util: WebauthnUtil, pk_util: HardwarePasskeyUtil):
    # Fill the username and click register
    wa_util.fill_username()
    wa_util.click_authenticate_button()

    # Go through the authentication flow
    pk_util.do_authentication_flow()
    wa_util.verify_logged_in()

    # Delete the credential
    wa_util.delete_credentials()

    # Log out
    wa_util.log_out()

    # verify the credential was deleted
    wa_util.fill_username()
    wa_util.click_authenticate_button()
    assert wa_util.wait_for_error_text() == WebAuthnText.NO_CREDENTIALS
