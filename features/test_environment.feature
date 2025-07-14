Feature: BDD Framework Test
  Test if the environment setup is working correctly

  @test @debug
  Scenario: Environment setup test
    Given I am on the WebAuthn registration page
    Given I enter username "test_user"
    Then I should see the page is loaded
