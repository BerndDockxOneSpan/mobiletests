import enum

from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy


class Context(enum.Enum):
    NATIVE = "NATIVE_APP"
    WEB = "CHROMIUM"

    @staticmethod
    def from_driver(driver: webdriver.Remote) -> 'Context':
        driver_context = driver.current_context
        return Context(driver_context)


class Locator:
    """ Data class representing an element on a webpage or a native element """

    def __init__(self, context: Context, by: str, value: str):
        self.__context = context
        self.__by: str = by
        self.__value: str = value

    def __or__(self, other) -> 'Locator':
        """ Create a new locator that matches this locator, or the other locator, only implemented for XPath locators """

        if self.__by != AppiumBy.XPATH or other.__by != AppiumBy.XPATH:
            raise NotImplementedError("Or is only implemented for XPATH locators")
        if self.__context != other.__context:
            raise NotImplementedError("Or is only implemented when both locators have the same context")

        xpath = f'{self.__value} or {other.__value}'
        return Locator.by_xpath(self.__context, xpath)

    @property
    def context(self) -> Context:
        """ Get the context this locator will work in. """
        return self.__context

    @property
    def by(self) -> str:
        """ Get what this locator searches by. """
        return self.__by

    @property
    def value(self) -> str:
        """ Get the value of what this locator searches for. """
        return self.__value

    @staticmethod
    def by_xpath(context: Context, xpath: str) -> 'Locator':
        """ Create a locator from a xpath. """
        return Locator(context, AppiumBy.XPATH, xpath)

    @staticmethod
    def _escape_string(value: str) -> str:
        """ Escape a string so it can be used in a xpath or a ui automator expression without issues """
        return value.replace('\\', '\\\\').replace('"', '\\"')

    @staticmethod
    def by_attributes(context: Context, attributes: dict[str, str]) -> 'Locator':
        """ Create a locator from a dictionary of attributes. """
        # Create a xpath locator to find the attributes
        xpath = f"//*[{" and ".join([f'@{key}="{Locator._escape_string(value)}"' for key, value in attributes.items()])}]"
        return Locator.by_xpath(context, xpath)

    @staticmethod
    def by_text(context: Context, text: str) -> 'Locator':
        """ Create a locator that looks for an element by the text it has. """
        if context == Context.WEB:
            xpath = f'//*[text()="{Locator._escape_string(text)}"]'
            return Locator.by_xpath(context, xpath)
        elif context == Context.NATIVE:
            automator_str = f'new UiSelector().text("{Locator._escape_string(text)}")'
            return Locator.by_ui_automator(context, automator_str)
        else:
            raise NotImplementedError(f"'Locator.by_text' is not yet implemented for the context '{context}'.")

    @staticmethod
    def by_contains_text(context: Context, text: str) -> 'Locator':
        """ Create a locator to see find an element containing a certain text. """
        if context == Context.WEB:
            xpath = f'//*[contains(text(), "{Locator._escape_string(text)})"]'
            return Locator.by_xpath(context, xpath)
        elif context == Context.NATIVE:
            automator_str = f'new UiSelector().textContains("{Locator._escape_string(text)}")'
            return Locator.by_ui_automator(context, automator_str)
        else:
            raise NotImplementedError(f"'Locator.by_text' is not yet implemented for the context '{context}'.")

    @staticmethod
    def by_id(context: Context, id_value: str) -> 'Locator':
        """
        Create a locator by an id.

        Please note that this does not seem to work in a browser context,
        you can use Locator.by_attributes for that instead.
        """
        return Locator(context, AppiumBy.ID, id_value)

    @staticmethod
    def by_ui_automator(context: Context, value: str) -> 'Locator':
        """ Create a locator by an Android UiAutomator instruction. """
        return Locator(context, AppiumBy.ANDROID_UIAUTOMATOR, value)

    @staticmethod
    def by_link_text(context: Context, link_text: str):
        """ Search for an element containing a link by the text the link has. """
        return Locator(context, AppiumBy.LINK_TEXT, link_text)

    @staticmethod
    def by_button_text(context: Context, button_text: str) -> 'Locator':
        """ Search for a button with a specific text """
        # Remove leading and trailing whitespaces from both sides
        xpath = f'//button[normalize-space(text())="{Locator._escape_string(button_text.strip())}"]'
        return Locator.by_xpath(context, xpath)

    @staticmethod
    def by_button_index(context: Context, button_index: int) -> 'Locator':
        """
        Search for a button by the index it is on screen with, should only be used if a button doesn't have an id.
        """
        automator_str = f'new UiSelector().className("android.widget.Button").instance({button_index})'
        return Locator.by_ui_automator(context, automator_str)
