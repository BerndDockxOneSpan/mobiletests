Feature: DIGIPASS FX7 Credential Management
  As a user with a DIGIPASS FX7 device
  I want to manage my stored credentials
  So that I can control my authentication data

  Background:
    Given I have a DIGIPASS FX7 device connected
    And I am on the WebAuthn management page

  @hardware @credential_management
  Scenario: Store multiple credentials for different services
    Given I register credentials for 5 different usernames
    When I authenticate with each stored credential
    Then all authentications should succeed
    And each credential should work independently

  @hardware @credential_management
  Scenario: Delete specific credential
    Given I have credentials stored for "user1" and "user2"
    When I delete the credential for "user1"
    Then authentication with "user1" should fail
    But authentication with "user2" should still work

  @hardware @credential_management @limit
  Scenario: Reach maximum credential storage limit
    Given I have registered 99 credentials on the device
    When I attempt to register the 100th credential
    Then the registration should succeed
    When I attempt to register the 101st credential
    Then the registration should fail
    And I should see an error about storage limit

  @hardware @credential_management @cross_platform
  Scenario: Use credential across different platforms
    Given I register a credential on Windows platform
    When I move the device to macOS platform
    And I attempt to authenticate with the same credential
    Then the authentication should succeed
    And the credential should work identically

  @hardware @credential_management
  Scenario: Verify credential persistence after power cycle
    Given I register a credential for "persistent_user"
    When I disconnect the device for 10 minutes
    And I reconnect the device
    And I authenticate with "persistent_user"
    Then the authentication should succeed
    And the credential should be unchanged

  @hardware @credential_management @error
  Scenario: Attempt to delete non-existent credential
    Given I have no credentials stored for "nonexistent_user"
    When I attempt to delete credentials for "nonexistent_user"
    Then the operation should fail gracefully
    And I should see an appropriate error message
    And the device should remain in a stable state
