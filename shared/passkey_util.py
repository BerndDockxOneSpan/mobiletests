import time

from appium.webdriver import WebElement
from appium.webdriver.extensions.android.nativekey import AndroidKey

from RelayBoard import RelayBoard
from shared.appium_util import DriverController
from shared.locator import Locator, Context
from shared.passkey_data import PasskeyLocators

DEFAULT_USERNAME = "fx7mobile"
DEFAULT_KEY_PIN = "1234" # Pin for the hardware security key
DEFAULT_DEVICE_PIN = "125412" # Pin for the phone


class LocalPasskeyUtil:
    """ Utility class to interact with the on device passkey manager """

    def __init__(self, controller: DriverController):
        self.controller: DriverController = controller

    def enter_pin(self, pin: str = DEFAULT_DEVICE_PIN):
        """ Enter the pin in the pin input field """
        pin_field = self.controller.wait_for_element(PasskeyLocators.PIN_INPUT_FIELD_DEVICE)
        pin_field.click()
        pin_field.send_keys(pin)
        self.controller.press_key(AndroidKey.ENTER)

    def do_local_passkey_registration_flow(self, pin: str = DEFAULT_DEVICE_PIN):
        """ Do the passkey registration flow and register the passkey on the mobile device."""
        # Wait for the pop-up to open, use text to check
        self.controller.wait_for_first_element(
            [PasskeyLocators.CREATE_PASSKEY_TEXT_1, PasskeyLocators.CREATE_PASSKEY_TEXT_2])
        # Button doesn't have an id, so search for it with the index
        self.controller.find_element(Locator.by_button_index(Context.NATIVE, 2)).click()

        self.enter_pin(pin)

    def do_local_passkey_authentication_flow(self, pin: str = DEFAULT_DEVICE_PIN):
        """ Do the passkey authentication flow for a passkey stored on the mobile device."""
        # Wait for the pin field and enter the pin
        self.enter_pin(pin)

    def wait_for_pin_error_text(self):
        """ Wait for the error text to appear for a device/lock screen prompt and return it. """
        element = self.controller.wait_for_element(PasskeyLocators.PIN_ERROR_TEXT_DEVICE)
        return element.text

    def click_discoverable(self, user: str = DEFAULT_USERNAME):
        """ Click a discoverable credential, by username. """
        locator = Locator.by_text(Context.NATIVE, user)
        element = self.controller.wait_for_element(locator)
        element.click()


class HardwarePasskeyUtil:
    """ Utility class to interact with a hardware passkey """

    def __init__(self, controller: DriverController, relay_board: RelayBoard):
        self.controller: DriverController = controller
        self.relay_board: RelayBoard = relay_board

    def do_registration_flow(self, pin: str = DEFAULT_KEY_PIN):
        """ Do the passkey registration flow with the given pin. """
        self.do_registration_flow_until_pin_input()

        # Wait for pin field and enter pin
        self.enter_pin(pin)

        # Wait for user presence to be requested and provide it
        self.wait_for_user_presence_request()
        self.provide_user_presence()

    def do_registration_flow_until_pin_input(self):
        """ Do the passkey registration flow up until you have to enter the pin. """
        # Wait for the pop-up to open, use text to check
        self.controller.wait_for_first_element(
            [PasskeyLocators.CREATE_PASSKEY_TEXT_1, PasskeyLocators.CREATE_PASSKEY_TEXT_2])
        # Click different device
        self.controller.find_element(PasskeyLocators.DIFFERENT_DEVICE).click()

    def do_authentication_flow(self, pin: str = DEFAULT_KEY_PIN):
        """ Do the passkey authentication flow with the given pin. """
        # Wait for pin field and enter pin
        self.enter_pin(pin)

        # Wait for user presence to be requested and provide it
        self.controller.wait_for_element(PasskeyLocators.CONNECT_KEY)
        self.provide_user_presence()

    def do_discoverable_flow(self, username: str = DEFAULT_USERNAME, pin: str = DEFAULT_KEY_PIN):
        """ Do the flow for a discoverable credential on a security key """
        # Wait for the window
        self.controller.wait_for_element(PasskeyLocators.DISCOVERABLE_TITLE)

        # Scroll to the bottom, wait a bit between scrolls
        time.sleep(0.1)
        self.controller.swipe_percent(0.5, 0.8, 0.5, 0.2)
        time.sleep(0.1)
        self.controller.swipe_percent(0.5, 0.8, 0.5, 0.2)

        # Click the "Use passkey on another device" button
        self.controller.wait_for_element(PasskeyLocators.DISCOVERABLE_DIFFERENT_DEVICE).click()

        # Enter the pin of the passkey
        self.enter_pin(pin)

        # Wait for user presence request and provide user presence
        self.wait_for_user_presence_request()
        self.provide_user_presence()

        # Click the field for the discoverable credential
        self.click_discoverable(username)

    def wait_for_pin_field(self) -> WebElement:
        """ Wait for the pin input field for a hardware security key to appear, and return it """
        return self.controller.wait_for_element(PasskeyLocators.PIN_INPUT_FIELD_KEY)

    def enter_pin(self, pin: str = DEFAULT_KEY_PIN):
        """ Enter the pin in the pin input field for a security key """
        pin_field = self.wait_for_pin_field()
        pin_field.send_keys(pin)
        self.controller.find_element(PasskeyLocators.CONFIRM_BUTTON).click()

    def wait_for_user_presence_request(self):
        """ Wait for the user presence to be requested """
        self.controller.wait_for_element(PasskeyLocators.CONNECT_KEY)

    def wait_for_pin_error_text(self):
        """ Wait for the error text to appear for a security key prompt and return it. """
        element = self.controller.wait_for_element(PasskeyLocators.PIN_ERROR_TEXT_KEY)
        return element.text

    def click_discoverable(self, user: str = DEFAULT_USERNAME):
        """ Click a discoverable credential, by username. """
        locator = Locator.by_text(Context.NATIVE, user)
        element = self.controller.wait_for_element(locator)
        element.click()

    def cancel_pin_input(self):
        """ Cancel the pin input prompt. """
        self.controller.find_element(PasskeyLocators.CANCEL_BUTTON).click()

    def provide_user_presence(self, wait_before=1):
        """ Provide user presence to the device, wait a bit before pressing the button. """
        # Wait a bit to make sure the device is ready to receive user presence
        time.sleep(wait_before)

        # Now use the relay (press the button on FX7).
        print("Relay: user presence button.")
        self.relay_board.switch_relay(1, 200)

    def wait_for_user_presence_timeout(self, wait_time=24):
        """ Wait for user presence to be requested and the required amount of time to trigger a timeout """
        self.wait_for_user_presence_request()
        time.sleep(wait_time)
