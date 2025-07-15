
Feature: DIGIPASS FX7 Browser Autofill Authentication
  As a user with a DIGIPASS FX7 device and PIN set
  I want to authenticate using browser autofill
  So that I can access webauthn.io with discoverable credentials

  Background:
    Given I have a DIGIPASS FX7 device connected via USB
    And the device has a PIN set to "1234"
    And I have multiple registrations on webauthn.io with the security key
    And I am on the WebAuthn authentication page at "https://webauthn.io/"


  @hardware @authentication @autofill @discoverable
  Scenario: Browser shows authentication options for empty username
    # XML Step 1: Leave username empty + Click Authenticate -> Sign in prompt appears
    Given I leave the username textbox empty
    When I click the authenticate button
    Then I should see a prompt to choose how I'd like to sign in to webauthn.io


  @hardware @authentication @autofill @device-selection
  Scenario: User selects passkey device option
    # XML Step 2: Select Use a passkey on different device -> Device options shown
    Given I am prompted to choose how to sign in
    When I select "Use a passkey on different device"
    Then I should see the device selection options:
      | Option           |
      | USB              |
      | Different device |


  @hardware @authentication @autofill @pin-entry
  Scenario: Device prompts for PIN when connected
    # XML Step 3: Connect security key -> LED blinks + PIN dialog opens
    Given the device selection options are shown
    When I connect the security key under test
    Then the device LED should blink once indicating battery level
    And I should see the "Confirm with PIN" dialog


  @hardware @authentication @autofill @pin-validation
  Scenario: Valid PIN enables user presence request
    # XML Step 4: Enter correct PIN -> LED blinks blue + Connect key dialog
    Given the "Confirm with PIN" dialog is shown
    When I enter the correct PIN "1234" and confirm
    Then the device LED should blink blue
    And I should see the "Connect your key" dialog for user presence


  @hardware @authentication @autofill @user-presence
  Scenario: User presence reveals credential list
    # XML Step 5: Press button -> LED stops + Username list appears
    Given the "Connect your key" dialog is shown for user presence
    When I press the button on the device
    Then the device LED should stop blinking
    And I should see a list of registered usernames


  @hardware @authentication @autofill @credential-selection
  Scenario: Selecting username completes authentication
    # XML Step 6: Select username -> Authentication successful
    Given a list of registered usernames is shown
    When I select any username from the list
    Then the authentication should succeed
    And I should be logged in


  @hardware @authentication @autofill @end-to-end
  Scenario: Complete autofill authentication flow
    # Complete flow from XML test case 2613
    Given I leave the username textbox empty
    When I authenticate with discoverable credentials using valid PIN
    Then I should be logged in successfully
