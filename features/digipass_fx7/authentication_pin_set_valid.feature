Feature: DIGIPASS FX7 Authentication with Valid PIN
  As a user with a DIGIPASS FX7 device and PIN set
  I want to authenticate using my device with valid PIN
  So that I can securely access my account on webauthn.io

  Background:
    Given I have a DIGIPASS FX7 device connected via USB
    And the device has a PIN set to "1234"
    And I have registered credentials on webauthn.io with the security key
    And I am on the WebAuthn authentication page at "https://webauthn.io/"


  @hardware @authentication @username-entry
  Scenario: Username entry enables authentication
    # XML Step 1: Enter username -> Username is entered
    Given I enter username "registered_user"
    Then the username should be entered successfully


  @hardware @authentication @no-passkeys-dialog
  Scenario: Authentication shows no passkeys dialog for username
    # XML Step 2: Click Authenticate -> No passkeys available dialog opens
    Given I enter username "registered_user"
    When I click the authenticate button
    Then I should see the "No passkeys available" dialog


  @hardware @authentication @device-selection
  Scenario: User selects different device option
    # XML Step 3: Select Use different device -> Choose device options shown
    Given the "No passkeys available" dialog is shown
    When I select "Use different device"
    Then I should see the device selection options:
      | Option           |
      | NFC              |
      | USB              |
      | Different device |


  @hardware @authentication @usb-selection
  Scenario: USB selection shows connect dialog
    # XML Step 4: Select USB security key -> Connect your key dialog opens
    Given the device selection options are shown
    When I select "USB security key"
    Then I should see the "Connect your key" dialog


  @hardware @authentication @device-connection
  Scenario: Security key connection prompts for PIN
    # XML Step 5: Connect Security Key -> LED blinks + PIN dialog opens
    Given the "Connect your key" dialog is shown
    When I connect the security key
    Then the device LED should blink once indicating battery level
    And I should see the "Confirm with PIN" dialog


  @hardware @authentication @pin-validation
  Scenario: Valid PIN enables user presence request
    # XML Step 6: Provide correct PIN -> LED blinks blue + Connect key dialog
    Given the "Confirm with PIN" dialog is shown
    When I enter the correct PIN "1234" and confirm
    Then the device LED should blink blue
    And I should see the "Connect your key" dialog for user presence


  @hardware @authentication @user-presence
  Scenario: User presence completes authentication
    # XML Step 7: Press security key button -> Authentication successful
    Given the "Connect your key" dialog is shown for user presence
    When I press the security key button to provide user presence
    Then the authentication should succeed
    And I should be logged in


  @hardware @authentication @end-to-end
  Scenario: Complete authentication flow with valid PIN
    # Complete flow from XML test case 2612
    Given I enter username "registered_user"
    When I authenticate with hardware device using valid PIN
    Then I should be logged in successfully


  @hardware @authentication @cross-platform
  Scenario: Authentication persists after page refresh
    # Authentication state verification after refresh
    Given I have successfully authenticated with username "cross_platform_user"
    When I refresh the page
    Then I should remain authenticated
