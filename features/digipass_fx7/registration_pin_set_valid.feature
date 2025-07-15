Feature: DIGIPASS FX7 Registration with Valid PIN
  As a user with a DIGIPASS FX7 device with PIN already set
  I want to register my device for WebAuthn using my valid PIN
  So that I can use it for secure authentication on webauthn.io

  Background:
    Given I have a DIGIPASS FX7 device connected via USB
    And the device has a PIN set to "1234"
    And the device is not yet registered
    And I am on the WebAuthn registration page at "https://webauthn.io/"

  @hardware @registration @pin_set @valid_pin @chrome
  Scenario: Successful registration with valid PIN on Chrome v135
    # Step 1: Enter username
    Given I enter username "test_user_reg_valid_pin"
    # Step 2: Click Register button -> Sign in options dialog opens
    When I click the register button
    Then I should see the sign in options dialog
    # Step 3: Select More options -> Choose device for passkey options shown
    When I select "More options"
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
    # Step 7: Press security key button -> Registration successful
    When I press the security key button to provide user presence
    Then the registration should succeed
    And I should see a success message
    And the credential should be stored on the device

  @hardware @registration @pin_set @valid_pin @detailed_flow
  Scenario: Registration with valid PIN - detailed hardware interaction
    Given I enter username "test_user_detailed"
    When I click the register button
    And I wait for hardware authenticator popup
    And I complete the hardware registration flow
    Then the registration should succeed
    And the credential should be stored on the device

  @hardware @registration @pin_set @valid_pin @verification
  Scenario: Verify registration persistence after valid PIN registration
    Given I enter username "test_user_persistence"
    When I click the register button
    And I complete the hardware registration flow
    Then the registration should succeed
    When I navigate to the authentication page
    And I enter username "test_user_persistence"
    And I click the authenticate button
    And I complete the hardware authentication flow
    Then the authentication should succeed
    And I should be logged in
