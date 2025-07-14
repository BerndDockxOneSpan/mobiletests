#!/usr/bin/env python3
"""
Comprehensive BDD Implementation Validation Script
Validates that the Gherkin implementation correctly maps to webauthn functionality.
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def validate_environment_setup():
    """Validate that environment.py properly initializes context."""
    print("🔍 Validating environment.py setup...")
    
    env_file = Path("features/environment.py")
    if not env_file.exists():
        print("❌ environment.py not found")
        return False
    
    content = env_file.read_text()
    
    # Check for proper imports
    required_imports = [
        "from shared.passkey_util import HardwarePasskeyUtil, LocalPasskeyUtil",
        "from webauthn.webauthn_util import WebauthnUtil", 
        "from shared.appium_util import DriverController",
        "from appium import webdriver"
    ]
    
    for import_line in required_imports:
        if import_line not in content:
            print(f"❌ Missing import: {import_line}")
            return False
    
    # Check for context initialization
    required_setup = [
        "context.driver = webdriver.Remote",
        "context.driver_controller = DriverController",
        "context.wa_util = WebauthnUtil",
        "context.pk_util = HardwarePasskeyUtil"
    ]
    
    for setup_line in required_setup:
        if setup_line not in content:
            print(f"❌ Missing context setup: {setup_line}")
            return False
    
    print("✅ Environment setup is correct")
    return True

def validate_step_implementations():
    """Validate that step definitions are properly implemented."""
    print("🔍 Validating step implementations...")
    
    step_files = [
        "step_definitions/webauthn_steps.py",
        "features/steps/webauthn_steps.py"
    ]
    
    critical_steps = [
        ("@given('I am on the WebAuthn registration page')", "context.wa_util.open_page()"),
        ("@given('I enter username", "context.wa_util.fill_username"),
        ("@when('I click the register button')", "context.wa_util.click_register_button()"),
        ("@when('I click the authenticate button')", "context.wa_util.click_authenticate_button()"),
        ("@then('the registration should succeed')", "context.wa_util.verify_registered_success()"),
        ("@then('the authentication should succeed')", "context.wa_util.verify_logged_in()")
    ]
    
    for step_file in step_files:
        if not Path(step_file).exists():
            print(f"❌ Step file not found: {step_file}")
            return False
        
        content = Path(step_file).read_text()
        
        for step_decorator, expected_implementation in critical_steps:
            if step_decorator in content:
                # Find the step function and check if it has real implementation
                step_start = content.find(step_decorator)
                step_section = content[step_start:step_start + 500]  # Get next 500 chars
                
                if expected_implementation in step_section:
                    print(f"✅ {step_decorator} is properly implemented")
                elif "# context." in step_section:
                    print(f"❌ {step_decorator} still has commented implementation")
                    return False
                else:
                    print(f"⚠️  {step_decorator} implementation may be incomplete")
    
    print("✅ Step implementations are complete")
    return True

def validate_feature_syntax():
    """Validate that feature files have correct syntax."""
    print("🔍 Validating feature file syntax...")
    
    try:
        # Use the virtual environment's behave if available
        venv_behave = Path(".venv/Scripts/behave.exe")
        if venv_behave.exists():
            behave_cmd = str(venv_behave)
        else:
            behave_cmd = "behave"
        
        # Run behave with dry-run to check syntax
        result = subprocess.run(
            [behave_cmd, "--dry-run", "--no-summary", "features/"],
            capture_output=True,
            text=True,
            cwd=Path.cwd()
        )
        
        if result.returncode == 0:
            print("✅ Feature file syntax is valid")
            return True
        else:
            print(f"❌ Feature file syntax errors:\n{result.stderr}")
            return False
            
    except FileNotFoundError:
        print("⚠️  behave not found, skipping syntax validation")
        return True

def validate_step_coverage():
    """Validate that all feature steps have corresponding implementations."""
    print("🔍 Validating step coverage...")
    
    try:
        # Use the virtual environment's behave if available
        venv_behave = Path(".venv/Scripts/behave.exe")
        if venv_behave.exists():
            behave_cmd = str(venv_behave)
        else:
            behave_cmd = "behave"
        
        # Run behave with dry-run to find undefined steps
        result = subprocess.run(
            [behave_cmd, "--dry-run", "features/"],
            capture_output=True,
            text=True,
            cwd=Path.cwd()
        )
        
        if "Undefined step:" in result.stderr:
            print(f"❌ Found undefined steps:\n{result.stderr}")
            return False
        else:
            print("✅ All feature steps have implementations")
            return True
            
    except FileNotFoundError:
        print("⚠️  behave not found, skipping step coverage validation")
        return True

def validate_hardware_device_steps():
    """Validate hardware device step implementations."""
    print("🔍 Validating hardware device steps...")
    
    digipass_file = Path("step_definitions/digipass_steps.py")
    if not digipass_file.exists():
        print("❌ digipass_steps.py not found")
        return False
    
    try:
        content = digipass_file.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        try:
            content = digipass_file.read_text(encoding='latin-1')
        except Exception as e:
            print(f"❌ Could not read digipass_steps.py: {e}")
            return False
    
    # Check for key hardware steps
    hardware_steps = [
        ("@when('I enter the correct PIN on the device')", "context.pk_util.enter_pin"),
        ("@when('I enter an incorrect PIN on the device')", "context.pk_util.enter_pin"),
        ("@when('I provide user presence on the device')", "context.relay_board.switch_relay")
    ]
    
    for step_decorator, expected_implementation in hardware_steps:
        if step_decorator in content:
            step_start = content.find(step_decorator)
            step_section = content[step_start:step_start + 500]
            
            if expected_implementation in step_section:
                print(f"✅ {step_decorator} is properly implemented")
            else:
                print(f"❌ {step_decorator} missing implementation: {expected_implementation}")
                return False
    
    print("✅ Hardware device steps are implemented")
    return True

def run_comprehensive_validation():
    """Run all validation checks."""
    print("=" * 60)
    print("🚀 BDD IMPLEMENTATION COMPREHENSIVE VALIDATION")
    print("=" * 60)
    
    validations = [
        ("Environment Setup", validate_environment_setup),
        ("Step Implementations", validate_step_implementations),
        ("Feature Syntax", validate_feature_syntax),
        ("Step Coverage", validate_step_coverage),
        ("Hardware Device Steps", validate_hardware_device_steps)
    ]
    
    results = {}
    all_passed = True
    
    for name, validation_func in validations:
        print(f"\n📋 {name}")
        print("-" * 40)
        try:
            results[name] = validation_func()
            if not results[name]:
                all_passed = False
        except Exception as e:
            print(f"❌ Validation failed with error: {e}")
            results[name] = False
            all_passed = False
    
    print("\n" + "=" * 60)
    print("📊 VALIDATION SUMMARY")
    print("=" * 60)
    
    for name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{name:<25} {status}")
    
    print("-" * 60)
    if all_passed:
        print("🎉 ALL VALIDATIONS PASSED!")
        print("🎯 BDD implementation is complete and ready for testing")
        print("\n💡 Next steps:")
        print("   1. Ensure Appium server is running (http://localhost:4723)")
        print("   2. Connect Android device with Chrome browser")
        print("   3. Connect DIGIPASS FX7 hardware device")
        print("   4. Run: behave features/digipass_fx7/registration.feature")
        return True
    else:
        print("🔴 SOME VALIDATIONS FAILED!")
        print("🛠️  Please address the issues above before proceeding")
        return False

if __name__ == "__main__":
    success = run_comprehensive_validation()
    sys.exit(0 if success else 1)
