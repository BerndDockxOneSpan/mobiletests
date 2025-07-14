Feature: WebAuthn Registration Test
  Test basic WebAuthn registration with timing improvements

  Background:
    Given I have a DIGIPASS FX7 device connected
    And I am on the WebAuthn registration page

  @hardware @registration @improved
  Scenario: Registration with improved timing
    Given I enter username "timing_test"
    When I click the register button
    And I complete the hardware registration flow
    Then the registration should succeed

  @hardware @authentication @improved
  Scenario: Authentication with improved timing
    Given I enter username "timing_test"
    When I click the authenticate button
    And I complete the hardware authentication flow
    Then the authentication should succeed
