import pytest

from shared.passkey_util import HardwarePasskeyUtil
from webauthn.webauthn_data import WebAuthnText
from webauthn.webauthn_util import WebauthnUtil


@pytest.mark.slow
@pytest.mark.browser
def test_025(wa_util: WebauthnUtil, pk_util: HardwarePasskeyUtil):
    # Fill the username and click register
    wa_util.fill_username()
    wa_util.click_authenticate_button()

    # Enter the pin and wait for user presence to be requested
    pk_util.enter_pin()

    # Wait for the user presence request to timeout
    pk_util.wait_for_user_presence_timeout()

    # Verify the error
    assert wa_util.wait_for_error_text() == WebAuthnText.TIMED_OUT_NOT_ALLOWED


