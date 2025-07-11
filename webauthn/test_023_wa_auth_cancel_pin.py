import pytest

from shared.passkey_util import HardwarePasskeyUtil
from webauthn.webauthn_data import WebAuthnText
from webauthn.webauthn_util import WebauthnUtil


@pytest.mark.browser
def test_023(wa_util: WebauthnUtil, pk_util: HardwarePasskeyUtil):
    # Fill the username and click register
    wa_util.fill_username()
    wa_util.click_authenticate_button()

    # Cancel pin input
    pk_util.cancel_pin_input()

    # Verify the error
    assert wa_util.wait_for_error_text() == WebAuthnText.TIMED_OUT_NOT_ALLOWED


