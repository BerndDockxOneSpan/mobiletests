Feature: DIGIPASS FX7 Registration
  As a user with a DIGIPASS FX7 device
  I want to register my device for WebAuthn
  So that I can use it for secure authentication

  Background:
    Given I have a DIGIPASS FX7 device connected
    And I am on the WebAuthn registration page

  @hardware @registration
  Scenario: Successful registration with valid PIN
    Given I enter username "test_user_001"
    When I click the register button
    And I enter the correct PIN on the device
    And I provide user presence on the device
    Then the registration should succeed
    And I should see a success message
    And the credential should be stored on the device

  @hardware @registration @error
  Scenario: Registration fails with wrong PIN
    Given I enter username "test_user_002"
    When I click the register button
    And I enter an incorrect PIN on the device
    Then the registration should fail
    And I should see a PIN error message
    And no credential should be stored

  @hardware @registration @pin_lockout
  Scenario: Device locks after maximum PIN attempts
    Given I enter username "test_user_003"
    When I click the register button
    And I enter incorrect PIN 3 times consecutively
    Then the device should require USB re-insertion
    When I enter incorrect PIN 8 times total
    Then the device should be permanently locked
    And I should see a lockout error message

  @hardware @registration @timeout
  Scenario: Registration times out during user presence
    Given I enter username "test_user_004"
    When I click the register button
    And I enter the correct PIN on the device
    But I do not provide user presence within 30 seconds
    Then the registration should timeout
    And I should see a timeout error message

  @hardware @registration @cancel
  Scenario: User cancels PIN entry during registration
    Given I enter username "test_user_005"
    When I click the register button
    And I cancel the PIN entry
    Then the registration should be cancelled
    And I should see a cancellation error message
