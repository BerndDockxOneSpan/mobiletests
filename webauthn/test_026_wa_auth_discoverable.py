import pytest

from shared.passkey_data import PasskeyText
from shared.passkey_util import HardwarePasskeyUtil
from webauthn.webauthn_util import WebauthnUtil


@pytest.mark.browser
def test_026(wa_util: WebauthnUtil, pk_util: HardwarePasskeyUtil):
    # Fill the username and click register
    wa_util.click_authenticate_button()

    # Select the correct credential
    pk_util.do_discoverable_flow()

    # Verify success
    wa_util.verify_logged_in()
