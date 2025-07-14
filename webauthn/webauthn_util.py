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

    # BDD-friendly methods for Gherkin step definitions

    def is_success_message_visible(self) -> bool:
        """Check if success message is visible."""
        try:
            element = self.controller.find_element_or_none(WebAuthnLocators.SUCCESS_BOX)
            return element is not None and element.is_displayed()
        except Exception:
            return False

    def is_pin_error_message_visible(self) -> bool:
        """Check if PIN error message is visible."""
        try:
            error_element = self.controller.find_element_or_none(WebAuthnLocators.ERROR_BOX)
            if error_element and error_element.is_displayed():
                return "PIN" in error_element.text or "pin" in error_element.text
            return False
        except Exception:
            return False

    def is_error_message_visible(self, error_type: str) -> bool:
        """Check if specific error message type is visible."""
        try:
            error_element = self.controller.find_element_or_none(WebAuthnLocators.ERROR_BOX)
            if error_element and error_element.is_displayed():
                error_text = error_element.text.lower()
                return error_type.lower() in error_text
            return False
        except Exception:
            return False

    def is_timeout_error_message_visible(self) -> bool:
        """Check if timeout error message is visible."""
        return self.is_error_message_visible("timeout") or self.is_error_message_visible("timed out")

    def is_lockout_error_message_visible(self) -> bool:
        """Check if lockout error message is visible."""
        return self.is_error_message_visible("locked") or self.is_error_message_visible("attempts")

    def is_logged_in(self) -> bool:
        """Check if user is currently logged in."""
        try:
            element = self.controller.find_element_or_none(WebAuthnLocators.LOGGED_IN_TEXT)
            return element is not None and element.is_displayed()
        except Exception:
            return False

    def verify_registration_failed(self):
        """Verify that registration failed."""
        error_element = self.controller.wait_for_element(WebAuthnLocators.ERROR_BOX)
        assert error_element.is_displayed(), "Expected registration failure, but no error message shown"

    def verify_authentication_failed(self):
        """Verify that authentication failed."""
        error_element = self.controller.wait_for_element(WebAuthnLocators.ERROR_BOX)
        assert error_element.is_displayed(), "Expected authentication failure, but no error message shown"

    def verify_timeout_error(self):
        """Verify that a timeout error occurred."""
        assert self.is_timeout_error_message_visible(), "Expected timeout error message not found"

    def navigate_to_registration_page(self):
        """Navigate to the registration page."""
        self.open_page()
        # Additional navigation logic if needed

    def navigate_to_authentication_page(self):
        """Navigate to the authentication page."""
        self.open_page()
        # Additional navigation logic if needed
