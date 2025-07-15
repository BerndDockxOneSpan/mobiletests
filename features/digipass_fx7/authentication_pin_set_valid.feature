Feature: DIGIPASS FX7 Authentication with Valid PIN
  As a user with a DIGIPASS FX7 device with PIN already set
  I want to authenticate using my device with valid PIN on Android
  So that I can securely access my account on webauthn.io

  Background:
    Given I have a DIGIPASS FX7 device connected via USB
    And the device has a PIN set to "1234"
    And I have registered credentials on webauthn.io with the security key
    And I am on the WebAuthn authentication page at "https://webauthn.io/"

  @hardware @authentication @pin_set @valid_pin @android
  Scenario: Successful authentication with valid PIN on Android
    # Step 1: Enter username
    Given I enter username "registered_user"
    # Step 2: Click Authenticate button -> No passkeys available dialog opens
    When I click the authenticate button
    Then I should see the "No passkeys available" dialog
    # Step 3: Select Use different device -> Choose device for passkey options shown
    When I select "Use different device"
    Then I should see the device selection options:
      | Option          |
      | NFC             |
      | USB             |
      | Different device|
    # Step 4: Select USB security key -> Connect your key dialog opens
    When I select "USB security key"
    Then I should see the "Connect your key" dialog
    # Step 5: Connect Security Key -> LED blinks once (battery) + PIN dialog opens
    When I connect the security key
    Then the device LED should blink once indicating battery level
    And I should see the "Confirm with PIN" dialog
    # Step 6: Provide correct PIN -> LED blinks blue + Connect key dialog opens
    When I enter the correct PIN "1234" and confirm
    Then the device LED should blink blue
    And I should see the "Connect your key" dialog for user presence
    # Step 7: Press security key button -> Authentication successful
    When I press the security key button to provide user presence
    Then the authentication should succeed
    And I should be logged in

  @hardware @authentication @pin_set @valid_pin @detailed_flow
  Scenario: Authentication with valid PIN - detailed hardware interaction
    Given I enter username "registered_user_detailed"
    When I click the authenticate button
    And I wait for hardware authenticator popup
    And I complete the hardware authentication flow
    Then the authentication should succeed
    And I should be logged in

  @hardware @authentication @pin_set @valid_pin @cross_platform
  Scenario: Verify authentication works across platforms
    Given I enter username "cross_platform_user"
    When I click the authenticate button
    And I complete the hardware authentication flow
    Then the authentication should succeed
    When I refresh the page
    And I enter username "cross_platform_user"
    And I click the authenticate button
    And I complete the hardware authentication flow
    Then the authentication should succeed
    And I should be logged in
