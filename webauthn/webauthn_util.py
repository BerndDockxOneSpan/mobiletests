import time

from shared.appium_util import DriverController
from shared.passkey_util import DEFAULT_USERNAME
from webauthn.webauthn_data import *


class WebauthnUtil:
    def __init__(self, controller: DriverController):
        self.controller = controller

    def open_page(self):
        """ Open the webauthn.io page. """
        self.controller.open_url('https://webauthn.io/')

    def fill_username(self, username: str = DEFAULT_USERNAME):
        """ Fill the username field. """
        self.controller.find_element(WebAuthnLocators.USERNAME_BOX).send_keys(username)

    def click_register_button(self):
        """ Press the register button. """
        self.controller.find_element(WebAuthnLocators.REGISTER_BUTTON).click()

    def click_authenticate_button(self):
        """ Press the authenticate button. """
        self.controller.find_element(WebAuthnLocators.AUTHENTICATE_BUTTON).click()

    def wait_for_success_text(self) -> str:
        """ Wait for success text to appear and return it. """
        element = self.controller.wait_for_element(WebAuthnLocators.SUCCESS_BOX)
        return element.text

    def wait_for_error_text(self) -> str:
        """ Wait for the error text to appear and return it. """
        element = self.controller.wait_for_element(WebAuthnLocators.ERROR_BOX)
        return element.text

    def verify_registered_success(self):
        """ Check that the passkey saved successfully text is present. """
        text = self.wait_for_success_text()
        assert text == WebAuthnText.REGISTER_SUCCESS

    def verify_logged_in(self):
        """ Verify that we are logged in. """
        self.controller.wait_for_element(WebAuthnLocators.LOGGED_IN_TEXT)

    def delete_credentials(self):
        """ Delete all credentials for the currently logged-in user. """
        button = self.controller.find_element(WebAuthnLocators.DELETE_BUTTON)
        while button is not None:
            button.click()
            # Small delay to give the site time to update and prevent stale references
            time.sleep(0.5)
            button = self.controller.find_element_or_none(WebAuthnLocators.DELETE_BUTTON)

    def log_out(self):
        """ Log out the user. """
        self.controller.find_element(WebAuthnLocators.LOG_OUT_BUTTON).click()
