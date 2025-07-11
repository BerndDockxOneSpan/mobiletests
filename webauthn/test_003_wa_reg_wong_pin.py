import pytest

from shared.passkey_data import PasskeyText
from shared.passkey_util import HardwarePasskeyUtil
from webauthn.webauthn_util import WebauthnUtil


@pytest.mark.browser
def test_003(wa_util: WebauthnUtil, pk_util: HardwarePasskeyUtil):
    # Fill the username and click register
    wa_util.fill_username()
    wa_util.click_register_button()

    # Go through the registration flow with the wrong pin
    pk_util.do_registration_flow_until_pin_input()
    pk_util.enter_pin(pin="98765")

    # Verify the error
    assert pk_util.wait_for_pin_error_text() == PasskeyText.SEVEN_ATTEMPTS_REMAINING

    # Close the pin input screen
    pk_util.cancel_pin_input()
