Feature: DIGIPASS FX7 Authentication
  As a user with a registered DIGIPASS FX7 device
  I want to authenticate using my device
  So that I can securely access my account

  Background:
    Given I have a DIGIPASS FX7 device with registered credentials
    And I am on the WebAuthn authentication page

  @hardware @authentication
  Scenario: Successful authentication with valid PIN
    Given I enter username "registered_user"
    When I click the authenticate button
    And I enter the correct PIN on the device
    And I provide user presence on the device
    Then the authentication should succeed
    And I should be logged in

  @hardware @authentication @error
  Scenario: Authentication fails with wrong PIN
    Given I enter username "registered_user"
    When I click the authenticate button
    And I enter an incorrect PIN on the device
    Then the authentication should fail
    And I should see a PIN error message
    When I enter the correct PIN on the device
    And I provide user presence on the device
    Then the authentication should succeed

  @hardware @authentication @timeout
  Scenario: Authentication times out during user presence
    Given I enter username "registered_user"
    When I click the authenticate button
    And I enter the correct PIN on the device
    But I do not provide user presence within 30 seconds
    Then the authentication should timeout
    And I should see a timeout error message

  @hardware @authentication @no_credential
  Scenario: Authentication fails when no credential exists
    Given I enter username "unregistered_user"
    When I click the authenticate button
    Then the authentication should fail immediately
    And I should see a "no credentials found" error message

  @hardware @authentication @discoverable
  Scenario: Successful discoverable credential authentication
    When I click the authenticate button without entering username
    And I select the correct credential from the list
    And I enter the correct PIN on the device
    And I provide user presence on the device
    Then the authentication should succeed
    And I should be logged in

  @hardware @authentication @cancel
  Scenario: User cancels authentication during PIN entry
    Given I enter username "registered_user"
    When I click the authenticate button
    And I cancel the PIN entry
    Then the authentication should be cancelled
    And I should see a cancellation error message
