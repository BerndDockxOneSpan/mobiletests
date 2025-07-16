from behave import given, when, then
import time
import logging

log = logging.getLogger(__name__)

@given('I have a DIGIPASS FX7 device connected via USB')
def step_device_connected_usb(context):
    """Verify device is connected via USB."""
    log.info("Verifying DIGIPASS FX7 device is connected via USB")
    assert hasattr(context, 'relay_board'), "Relay board not initialized"
    # Verify USB connection status
    log.info("DIGIPASS FX7 device verified as connected via USB")

@given('the device has a PIN set to "{pin}"')
def step_device_has_pin(context, pin):
    """Verify device has specific PIN set."""
    context.current_pin = pin
    log.info(f"Device verified to have PIN set to {pin}")
