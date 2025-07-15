Feature: DIGIPASS FX7 Browser Autofill with Valid PIN
  As a user with a DIGIPASS FX7 device with PIN already set
  I want to authenticate using browser autofill feature with valid PIN
  So that I can select from multiple registered usernames on webauthn.io

  Background:
    Given I have a DIGIPASS FX7 device connected via USB
    And the device has a PIN set to "1234"
    And I have multiple registrations on webauthn.io with the security key
    And I am on the WebAuthn authentication page at "https://webauthn.io/"

  @hardware @authentication @autofill @pin_set @valid_pin @discoverable
  Scenario: Successful browser autofill authentication with valid PIN
    # Step 1: Leave username empty + Click Authenticate -> Sign in prompt appears
    Given I leave the username textbox empty
    When I click the authenticate button
    Then I should see a prompt to choose how I'd like to sign in to webauthn.io
    # Step 2: Select Use a passkey on different device -> Device selection options shown
    When I select "Use a passkey on different device"
    Then I should see the device selection options:
      | Option          |
      | USB             |
      | Different device|
    # Step 3: Connect security key -> LED blinks once (battery) + PIN dialog opens
    When I connect the security key under test
    Then the device LED should blink once indicating battery level
    And I should see the "Confirm with PIN" dialog
    # Step 4: Enter correct PIN -> LED blinks blue + Connect key dialog opens
    When I enter the correct PIN "1234" and confirm
    Then the device LED should blink blue
    And I should see the "Connect your key" dialog for user presence
    # Step 5: Press device button -> LED stops blinking + Username list appears
    When I press the button on the device
    Then the device LED should stop blinking
    And I should see a list of registered usernames
    # Step 6: Select any username -> Authentication successful
    When I select any username from the list
    Then the authentication should succeed
    And I should be logged in

  @hardware @authentication @autofill @pin_set @valid_pin @detailed_flow
  Scenario: Browser autofill with valid PIN - detailed hardware interaction
    Given I leave the username textbox empty
    When I click the authenticate button
    And I wait for hardware authenticator popup
    And I complete the hardware authentication flow
    Then I should see a list of registered usernames
    When I select any username from the list
    Then the authentication should succeed
    And I should be logged in

  @hardware @authentication @autofill @pin_set @valid_pin @multiple_credentials
  Scenario: Verify multiple credential selection in autofill
    Given I leave the username textbox empty
    When I click the authenticate button
    And I complete the hardware authentication flow
    Then I should see a list of registered usernames
    And the list should contain multiple usernames
    When I select the first username from the list
    Then the authentication should succeed
    When I logout and return to the authentication page
    And I leave the username textbox empty
    And I click the authenticate button
    And I complete the hardware authentication flow
    And I select the second username from the list
    Then the authentication should succeed
    And I should be logged in
