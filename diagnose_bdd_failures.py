#!/usr/bin/env python3
"""
BDD Scenario Failure Diagnostic Script
Identifies why authentication and registration scenarios are failing.
"""

import sys
import subprocess
from pathlib import Path

def check_appium_server():
    """Check if Appium server is running."""
    print("🔍 Checking Appium Server...")
    try:
        import urllib.request
        urllib.request.urlopen('http://localhost:4723/status', timeout=5)
        print("✅ Appium server is running on http://localhost:4723")
        return True
    except urllib.error.URLError:
        print("❌ Appium server is not running on http://localhost:4723")
        print("💡 Start Appium with: appium --port 4723")
        return False
    except Exception as e:
        print(f"❌ Error checking Appium server: {e}")
        return False

def check_android_device():
    """Check if Android device is connected."""
    print("\n🔍 Checking Android Device...")
    try:
        result = subprocess.run(['adb', 'devices'], capture_output=True, text=True)
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')[1:]  # Skip header
            devices = [line for line in lines if line.strip() and 'device' in line]
            if devices:
                print(f"✅ Found {len(devices)} Android device(s) connected")
                for device in devices:
                    print(f"   📱 {device}")
                return True
            else:
                print("❌ No Android devices connected")
                print("💡 Connect Android device and enable USB debugging")
                return False
        else:
            print(f"❌ adb command failed: {result.stderr}")
            return False
    except FileNotFoundError:
        print("❌ adb not found - Android SDK not installed or not in PATH")
        return False
    except Exception as e:
        print(f"❌ Error checking Android devices: {e}")
        return False

def check_chrome_browser():
    """Check if Chrome is available on device."""
    print("\n🔍 Checking Chrome Browser...")
    try:
        result = subprocess.run(['adb', 'shell', 'pm', 'list', 'packages', 'chrome'], 
                               capture_output=True, text=True)
        if result.returncode == 0 and 'chrome' in result.stdout:
            print("✅ Chrome browser is installed on device")
            return True
        else:
            print("❌ Chrome browser not found on device")
            print("💡 Install Chrome browser on the Android device")
            return False
    except Exception as e:
        print(f"❌ Error checking Chrome browser: {e}")
        return False

def check_hardware_setup():
    """Check hardware setup requirements."""
    print("\n🔍 Checking Hardware Setup...")
    
    # Check for relay board module
    try:
        import RelayBoard
        print("✅ RelayBoard module is available")
        hardware_available = True
    except ImportError:
        print("❌ RelayBoard module not found")
        hardware_available = False
    
    # Note about DIGIPASS FX7
    print("📝 DIGIPASS FX7 hardware device requirements:")
    print("   - Physical DIGIPASS FX7 device must be connected")
    print("   - Device should be powered and recognized by the system")
    print("   - Relay board should be connected for button automation")
    
    return hardware_available

def suggest_workarounds():
    """Suggest workarounds for missing components."""
    print("\n🛠️  WORKAROUNDS FOR MISSING COMPONENTS:")
    print("-" * 50)
    
    print("1. 📱 No Appium/Device Setup:")
    print("   - Use dry-run mode: behave --dry-run features/")
    print("   - Test step definitions without hardware")
    print("   - Validate Gherkin syntax and step coverage")
    
    print("\n2. 🌐 No Browser Testing:")
    print("   - Use mock/stub implementations")
    print("   - Test business logic without UI interaction")
    print("   - Focus on PIN management and hardware scenarios")
    
    print("\n3. 🔧 No Hardware Device:")
    print("   - Use simulation mode for device interactions")
    print("   - Test timeout and error scenarios")
    print("   - Validate step definitions and flow logic")

def check_bdd_step_coverage():
    """Check if BDD steps are properly defined."""
    print("\n🔍 Checking BDD Step Coverage...")
    try:
        venv_behave = Path(".venv/Scripts/behave.exe")
        if venv_behave.exists():
            behave_cmd = str(venv_behave)
        else:
            behave_cmd = "behave"
        
        # Test registration feature
        result = subprocess.run(
            [behave_cmd, "--dry-run", "features/digipass_fx7/registration.feature"],
            capture_output=True, text=True, cwd=Path.cwd()
        )
        
        if "undefined" in result.stderr.lower():
            print("❌ Found undefined steps in registration feature")
            print(result.stderr)
            return False
        else:
            print("✅ All registration steps are defined")
        
        # Test authentication feature
        result = subprocess.run(
            [behave_cmd, "--dry-run", "features/digipass_fx7/authentication.feature"],
            capture_output=True, text=True, cwd=Path.cwd()
        )
        
        if "undefined" in result.stderr.lower():
            print("❌ Found undefined steps in authentication feature")
            print(result.stderr)
            return False
        else:
            print("✅ All authentication steps are defined")
        
        return True
        
    except Exception as e:
        print(f"❌ Error checking step coverage: {e}")
        return False

def main():
    """Run comprehensive diagnostic."""
    print("=" * 60)
    print("🚀 BDD SCENARIO FAILURE DIAGNOSTIC")
    print("=" * 60)
    
    results = {}
    
    # Check all components
    results['appium'] = check_appium_server()
    results['android'] = check_android_device()
    results['chrome'] = check_chrome_browser() if results['android'] else False
    results['hardware'] = check_hardware_setup()
    results['steps'] = check_bdd_step_coverage()
    
    print("\n" + "=" * 60)
    print("📊 DIAGNOSTIC SUMMARY")
    print("=" * 60)
    
    for component, status in results.items():
        status_icon = "✅" if status else "❌"
        print(f"{component.capitalize():<15} {status_icon}")
    
    print("-" * 60)
    
    if all(results.values()):
        print("🎉 All components are ready!")
        print("🚀 BDD scenarios should run successfully")
    else:
        missing = [comp for comp, status in results.items() if not status]
        print(f"🔴 Missing components: {', '.join(missing)}")
        print("🔧 See workarounds below for testing without missing components")
        suggest_workarounds()
    
    return all(results.values())

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
