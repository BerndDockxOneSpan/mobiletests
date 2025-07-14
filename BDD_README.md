# BDD Testing with Gherkin for DIGIPASS FX7

This document explains how to use the Behavior-Driven Development (BDD) testing framework implemented in this project using Gherkin syntax and Behave.

## Overview

The BDD framework allows you to write tests in natural language using Gherkin syntax, making them readable by both technical and non-technical stakeholders.

## Directory Structure

```
mobiletests-master/
├── features/                           # Gherkin feature files
│   ├── environment.py                  # Test environment setup
│   └── digipass_fx7/                  # DIGIPASS FX7 specific features
│       ├── registration.feature        # Registration scenarios
│       ├── authentication.feature     # Authentication scenarios
│       ├── pin_management.feature     # PIN management scenarios
│       └── credential_management.feature # Credential scenarios
├── step_definitions/                  # Python step implementations
│   ├── digipass_steps.py             # DIGIPASS FX7 device steps
│   ├── webauthn_steps.py             # WebAuthn web interface steps
│   └── common_steps.py               # Reusable common steps
├── behave.ini                        # Behave configuration
└── run_bdd_tests.py                  # Test runner script
```

## Installation

The required dependencies are already installed in your virtual environment:

```bash
# Dependencies are in requirements.txt:
behave>=1.2.6
pytest-bdd>=6.1.1
allure-behave>=2.13.2
```

## Running Tests

### Using the Test Runner Script

```bash
# Run all BDD tests
python run_bdd_tests.py

# Run specific feature
python run_bdd_tests.py --features features/digipass_fx7/registration.feature

# Run tests with specific tags
python run_bdd_tests.py --tags @hardware
python run_bdd_tests.py --tags "@registration and @hardware"
python run_bdd_tests.py --tags "@authentication or @pin_management"

# Run with different output formats
python run_bdd_tests.py --format junit --output reports/
python run_bdd_tests.py --format json --output reports/

# Dry run (validate syntax without execution)
python run_bdd_tests.py --dry-run

# List available features and tags
python run_bdd_tests.py --list-features
python run_bdd_tests.py --list-tags
```

### Using Behave Directly

```bash
# Run all features
behave

# Run specific feature
behave features/digipass_fx7/registration.feature

# Run with tags
behave --tags @hardware
behave --tags "@registration and not @slow"

# Generate reports
behave --junit --junit-directory reports/
behave --format json --outfile reports/results.json
```

## Available Tags

- `@hardware` - Tests involving hardware DIGIPASS FX7 device
- `@local` - Tests using local device passkeys
- `@registration` - User registration scenarios
- `@authentication` - User authentication scenarios
- `@pin_management` - PIN setup and management scenarios
- `@credential_management` - Credential storage and management
- `@error` - Error handling scenarios
- `@timeout` - Timeout-related scenarios
- `@lockout` - PIN lockout scenarios
- `@cancel` - User cancellation scenarios
- `@slow` - Long-running tests
- `@cross_platform` - Cross-platform compatibility tests

## Writing New Feature Files

### Basic Gherkin Syntax

```gherkin
Feature: Description of the feature
  As a [role]
  I want [goal]
  So that [benefit]

  Background:
    Given common setup steps

  @tag1 @tag2
  Scenario: Description of the scenario
    Given initial condition
    When action is performed
    Then expected result occurs
    And additional verification
```

### Example Feature

```gherkin
Feature: PIN Validation
  As a user with a DIGIPASS FX7 device
  I want PIN validation to work correctly
  So that my device is secure

  @hardware @pin_management
  Scenario: Valid PIN is accepted
    Given I have a DIGIPASS FX7 device connected
    When I set a PIN with exactly 4 characters "1234"
    Then the PIN should be accepted and saved
    And the device should be ready for FIDO operations
```

## Writing Step Definitions

Step definitions are Python functions that implement the Gherkin steps:

```python
from behave import given, when, then

@given('I have a DIGIPASS FX7 device connected')
def step_device_connected(context):
    """Verify device is connected and ready."""
    assert context.pk_util.is_device_connected()

@when('I set a PIN with exactly {length:d} characters "{pin}"')
def step_set_pin_exact_length(context, length, pin):
    """Set a PIN with exact character count."""
    assert len(pin) == length
    context.pk_util.set_pin(pin)

@then('the PIN should be accepted and saved')
def step_pin_accepted_saved(context):
    """Verify PIN was accepted and saved."""
    assert context.pk_util.verify_pin_saved()
```

## Context and Data Sharing

The `context` object is used to share data between steps:

```python
# Store data in one step
context.username = "testuser"
context.pin = "1234"

# Use data in another step
assert context.username == "testuser"
```

## Environment Setup

The `features/environment.py` file handles test setup and teardown:

```python
def before_scenario(context, scenario):
    """Setup before each scenario."""
    if 'hardware' in scenario.tags:
        context.pk_util = HardwarePasskeyUtil(context.controller, context.relay_board)
    elif 'local' in scenario.tags:
        context.pk_util = LocalPasskeyUtil(context.controller)

def after_scenario(context, scenario):
    """Cleanup after each scenario."""
    if hasattr(context, 'pk_util'):
        context.pk_util.cleanup()
```

## Integration with Existing Tests

BDD tests complement the existing pytest-based tests:

- **Pytest tests**: Technical, detailed unit and integration tests
- **BDD tests**: Business-readable acceptance tests and user workflows

Both test types can share the same utility classes and infrastructure.

## Reporting

### JUnit Reports (for CI/CD)
```bash
behave --junit --junit-directory reports/
```

### JSON Reports
```bash
behave --format json --outfile reports/results.json
```

### HTML Reports (with Allure)
```bash
behave --format allure_behave.formatter:AllureFormatter --outdir reports/allure-results/
allure serve reports/allure-results/
```

## Best Practices

1. **Keep scenarios focused**: Each scenario should test one specific behavior
2. **Use descriptive names**: Make scenarios readable by non-technical stakeholders
3. **Avoid technical details in steps**: Focus on business behavior, not implementation
4. **Reuse step definitions**: Create reusable steps for common actions
5. **Use appropriate tags**: Tag scenarios for easy filtering and organization
6. **Keep setup minimal**: Use Background for common setup, but keep it light

## Troubleshooting

### Common Issues

1. **Step not found**: Make sure step definitions are in the `step_definitions/` directory
2. **Import errors**: Check that all required modules are installed
3. **Device connection issues**: Verify hardware setup and relay board configuration
4. **Timeout issues**: Increase timeout values for slow operations

### Debug Mode

Run with verbose output to see detailed execution:

```bash
behave --verbose --no-capture
```

### Dry Run for Syntax Validation

```bash
behave --dry-run
```

This validates Gherkin syntax and step definitions without executing the tests.

## Contributing

When adding new BDD tests:

1. Write the feature file first in plain English
2. Implement step definitions that are reusable
3. Add appropriate tags for categorization
4. Update this README if adding new patterns or conventions
5. Test both success and failure scenarios
