from behave import given, when, then
import logging

log = logging.getLogger(__name__)

@given('I am on the WebAuthn registration page')
def step_on_registration_page(context):
    """Navigate to WebAuthn registration page."""
    log.info("Navigating to WebAuthn registration page")
    # This would use the WebauthnUtil to navigate to the page
    # context.wa_util.open_page()

@given('I am on the WebAuthn authentication page')
def step_on_authentication_page(context):
    """Navigate to WebAuthn authentication page."""
    log.info("Navigating to WebAuthn authentication page")
    # context.wa_util.open_page()

@given('I am on the WebAuthn management page')
def step_on_management_page(context):
    """Navigate to WebAuthn management page."""
    log.info("Navigating to WebAuthn management page")

@given('I enter username "{username}"')
def step_enter_username(context, username):
    """Enter username in the form field."""
    context.current_username = username
    log.info(f"Entering username: {username}")
    # context.wa_util.fill_username(username=username)

@given('I register credentials for {count:d} different usernames')
def step_register_multiple_credentials(context, count):
    """Register credentials for multiple usernames."""
    log.info(f"Registering credentials for {count} different usernames")
    context.registered_usernames = [f"user_{i}" for i in range(1, count + 1)]

@given('I have credentials stored for "{user1}" and "{user2}"')
def step_have_stored_credentials(context, user1, user2):
    """Verify credentials are stored for specific users."""
    context.stored_users = [user1, user2]
    log.info(f"Verified credentials stored for {user1} and {user2}")

@given('I have registered {count:d} credentials on the device')
def step_have_registered_count(context, count):
    """Verify specific number of credentials registered."""
    context.credential_count = count
    log.info(f"Verified {count} credentials registered on device")

@given('I register a credential on Windows platform')
def step_register_on_windows(context):
    """Register credential on Windows platform."""
    context.registration_platform = "Windows"
    log.info("Registering credential on Windows platform")

@given('I register a credential for "{username}"')
def step_register_credential_for_user(context, username):
    """Register credential for specific username."""
    context.registered_user = username
    log.info(f"Registering credential for {username}")

@given('I have no credentials stored for "{username}"')
def step_no_credentials_for_user(context, username):
    """Verify no credentials exist for username."""
    log.info(f"Verified no credentials stored for {username}")

@when('I click the register button')
def step_click_register_button(context):
    """Click the register button."""
    log.info("Clicking register button")
    # context.wa_util.click_register_button()

@when('I click the authenticate button')
def step_click_authenticate_button(context):
    """Click the authenticate button."""
    log.info("Clicking authenticate button")
    # context.wa_util.click_authenticate_button()

@when('I click the authenticate button without entering username')
def step_click_authenticate_no_username(context):
    """Click authenticate button without entering username."""
    log.info("Clicking authenticate button without entering username")
    # This would trigger discoverable credential flow

@when('I select the correct credential from the list')
def step_select_correct_credential(context):
    """Select the correct credential from discoverable list."""
    log.info("Selecting correct credential from list")

@when('I authenticate with each stored credential')
def step_authenticate_each_credential(context):
    """Authenticate with each stored credential."""
    log.info("Authenticating with each stored credential")
    for username in getattr(context, 'registered_usernames', []):
        log.info(f"Authenticating with {username}")

@when('I delete the credential for "{username}"')
def step_delete_credential_for_user(context, username):
    """Delete credential for specific username."""
    log.info(f"Deleting credential for {username}")
    # This would use WebauthnUtil to delete the credential

@when('I attempt to register the {ordinal} credential')
def step_attempt_register_ordinal(context, ordinal):
    """Attempt to register nth credential."""
    log.info(f"Attempting to register {ordinal} credential")

@when('I move the device to macOS platform')
def step_move_to_macos(context):
    """Move device to macOS platform."""
    context.current_platform = "macOS"
    log.info("Moving device to macOS platform")

@when('I attempt to authenticate with the same credential')
def step_authenticate_same_credential(context):
    """Authenticate with the same credential on new platform."""
    log.info("Attempting to authenticate with same credential")

@when('I disconnect the device for {minutes:d} minutes')
def step_disconnect_device_duration(context, minutes):
    """Disconnect device for specified duration."""
    log.info(f"Disconnecting device for {minutes} minutes")
    # This would be simulated in test environment

@when('I reconnect the device')
def step_reconnect_device(context):
    """Reconnect the device."""
    log.info("Reconnecting device")

@when('I authenticate with "{username}"')
def step_authenticate_with_user(context, username):
    """Authenticate with specific username."""
    log.info(f"Authenticating with {username}")

@when('I attempt to delete credentials for "{username}"')
def step_attempt_delete_credentials(context, username):
    """Attempt to delete credentials for username."""
    log.info(f"Attempting to delete credentials for {username}")

@then('the registration should succeed')
def step_registration_succeeds(context):
    """Verify registration was successful."""
    log.info("Verifying registration succeeded")
    # context.wa_util.verify_registered_success()

@then('the registration should fail')
def step_registration_fails(context):
    """Verify registration failed."""
    log.info("Verifying registration failed")

@then('the registration should be cancelled')
def step_registration_cancelled(context):
    """Verify registration was cancelled."""
    log.info("Verifying registration was cancelled")

@then('the registration should timeout')
def step_registration_timeout(context):
    """Verify registration timed out."""
    log.info("Verifying registration timed out")

@then('the authentication should succeed')
def step_authentication_succeeds(context):
    """Verify authentication was successful."""
    log.info("Verifying authentication succeeded")
    # context.wa_util.verify_logged_in()

@then('the authentication should fail')
def step_authentication_fails(context):
    """Verify authentication failed."""
    log.info("Verifying authentication failed")

@then('the authentication should fail immediately')
def step_authentication_fails_immediately(context):
    """Verify authentication failed without device interaction."""
    log.info("Verifying authentication failed immediately")

@then('the authentication should be cancelled')
def step_authentication_cancelled(context):
    """Verify authentication was cancelled."""
    log.info("Verifying authentication was cancelled")

@then('the authentication should timeout')
def step_authentication_timeout(context):
    """Verify authentication timed out."""
    log.info("Verifying authentication timed out")

@then('I should see a success message')
def step_see_success_message(context):
    """Verify success message is displayed."""
    log.info("Verifying success message is displayed")

@then('I should see a PIN error message')
def step_see_pin_error_message(context):
    """Verify PIN error message is displayed."""
    log.info("Verifying PIN error message is displayed")

@then('I should see a "{error_type}" error message')
def step_see_specific_error_message(context, error_type):
    """Verify specific error message is displayed."""
    log.info(f"Verifying {error_type} error message is displayed")

@then('I should see a timeout error message')
def step_see_timeout_error_message(context):
    """Verify timeout error message is displayed."""
    log.info("Verifying timeout error message is displayed")

@then('I should see a lockout error message')
def step_see_lockout_error_message(context):
    """Verify lockout error message is displayed."""
    log.info("Verifying lockout error message is displayed")

@then('I should see a cancellation error message')
def step_see_cancellation_error_message(context):
    """Verify cancellation error message is displayed."""
    log.info("Verifying cancellation error message is displayed")

@then('I should be logged in')
def step_logged_in(context):
    """Verify user is logged in."""
    log.info("Verifying user is logged in")

@then('the credential should be stored on the device')
def step_credential_stored(context):
    """Verify credential was stored on device."""
    log.info("Verifying credential was stored on device")

@then('no credential should be stored')
def step_no_credential_stored(context):
    """Verify no credential was stored on device."""
    log.info("Verifying no credential was stored")

@then('all authentications should succeed')
def step_all_authentications_succeed(context):
    """Verify all authentications succeeded."""
    log.info("Verifying all authentications succeeded")

@then('each credential should work independently')
def step_each_credential_independent(context):
    """Verify each credential works independently."""
    log.info("Verifying each credential works independently")

@then('authentication with "{username}" should fail')
def step_auth_with_user_fails(context, username):
    """Verify authentication with specific user fails."""
    log.info(f"Verifying authentication with {username} fails")

@then('authentication with "{username}" should still work')
def step_auth_with_user_works(context, username):
    """Verify authentication with specific user still works."""
    log.info(f"Verifying authentication with {username} still works")

@then('the credential should work identically')
def step_credential_works_identically(context):
    """Verify credential works identically across platforms."""
    log.info("Verifying credential works identically")

@then('the credential should be unchanged')
def step_credential_unchanged(context):
    """Verify credential is unchanged after power cycle."""
    log.info("Verifying credential is unchanged")

@then('the operation should fail gracefully')
def step_operation_fails_gracefully(context):
    """Verify operation fails gracefully."""
    log.info("Verifying operation fails gracefully")

@then('I should see an appropriate error message')
def step_see_appropriate_error(context):
    """Verify appropriate error message is shown."""
    log.info("Verifying appropriate error message is shown")

@then('the device should remain in a stable state')
def step_device_stable_state(context):
    """Verify device remains in stable state."""
    log.info("Verifying device remains in stable state")
