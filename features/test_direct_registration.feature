Feature: Test Registration Flow Directly
  Test calling do_registration_flow directly without username entry

  @hardware @registration @direct
  Scenario: Test hardware registration flow method directly
    Given I have a DIGIPASS FX7 device connected
    And I am on the WebAuthn registration page
    When I click the register button directly
    And I complete the hardware registration flow
    Then the registration should succeed
