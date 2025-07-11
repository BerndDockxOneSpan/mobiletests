import pytest

from shared.passkey_data import PasskeyText
from shared.passkey_util import HardwarePasskeyUtil
from webauthn.webauthn_util import WebauthnUtil


@pytest.mark.browser
def test_022(wa_util: WebauthnUtil, pk_util: HardwarePasskeyUtil):
    # Fill the username and click register
    wa_util.fill_username()
    wa_util.click_authenticate_button()

    # Go through the authentication flow
    pk_util.enter_pin(pin="4321")
    # Verify the error
    assert pk_util.wait_for_pin_error_text() == PasskeyText.SEVEN_ATTEMPTS_REMAINING

    # Try again with correct pin
    pk_util.do_authentication_flow()
    # Verify success
    wa_util.verify_logged_in()

