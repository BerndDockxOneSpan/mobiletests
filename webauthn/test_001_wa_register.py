import pytest

from shared.passkey_util import HardwarePasskeyUtil
from webauthn.webauthn_util import WebauthnUtil

@pytest.mark.browser
def test_001(wa_util: WebauthnUtil, pk_util: HardwarePasskeyUtil):
    # Fill the username and click register
    wa_util.fill_username()
    wa_util.click_register_button()

    # Go through the registration flow
    pk_util.do_registration_flow()

    wa_util.verify_registered_success()
