import pytest

from shared.passkey_util import HardwarePasskeyUtil
from webauthn.webauthn_data import WebAuthnText
from webauthn.webauthn_util import WebauthnUtil


@pytest.mark.slow
@pytest.mark.browser
def test_007(wa_util: WebauthnUtil, pk_util: HardwarePasskeyUtil):
    # Fill the username and click register, use a different username to prevent conflicts with the already registered one
    wa_util.fill_username(username="fx7other")
    wa_util.click_register_button()

    # Go through the registration flow
    pk_util.do_registration_flow_until_pin_input()
    pk_util.enter_pin()

    # Let the request timeout
    pk_util.wait_for_user_presence_timeout()

    # Verify the error
    assert wa_util.wait_for_error_text() == WebAuthnText.UNKNOWN_EXCEPTION
