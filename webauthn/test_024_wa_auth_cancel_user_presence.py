import pytest

from shared.passkey_util import HardwarePasskeyUtil
from webauthn.webauthn_data import WebAuthnText
from webauthn.webauthn_util import WebauthnUtil


@pytest.mark.browser
def test_024(wa_util: WebauthnUtil, pk_util: HardwarePasskeyUtil):
    # Fill the username and click register
    wa_util.fill_username()
    wa_util.click_authenticate_button()

    # Enter the pin and wait for user presence to be requested
    pk_util.enter_pin()
    pk_util.wait_for_user_presence_request()

    # Cancel by pressing the back button
    wa_util.controller.press_back_button()

    # Verify the error
    assert wa_util.wait_for_error_text() == WebAuthnText.TIMED_OUT_NOT_ALLOWED


