import pytest

from shared.passkey_util import HardwarePasskeyUtil
from webauthn.webauthn_data import WebAuthnText
from webauthn.webauthn_util import WebauthnUtil


@pytest.mark.browser
def test_005(wa_util: WebauthnUtil, pk_util: HardwarePasskeyUtil):
    # Fill the username and click register
    wa_util.fill_username()
    wa_util.click_register_button()

    # Go through the registration flow
    pk_util.do_registration_flow_until_pin_input()
    pk_util.wait_for_pin_field()

    # Cancel the input
    pk_util.cancel_pin_input()

    # Verify the error
    assert wa_util.wait_for_error_text() == WebAuthnText.TIMED_OUT_NOT_ALLOWED
