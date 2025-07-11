import pytest

from shared.passkey_util import HardwarePasskeyUtil
from webauthn.webauthn_util import WebauthnUtil

@pytest.mark.browser
def test_021(wa_util: WebauthnUtil, pk_util: HardwarePasskeyUtil):
    # Fill the username and click register
    wa_util.fill_username()
    wa_util.click_authenticate_button()

    # Go through the authentication flow
    pk_util.do_authentication_flow()

    wa_util.verify_logged_in()
