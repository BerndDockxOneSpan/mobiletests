import logging
from shared.passkey_util import HardwarePasskeyUtil, LocalPasskeyUtil
from webauthn.webauthn_util import WebauthnUtil
from shared.appium_util import DriverController
from RelayBoard import create_board, BoardType

log = logging.getLogger(__name__)

def before_all(context):
    """Setup test environment before all scenarios."""
    context.config.setup_logging()
    
    # Initialize relay board for hardware tests
    context.relay_board = create_board(BoardType.STUB)
    
def before_scenario(context, scenario):
    """Setup before each scenario."""
    # Check if this is just a test scenario that doesn't need hardware
    if 'test' in [tag.lower() for tag in scenario.tags]:
        # For test scenarios, create mock utilities
        context.driver = None
        context.driver_controller = None
        context.wa_util = None
        context.pk_util = None
        log.info("Test scenario - skipping hardware initialization")
        return
    
    # Initialize Appium driver for Android device
    from appium import webdriver
    from appium.options.android import UiAutomator2Options
    
    base_capabilities = {
        'platformName': 'Android',
        'automationName': 'uiautomator2',
        'deviceName': 'Android',
        'nativeWebScreenshot': True,
    }
    
    # Add browser capabilities if needed
    if 'browser' in [tag.lower() for tag in scenario.tags]:
        base_capabilities['browserName'] = 'Chrome'
    
    appium_server_url = 'http://localhost:4723'
    
    try:
        # Create Appium driver
        context.driver = webdriver.Remote(
            appium_server_url, 
            options=UiAutomator2Options().load_capabilities(base_capabilities)
        )
        
        # Initialize driver controller
        context.driver_controller = DriverController(context.driver)
        
        # Initialize utilities based on tags
        if 'hardware' in [tag.lower() for tag in scenario.tags]:
            context.pk_util = HardwarePasskeyUtil(context.driver_controller, context.relay_board)
        elif 'local' in [tag.lower() for tag in scenario.tags]:
            context.local_pk_util = LocalPasskeyUtil(context.driver_controller)
        
        # Always initialize WebAuthn utility and open page
        context.wa_util = WebauthnUtil(context.driver_controller)
        context.wa_util.open_page()
        
    except Exception as e:
        print(f"Failed to initialize test environment: {e}")
        print("Make sure Appium server is running: appium --port 4723")
        print("Make sure Android device is connected with USB debugging enabled")
        # Set context to None so tests can check if setup failed
        context.driver = None
        context.driver_controller = None
        context.wa_util = None
        raise RuntimeError(f"Environment setup failed: {e}")

def after_scenario(context, scenario):
    """Cleanup after each scenario."""
    # Cleanup utilities
    if hasattr(context, 'pk_util') and context.pk_util:
        # Cleanup hardware passkey util
        pass
    if hasattr(context, 'local_pk_util') and context.local_pk_util:
        # Cleanup local passkey util
        pass
    if hasattr(context, 'wa_util') and context.wa_util:
        # Cleanup webauthn util
        pass
    
    # Quit the driver
    if hasattr(context, 'driver') and context.driver:
        try:
            context.driver.quit()
        except Exception as e:
            print(f"Error closing driver: {e}")
        context.driver = None
        context.driver_controller = None

def after_all(context):
    """Cleanup test environment after all scenarios."""
    if hasattr(context, 'relay_board'):
        context.relay_board.close()
