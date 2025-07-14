Feature: DIGIPASS FX7 PIN Management
  As a user with a DIGIPASS FX7 device
  I want to manage my device PIN
  So that I can maintain secure access to my credentials

  Background:
    Given I have a DIGIPASS FX7 device connected

  @hardware @pin_management
  Scenario: Set initial PIN with minimum length
    Given the device has no PIN set
    When I set a PIN with exactly 4 characters "1234"
    Then the PIN should be accepted and saved
    And the device should be ready for FIDO operations

  @hardware @pin_management
  Scenario: Set initial PIN with maximum ASCII length
    Given the device has no PIN set
    When I set a PIN with 63 ASCII characters
    Then the PIN should be accepted and saved
    And all characters should be stored correctly

  @hardware @pin_management @error
  Scenario: Reject PIN that is too short
    Given the device has no PIN set
    When I attempt to set a PIN with 3 characters "123"
    Then the PIN should be rejected
    And I should see an error about minimum length requirements

  @hardware @pin_management @error
  Scenario: Reject PIN that exceeds UTF-8 byte limit
    Given the device has no PIN set
    When I attempt to set a PIN with special characters exceeding 63 bytes
    Then the PIN should be rejected
    And I should see an error about byte limit exceeded

  @hardware @pin_management
  Scenario: Change existing PIN with correct old PIN
    Given the device has a PIN set to "1234"
    When I change the PIN from "1234" to "5678"
    Then the PIN change should succeed
    And the device should work with the new PIN "5678"

  @hardware @pin_management @error
  Scenario: Fail to change PIN with incorrect old PIN
    Given the device has a PIN set to "1234"
    When I attempt to change the PIN from "9999" to "5678"
    Then the PIN change should fail
    And I should see an error about incorrect old PIN
    And the original PIN "1234" should remain unchanged

  @hardware @pin_management @lockout
  Scenario: PIN lockout after 3 consecutive wrong attempts
    Given the device has a PIN set to "1234"
    When I enter incorrect PIN "9999" 3 times consecutively
    Then the device should require USB re-insertion
    And I should see an error message about reconnection
    When I disconnect and reconnect the USB device
    Then the PIN attempt counter should be reset
    And I should be able to enter the correct PIN

  @hardware @pin_management @lockout
  Scenario: Permanent lockout after 8 total wrong attempts
    Given the device has a PIN set to "1234"
    When I enter incorrect PIN across multiple sessions totaling 8 attempts
    Then the device should be permanently locked
    And I should see an error about device being locked
    And only factory reset should restore functionality
