import os

import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from pytest import StashKey, CollectReport

import RelayBoard
from shared.appium_util import DriverController
from shared.passkey_util import HardwarePasskeyUtil, LocalPasskeyUtil
from webauthn.webauthn_util import WebauthnUtil

base_capabilities = dict(
    platformName='Android',
    automationName='uiautomator2',
    deviceName='Android',
    # Even in a web context, we want to see the full device, not only the website
    nativeWebScreenshot=True,
)
browser_capabilities = dict(
    browserName='Chrome',
)

appium_server_url = 'http://localhost:4723'


@pytest.fixture(scope='function')
def driver(request):
    """ Create a driver to interact with the Android device """
    capabilities = base_capabilities.copy()
    # If a test is marked with @pytest.mark.browser, we will add the browser capabilities to the requested capabilities
    if request.node.get_closest_marker('browser'):
        capabilities |= browser_capabilities

    driver = webdriver.Remote(appium_server_url, options=UiAutomator2Options().load_capabilities(capabilities))
    yield driver
    driver.quit()


@pytest.fixture(scope='session')
def relay_board(request) -> RelayBoard:
    """ Connect to a relay board """
    board = RelayBoard.create_board()
    yield board
    board.close()


@pytest.fixture(scope='function')
def controller(request, driver) -> DriverController:
    """ Create a driver controller object """
    return DriverController(driver)


@pytest.fixture(scope='function')
def pk_util(request, controller, relay_board) -> HardwarePasskeyUtil:
    """ Create a HardwarePasskeyUtil object """
    return HardwarePasskeyUtil(controller, relay_board)


@pytest.fixture(scope='function')
def local_pk_util(request, controller) -> LocalPasskeyUtil:
    """ Create a LocalPasskeyUtil object """
    return LocalPasskeyUtil(controller)


@pytest.fixture(scope='function')
def wa_util(request, controller, relay_board) -> WebauthnUtil:
    """ Create a Webauthn Utility object and open the page """
    util = WebauthnUtil(controller)
    util.open_page()
    return util


# Key used to store the result of a test in the stash
phase_report_key = StashKey[dict[str, CollectReport]]()


# Hook that will store the result of a test, so we can access it in fixtures
@pytest.hookimpl(wrapper=True, tryfirst=True)
def pytest_runtest_makereport(item):
    # Execute other hooks to obtain the result
    report = yield

    # Store the result per phase
    item.stash.setdefault(phase_report_key, {})[report.when] = report

    return report


@pytest.fixture(scope='function', autouse=True)
def make_screenshot_on_fail(request, driver):
    """ Check if the test failed, and if so create a screenshot of the device """
    # Wait until the test is done
    yield

    report = request.node.stash[phase_report_key]
    if ("setup" in report and report["setup"].failed) or ("call" in report and report["call"].failed):
        # Test failed during setup or during the test itself, make a screenshot
        file_name = request.node.nodeid.replace("/", "_").replace(":", "_").replace(".py", "") + ".png"
        if not os.path.exists('fail_screenshots'):
            os.mkdir('fail_screenshots')
        driver.save_screenshot(f'fail_screenshots/{file_name}')
