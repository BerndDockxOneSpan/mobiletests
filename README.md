# Mobile end-to-end tests

Currently, the available tests consist of the desktop webauthn tests, ported to mobile.

## Running

To run the tests, make sure appium is installed and running, and the `UiAutomator2` driver is installed. 
Additionally, these tests require chromedriver to be installed, Appium can download this automatically if it is run with
the `--allow-insecure chromedriver_autodownload` argument.

## Testing Frameworks

This project supports two testing approaches:

### 1. Traditional pytest Tests
- Located in `webauthn/` directory
- Technical unit and integration tests
- Run with: `pytest webauthn/`

### 2. BDD/Gherkin Tests (NEW)
- Located in `features/` directory  
- Business-readable acceptance tests
- Written in natural language using Gherkin syntax
- Run with: `python run_bdd_tests.py` or `behave`
- See [BDD_README.md](BDD_README.md) for detailed documentation

### Quick BDD Examples
```bash
# Run all BDD tests
python run_bdd_tests.py

# Run hardware device tests only
python run_bdd_tests.py --tags @hardware

# Run registration scenarios
python run_bdd_tests.py --tags @registration

# List available test scenarios
python run_bdd_tests.py --list-features
```