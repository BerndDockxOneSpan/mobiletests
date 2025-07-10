import time

from appium import webdriver
from appium.webdriver import WebElement
from selenium.common import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from shared.locator import Locator, Context


# Note: when using a slow device or slow emulator this might need to be increased
WAIT_TIMEOUT = 10


class DriverController:
    """ Wrapper for the Appium driver that provides some utility methods """

    def __init__(self, driver: webdriver.Remote):
        self.driver = driver
        self._current_context = Context.from_driver(self.driver)
        self._device_size: dict[str, int] | None = None

    @property
    def device_size(self) -> dict[str, int]:
        """ Get the size of the device's screen """
        if self._device_size is None:
            self._device_size = self.driver.get_window_size()
        return self._device_size

    @property
    def device_width(self) -> int:
        """ Get the width of the device's screen """
        return self.device_size["width"]

    @property
    def device_height(self) -> int:
        """ Get the height of the device's screen """
        return self.device_size["height"]

    def switch_context(self, context: Context, force: bool = False) -> None:
        """
        Switches the context of the Appium driver.
        If the desired context is the same as the current context, no command will be executed, unless force is True.

        :param context: The context to switch to.
        :param force: Send the switch command even if the current context is the same as the desired context.
        """
        if self._current_context == context and not force:
            return
        self.driver.switch_to.context(context.value)
        self._current_context = context

    def find_element(self, locator: Locator) -> WebElement:
        """ Find an element based on a locator """
        self.switch_context(locator.context)
        return self.driver.find_element(locator.by, locator.value)

    def find_element_or_none(self, locator: Locator) -> WebElement | None:
        """ Find an element based on a locator, or return None if it doesn't exist. """
        # Not really a fan of this way of doing it, but there doesn't seem to be another way
        try:
            return self.find_element(locator)
        except NoSuchElementException:
            return None

    def find_elements(self, locator: Locator) -> list[WebElement]:
        """ Find all elements that match a locator """
        self.switch_context(locator.context)
        return self.driver.find_elements(locator.by, locator.value)

    def wait_for(self, condition: expected_conditions, timeout: int = WAIT_TIMEOUT):
        """
        Wait for a condition to be met, with a maximum timeout

        :param condition: A condition from expected_conditions
        :param timeout: The timeout
        :return: What the condition returns
        """
        return WebDriverWait(self.driver, timeout).until(condition)

    def wait_for_element(self, locator: Locator, timeout: int = WAIT_TIMEOUT) -> WebElement:
        """ Wait for an element based on a locator with a timeout """
        self.switch_context(locator.context)
        return self.wait_for(expected_conditions.presence_of_element_located((locator.by, locator.value)), timeout)

    def wait_for_element_or_none(self, locator: Locator, timeout: int = WAIT_TIMEOUT) -> WebElement | None:
        """ Wait for an element based on a locator, or return None if it doesn't exist. """
        try:
            return self.wait_for_element(locator, timeout)
        except NoSuchElementException:
            return None

    def wait_for_first_element(self, locators: list[Locator], timeout: int = WAIT_TIMEOUT, time_between_tries: float = 0.5) -> WebElement:
        """ Wait for the first element to be located from a list of locators """
        start_time = time.time()
        while time.time() - start_time < timeout:
            for locator in locators:
                element = self.find_element_or_none(locator)
                if element is not None:
                    return element
            time.sleep(time_between_tries)

        raise TimeoutError('Timed out waiting for first element to be located.')

    def open_url(self, url: str) -> None:
        """ Open a web page, blocks until the page is fully loaded """
        self.driver.get(url)

    def press_key(self, key: int):
        """ Press a key on the device, use AndroidKey to find the key codes """
        self.driver.press_keycode(key)

    def swipe_percent(self, start_x: float, start_y: float, end_x: float, end_y: float, duration: int = 0):
        """
        Swipe using a percentage relative to the screen size, so (0.5, 0.5) would be the center of the screen.

        :param start_x: The x percentage of the start of the swipe.
        :param start_y: The y percentage of the start of the swipe.
        :param end_x: The x percentage of the end of the swipe.
        :param end_y: The y percentage of the end of the swipe.
        :param duration: The duration of the swipe, in milliseconds.
        """
        start_x_absolute = int(start_x * self.device_width)
        start_y_absolute = int(start_y * self.device_height)
        end_x_absolute = int(end_x * self.device_width)
        end_y_absolute = int(end_y * self.device_height)
        self.driver.swipe(start_x_absolute, start_y_absolute, end_x_absolute, end_y_absolute, duration)

    def press_back_button(self):
        """ Press the Android back button """
        self.switch_context(Context.NATIVE)
        self.driver.back()
