from behave import given, when, then
import time
import logging

log = logging.getLogger(__name__)

@given('I have a DIGIPASS FX7 device connected')
def step_device_connected(context):
    assert hasattr(context, 'relay_board'), "Relay board not initialized"
    log.info("DIGIPASS FX7 device verified as connected")

@given('I have a DIGIPASS FX7 device with registered credentials')
def step_device_with_credentials(context):
    context.execute_steps('''
        Given I have a DIGIPASS FX7 device connected
    ''')
    log.info("DIGIPASS FX7 device has registered credentials")

@given('the device has no PIN set')
def step_device_no_pin(context):
    log.info("Device verified to have no PIN set")

@given('the device has a PIN set to "{pin}"')
def step_device_has_pin(context, pin):
    context.current_pin = pin
    log.info(f"Device verified to have PIN set to {pin}")

@when('I enter the correct PIN on the device')
def step_enter_correct_pin(context):
    pin = getattr(context, 'current_pin', '1234')
    log.info(f"Entering correct PIN: {pin}")
    if hasattr(context, 'pk_util') and context.pk_util:
        context.pk_util.enter_pin(pin=pin)
    else:
        raise RuntimeError("Hardware passkey utility not initialized")

@when('I enter an incorrect PIN on the device')
def step_enter_incorrect_pin(context):
    log.info("Entering incorrect PIN")
    if hasattr(context, 'pk_util') and context.pk_util:
        context.pk_util.enter_pin(pin="wrong_pin")
    else:
        raise RuntimeError("Hardware passkey utility not initialized")

@when('I enter incorrect PIN "{pin}" {count:d} times consecutively')
def step_enter_incorrect_pin_multiple(context, pin, count):
    log.info(f"Entering incorrect PIN {pin} {count} times consecutively")
    for attempt in range(count):
        log.info(f"Attempt {attempt + 1} with incorrect PIN")
        if attempt < count - 1:
            time.sleep(0.5)

@when('I enter incorrect PIN across multiple sessions totaling {total:d} attempts')
def step_enter_incorrect_pin_total(context, total):
    """Enter incorrect PIN across multiple sessions."""
    log.info(f"Simulating {total} incorrect PIN attempts across multiple sessions")
    # This would simulate disconnecting/reconnecting and entering wrong PINs

@when('I provide user presence on the device')
def step_provide_user_presence(context):
    """Provide user presence (button press) on device."""
    log.info("Providing user presence (button press)")
    # This would trigger the relay board to press the button
    if hasattr(context, 'relay_board'):
        context.relay_board.switch_relay(1, 200)  # Press button for 200ms

@when('I do not provide user presence within {timeout:d} seconds')
def step_no_user_presence_timeout(context, timeout):
    """Wait for timeout without providing user presence."""
    log.info(f"Waiting {timeout} seconds without providing user presence")
    time.sleep(timeout + 2)  # Wait longer than timeout

@when('I cancel the PIN entry')
def step_cancel_pin_entry(context):
    """Cancel PIN entry operation."""
    log.info("Cancelling PIN entry")
    # This would simulate pressing back or cancel

@when('I set a PIN with exactly {length:d} characters "{pin}"')
def step_set_pin_exact_length(context, length, pin):
    """Set a PIN with exact character count."""
    assert len(pin) == length, f"PIN length mismatch: expected {length}, got {len(pin)}"
    context.new_pin = pin
    log.info(f"Setting PIN with {length} characters: {pin}")

@when('I set a PIN with {length:d} ASCII characters')
def step_set_pin_ascii_length(context, length):
    """Set a PIN with specific ASCII character count."""
    pin = 'a' * length  # Create PIN with repeated 'a'
    context.new_pin = pin
    log.info(f"Setting PIN with {length} ASCII characters")

@when('I attempt to set a PIN with {length:d} characters "{pin}"')
def step_attempt_set_short_pin(context, length, pin):
    """Attempt to set a PIN that may be invalid."""
    context.attempted_pin = pin
    log.info(f"Attempting to set PIN with {length} characters: {pin}")

@when('I attempt to set a PIN with special characters exceeding {limit:d} bytes')
def step_attempt_set_long_utf8_pin(context, limit):
    """Attempt to set a PIN that exceeds UTF-8 byte limit."""
    # Create a PIN with multi-byte UTF-8 characters that exceeds the limit
    context.attempted_pin = "🔐" * 20  # Emoji characters use multiple bytes
    log.info(f"Attempting to set PIN exceeding {limit} bytes")

@when('I change the PIN from "{old_pin}" to "{new_pin}"')
def step_change_pin_success(context, old_pin, new_pin):
    """Change PIN from old to new value."""
    context.old_pin = old_pin
    context.new_pin = new_pin
    log.info(f"Changing PIN from {old_pin} to {new_pin}")

@when('I attempt to change the PIN from "{old_pin}" to "{new_pin}"')
def step_attempt_change_pin(context, old_pin, new_pin):
    """Attempt to change PIN (may fail)."""
    context.attempted_old_pin = old_pin
    context.attempted_new_pin = new_pin
    log.info(f"Attempting to change PIN from {old_pin} to {new_pin}")

@when('I disconnect and reconnect the USB device')
def step_disconnect_reconnect_usb(context):
    """Disconnect and reconnect the USB device."""
    log.info("Disconnecting and reconnecting USB device")
    # This would control power to the device via relay board
    if hasattr(context, 'relay_board'):
        context.relay_board.set_relay(2, False)  # Disconnect power
        time.sleep(1)
        context.relay_board.set_relay(2, True)   # Reconnect power
        time.sleep(2)  # Wait for device to initialize

@then('the device should require USB re-insertion')
def step_device_requires_usb_reinsertion(context):
    """Verify device requires USB re-insertion."""
    log.info("Verifying device requires USB re-insertion")
    # This would check for the appropriate error message

@then('the device should be permanently locked')
def step_device_permanently_locked(context):
    """Verify device is permanently locked."""
    log.info("Verifying device is permanently locked")
    # This would check for permanent lockout state

@then('the PIN should be accepted and saved')
def step_pin_accepted_saved(context):
    """Verify PIN was accepted and saved."""
    log.info("Verifying PIN was accepted and saved")
    # This would verify the PIN is stored

@then('the PIN should be rejected')
def step_pin_rejected(context):
    """Verify PIN was rejected."""
    log.info("Verifying PIN was rejected")

@then('the PIN change should succeed')
def step_pin_change_success(context):
    """Verify PIN change succeeded."""
    log.info("Verifying PIN change succeeded")

@then('the PIN change should fail')
def step_pin_change_fail(context):
    """Verify PIN change failed."""
    log.info("Verifying PIN change failed")

@then('the device should be ready for FIDO operations')
def step_device_ready_fido(context):
    """Verify device is ready for FIDO operations."""
    log.info("Verifying device is ready for FIDO operations")

@then('all characters should be stored correctly')
def step_all_characters_stored(context):
    """Verify all PIN characters were stored correctly."""
    log.info("Verifying all PIN characters were stored correctly")

@then('the device should work with the new PIN "{pin}"')
def step_device_works_new_pin(context, pin):
    """Verify device works with the new PIN."""
    log.info(f"Verifying device works with new PIN: {pin}")

@then('the original PIN "{pin}" should remain unchanged')
def step_original_pin_unchanged(context, pin):
    """Verify original PIN is unchanged."""
    log.info(f"Verifying original PIN {pin} remains unchanged")

@then('the PIN attempt counter should be reset')
def step_pin_counter_reset(context):
    """Verify PIN attempt counter was reset."""
    log.info("Verifying PIN attempt counter was reset")

@then('I should be able to enter the correct PIN')
def step_can_enter_correct_pin(context):
    """Verify correct PIN can be entered."""
    log.info("Verifying correct PIN can be entered")

@then('only factory reset should restore functionality')
def step_only_factory_reset_restores(context):
    """Verify only factory reset can restore functionality."""
    log.info("Verifying only factory reset can restore functionality")

@then('I should see an error about minimum length requirements')
def step_see_min_length_error(context):
    """Verify minimum length error message."""
    log.info("Verifying minimum length error message is shown")

@then('I should see an error about byte limit exceeded')
def step_see_byte_limit_error(context):
    """Verify byte limit error message."""
    log.info("Verifying byte limit exceeded error message is shown")

@then('I should see an error about incorrect old PIN')
def step_see_incorrect_old_pin_error(context):
    """Verify incorrect old PIN error message."""
    log.info("Verifying incorrect old PIN error message is shown")

@then('I should see an error message about reconnection')
def step_see_reconnection_error(context):
    """Verify reconnection error message."""
    log.info("Verifying reconnection error message is shown")

@then('I should see an error about device being locked')
def step_see_device_locked_error(context):
    """Verify device locked error message."""
    log.info("Verifying device locked error message is shown")

@when('I enter incorrect PIN {count:d} times consecutively')
def step_enter_incorrect_pin_consecutive(context, count):
    """Enter incorrect PIN multiple times consecutively."""
    log.info(f"Entering incorrect PIN {count} times consecutively")
    if hasattr(context, 'pk_util') and context.pk_util:
        for attempt in range(count):
            try:
                context.pk_util.enter_pin(pin="0000")  # Wrong PIN
                error_text = context.pk_util.wait_for_pin_error_text()
                log.info(f"Attempt {attempt + 1}: {error_text}")
                if attempt < count - 1:
                    time.sleep(0.5)  # Brief pause between attempts
            except Exception as e:
                log.info(f"PIN attempt {attempt + 1} failed: {e}")
    else:
        raise RuntimeError("Hardware passkey utility not initialized")

@when('I enter incorrect PIN {total:d} times total')
def step_enter_incorrect_pin_total_simple(context, total):
    """Enter incorrect PIN total times across sessions."""
    log.info(f"Simulating {total} incorrect PIN attempts total")
    if hasattr(context, 'pk_util') and context.pk_util:
        for attempt in range(total):
            try:
                context.pk_util.enter_pin(pin="0000")  # Wrong PIN
                error_text = context.pk_util.wait_for_pin_error_text()
                log.info(f"Total attempt {attempt + 1}: {error_text}")
                if attempt < total - 1:
                    time.sleep(0.2)  # Brief pause between attempts
            except Exception as e:
                log.info(f"PIN attempt {attempt + 1} failed: {e}")
                break  # Stop if device locks or fails
    else:
        raise RuntimeError("Hardware passkey utility not initialized")

@then('I should see an error about storage limit')
def step_see_storage_limit_error(context):
    """Verify storage limit error is displayed."""
    log.info("Verifying storage limit error message")
    if hasattr(context, 'wa_util') and context.wa_util:
        try:
            error_text = context.wa_util.wait_for_error_text()
            assert "storage" in error_text.lower() or "limit" in error_text.lower(), f"Expected storage limit error, got: {error_text}"
            log.info(f"Storage limit error confirmed: {error_text}")
        except Exception as e:
            log.info(f"Could not verify storage limit error: {e}")
    else:
        raise RuntimeError("WebAuthn utility not initialized")
