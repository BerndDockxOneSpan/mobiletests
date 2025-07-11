import pytest

from shared.passkey_util import HardwarePasskeyUtil
from webauthn.webauthn_data import WebAuthnText
from webauthn.webauthn_util import WebauthnUtil


@pytest.mark.browser
def test_004(wa_util: WebauthnUtil, pk_util: HardwarePasskeyUtil):
    # Fill the username and click register
    wa_util.fill_username()
    wa_util.click_register_button()

    # Go through the registration flow
    pk_util.do_registration_flow_until_pin_input()
    pk_util.enter_pin()

    # Verify the error, this can also return UNKNOWN_ERROR in some Android versions
    text = wa_util.wait_for_error_text()
    assert text == WebAuthnText.PREVIOUSLY_REGISTERED or WebAuthnText.UNKNOWN_EXCEPTION
