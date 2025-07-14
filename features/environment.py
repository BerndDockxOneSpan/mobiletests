import logging
from shared.passkey_util import HardwarePasskeyUtil, LocalPasskeyUtil
from webauthn.webauthn_util import WebauthnUtil
from shared.appium_util import DriverController
from RelayBoard import create_board, BoardType

def before_all(context):
    """Setup test environment before all scenarios."""
    context.config.setup_logging()
    
    # Initialize relay board for hardware tests
    context.relay_board = create_board(BoardType.STUB)
    
def before_scenario(context, scenario):
    """Setup before each scenario."""
    # Initialize driver controller (this would normally come from pytest fixtures)
    # For BDD tests, we need to create it here
    # Note: This assumes you have a way to get the driver instance
    # context.driver_controller = DriverController(driver_instance)
    
    # Initialize utilities based on tags
    if 'hardware' in scenario.tags:
        # context.pk_util = HardwarePasskeyUtil(context.driver_controller, context.relay_board)
        pass  # Will be initialized when driver is available
    elif 'local' in scenario.tags:
        # context.local_pk_util = LocalPasskeyUtil(context.driver_controller)
        pass  # Will be initialized when driver is available
    
    # context.wa_util = WebauthnUtil(context.driver_controller)

def after_scenario(context, scenario):
    """Cleanup after each scenario."""
    if hasattr(context, 'pk_util'):
        # Cleanup hardware passkey util
        pass
    if hasattr(context, 'local_pk_util'):
        # Cleanup local passkey util
        pass
    if hasattr(context, 'wa_util'):
        # Cleanup webauthn util
        pass

def after_all(context):
    """Cleanup test environment after all scenarios."""
    if hasattr(context, 'relay_board'):
        context.relay_board.close()
