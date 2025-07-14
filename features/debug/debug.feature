Feature: WebAuthn Debug
  Debug WebAuthn hardware authenticator integration

  Background:
    Given I have a DIGIPASS FX7 device connected
    And I am on the WebAuthn registration page

  @debug @hardware @registration
  Scenario: Debug registration flow
    Given I enter username "debug_test"
    When I click the register button with debug
    And I wait for hardware authenticator popup
    Then the registration should succeed
