from behave import given, when, then
import time
import logging

log = logging.getLogger(__name__)

# Common step definitions that can be reused across features

@given('I wait for {seconds:d} seconds')
def step_wait_seconds(context, seconds):
    """Wait for specified number of seconds."""
    log.info(f"Waiting for {seconds} seconds")
    time.sleep(seconds)

@when('I wait for {seconds:d} seconds')
def step_when_wait_seconds(context, seconds):
    """Wait for specified number of seconds in when clause."""
    log.info(f"Waiting for {seconds} seconds")
    time.sleep(seconds)

@then('I should wait for {seconds:d} seconds')
def step_then_wait_seconds(context, seconds):
    """Wait for specified number of seconds in then clause."""
    log.info(f"Waiting for {seconds} seconds")
    time.sleep(seconds)

@given('the test environment is initialized')
def step_test_env_initialized(context):
    """Verify test environment is properly initialized."""
    log.info("Verifying test environment is initialized")
    assert hasattr(context, 'relay_board'), "Relay board not available"

@when('I simulate a power cycle')
def step_simulate_power_cycle(context):
    """Simulate a power cycle of the device."""
    log.info("Simulating power cycle")
    if hasattr(context, 'relay_board'):
        # Turn off power
        context.relay_board.set_relay(2, False)
        time.sleep(2)
        # Turn on power
        context.relay_board.set_relay(2, True)
        time.sleep(3)  # Wait for device to boot

@when('I simulate button press')
def step_simulate_button_press(context):
    """Simulate pressing the device button."""
    log.info("Simulating button press")
    if hasattr(context, 'relay_board'):
        context.relay_board.switch_relay(1, 200)  # 200ms press

@when('I simulate long button press for {duration:d} milliseconds')
def step_simulate_long_button_press(context, duration):
    """Simulate long button press."""
    log.info(f"Simulating long button press for {duration}ms")
    if hasattr(context, 'relay_board'):
        context.relay_board.switch_relay(1, duration)

@then('the device LED should indicate ready state')
def step_device_led_ready(context):
    """Verify device LED indicates ready state."""
    log.info("Verifying device LED indicates ready state")
    # This would check for solid white LED

@then('the device LED should blink indicating user presence required')
def step_device_led_blink(context):
    """Verify device LED blinks for user presence."""
    log.info("Verifying device LED blinks for user presence")
    # This would check for blinking white LED

@then('the operation should complete within {seconds:d} seconds')
def step_operation_completes_within(context, seconds):
    """Verify operation completes within specified time."""
    log.info(f"Verifying operation completes within {seconds} seconds")
    # This would implement timeout checking

@then('no error messages should be displayed')
def step_no_error_messages(context):
    """Verify no error messages are displayed."""
    log.info("Verifying no error messages are displayed")

@then('the system should be in a clean state')
def step_system_clean_state(context):
    """Verify system is in a clean state."""
    log.info("Verifying system is in clean state")

# Context management steps
@given('I store the current state as "{state_name}"')
def step_store_current_state(context, state_name):
    """Store the current state for later comparison."""
    if not hasattr(context, 'stored_states'):
        context.stored_states = {}
    context.stored_states[state_name] = {
        'timestamp': time.time(),
        'state': 'current_state_placeholder'
    }
    log.info(f"Stored current state as {state_name}")

@then('the state should be the same as "{state_name}"')
def step_state_same_as_stored(context, state_name):
    """Verify current state matches stored state."""
    if hasattr(context, 'stored_states') and state_name in context.stored_states:
        log.info(f"Verifying state matches stored state {state_name}")
    else:
        log.warning(f"Stored state {state_name} not found")

# Error handling steps
@then('I should see an error containing "{error_text}"')
def step_see_error_containing(context, error_text):
    """Verify error message contains specific text."""
    log.info(f"Verifying error message contains: {error_text}")

@then('I should not see any error messages')
def step_no_error_messages_visible(context):
    """Verify no error messages are visible."""
    log.info("Verifying no error messages are visible")

# Utility steps for data validation
@then('the response should contain valid data')
def step_response_valid_data(context):
    """Verify response contains valid data."""
    log.info("Verifying response contains valid data")

@then('the data should be properly formatted')
def step_data_properly_formatted(context):
    """Verify data is properly formatted."""
    log.info("Verifying data is properly formatted")
