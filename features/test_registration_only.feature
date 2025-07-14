Feature: Test Registration Flow Only
  Test the hardware registration flow in isolation

  @hardware @registration @browser
  Scenario: Test hardware registration flow method
    Given I have a DIGIPASS FX7 device connected
    And I am on the WebAuthn registration page
    And I enter username "test_reg_flow"
    When I click the register button
    When I complete the hardware registration flow
    Then the registration should succeed
