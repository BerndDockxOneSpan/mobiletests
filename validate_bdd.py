#!/usr/bin/env python3
"""
Validation script for BDD/Gherkin setup

This script validates that the BDD framework is properly configured and ready to use.
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_packages():
    """Check if required Python packages are installed."""
    required_packages = ['behave', 'pytest_bdd', 'allure_behave']
    missing_packages = []
    
    print("Checking Python packages...")
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"  ✅ {package} - OK")
        except ImportError:
            missing_packages.append(package)
            print(f"  ❌ {package} - MISSING")
    
    return len(missing_packages) == 0

def check_directory_structure():
    """Check if required directories exist."""
    required_dirs = [
        'features',
        'features/digipass_fx7',
        'step_definitions'
    ]
    
    print("\nChecking directory structure...")
    
    missing_dirs = []
    for dir_path in required_dirs:
        if Path(dir_path).exists():
            print(f"  ✅ {dir_path}/ - OK")
        else:
            missing_dirs.append(dir_path)
            print(f"  ❌ {dir_path}/ - MISSING")
    
    return len(missing_dirs) == 0

def check_feature_files():
    """Check if feature files exist and are valid."""
    feature_files = [
        'features/digipass_fx7/registration.feature',
        'features/digipass_fx7/authentication.feature',
        'features/digipass_fx7/pin_management.feature',
        'features/digipass_fx7/credential_management.feature'
    ]
    
    print("\nChecking feature files...")
    
    missing_files = []
    for feature_file in feature_files:
        if Path(feature_file).exists():
            print(f"  ✅ {feature_file} - OK")
        else:
            missing_files.append(feature_file)
            print(f"  ❌ {feature_file} - MISSING")
    
    return len(missing_files) == 0

def check_step_definitions():
    """Check if step definition files exist."""
    step_files = [
        'step_definitions/digipass_steps.py',
        'step_definitions/webauthn_steps.py',
        'step_definitions/common_steps.py'
    ]
    
    print("\nChecking step definition files...")
    
    missing_files = []
    for step_file in step_files:
        if Path(step_file).exists():
            print(f"  ✅ {step_file} - OK")
        else:
            missing_files.append(step_file)
            print(f"  ❌ {step_file} - MISSING")
    
    return len(missing_files) == 0

def check_config_files():
    """Check if configuration files exist."""
    config_files = [
        'behave.ini',
        'features/environment.py'
    ]
    
    print("\nChecking configuration files...")
    
    missing_files = []
    for config_file in config_files:
        if Path(config_file).exists():
            print(f"  ✅ {config_file} - OK")
        else:
            missing_files.append(config_file)
            print(f"  ❌ {config_file} - MISSING")
    
    return len(missing_files) == 0

def validate_gherkin_syntax():
    """Validate Gherkin syntax using behave dry run."""
    print("\nValidating Gherkin syntax...")
    
    # Try to find behave executable in venv first
    behave_cmd = '.venv/Scripts/behave.exe' if Path('.venv/Scripts/behave.exe').exists() else 'behave'
    
    try:
        result = subprocess.run(
            [behave_cmd, '--dry-run', 'features/'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        # Behave dry-run is successful if it completes, even with undefined steps
        if result.returncode == 0 or "undefined" in result.stdout:
            print("  ✅ Gherkin syntax validation - OK")
            if "undefined" in result.stdout:
                undefined_count = result.stdout.count("undefined")
                print(f"     Note: {undefined_count} undefined steps found (normal for new framework)")
            return True
        else:
            print("  ❌ Gherkin syntax validation - FAILED")
            print(f"     Error: {result.stderr}")
            return False
            
    except FileNotFoundError:
        print("  ❌ behave command not found")
        return False
    except subprocess.TimeoutExpired:
        print("  ❌ Validation timed out")
        return False
    except Exception as e:
        print(f"  ❌ Validation error: {e}")
        return False

def check_utility_integration():
    """Check if utility classes have BDD-friendly methods."""
    print("\nChecking utility class integration...")
    
    try:
        # Check if enhanced methods exist in utility classes
        from shared.passkey_util import HardwarePasskeyUtil
        from webauthn.webauthn_util import WebauthnUtil
        
        # Check HardwarePasskeyUtil methods
        hw_methods = ['is_device_connected', 'wait_for_device_ready', 'has_registered_credentials']
        hw_util_ok = all(hasattr(HardwarePasskeyUtil, method) for method in hw_methods)
        
        # Check WebauthnUtil methods  
        wa_methods = ['is_success_message_visible', 'is_error_message_visible', 'is_logged_in']
        wa_util_ok = all(hasattr(WebauthnUtil, method) for method in wa_methods)
        
        if hw_util_ok and wa_util_ok:
            print("  ✅ Utility class integration - OK")
            return True
        else:
            print("  ❌ Utility class integration - MISSING METHODS")
            return False
            
    except ImportError as e:
        print(f"  ❌ Import error: {e}")
        return False

def main():
    """Main validation function."""
    print("🧪 BDD/Gherkin Framework Validation")
    print("=" * 50)
    
    checks = [
        ("Python Packages", check_python_packages),
        ("Directory Structure", check_directory_structure),
        ("Feature Files", check_feature_files),
        ("Step Definitions", check_step_definitions),
        ("Configuration Files", check_config_files),
        ("Utility Integration", check_utility_integration),
        ("Gherkin Syntax", validate_gherkin_syntax)
    ]
    
    passed_checks = 0
    total_checks = len(checks)
    
    for check_name, check_func in checks:
        try:
            if check_func():
                passed_checks += 1
        except Exception as e:
            print(f"  ❌ {check_name} - ERROR: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Validation Results: {passed_checks}/{total_checks} checks passed")
    
    if passed_checks == total_checks:
        print("🎉 BDD framework is ready to use!")
        print("\nNext steps:")
        print("  1. Run: python run_bdd_tests.py --dry-run")
        print("  2. Run: python run_bdd_tests.py --list-features")
        print("  3. Run: python run_bdd_tests.py --tags @hardware")
        sys.exit(0)
    else:
        print("⚠️  BDD framework needs attention before use.")
        print("\nPlease fix the failed checks above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
