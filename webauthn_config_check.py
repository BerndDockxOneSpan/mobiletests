#!/usr/bin/env python3
"""
Chrome WebAuthn Configuration Checker
Checks if Chrome is properly configured for WebAuthn hardware authenticators.
"""

def check_chrome_webauthn_settings():
    """Check Chrome WebAuthn configuration."""
    print("🔍 Chrome WebAuthn Configuration Check")
    print("=" * 40)
    
    print("\n📋 Required Chrome Settings for WebAuthn:")
    print("1. ✅ Hardware security keys enabled")
    print("2. ✅ WebAuthn API enabled") 
    print("3. ✅ Allow websites to use security keys")
    print("4. ✅ USB security keys allowed")
    
    print("\n🔧 Chrome Flags to Verify (chrome://flags/):")
    chrome_flags = [
        "enable-web-authentication-api",
        "enable-webauthn-provisional-app-id-support", 
        "enable-webauthn-ctap2-support",
        "enable-webauthn-cable-support"
    ]
    
    for flag in chrome_flags:
        print(f"   - {flag}: Should be 'Enabled' or 'Default'")
    
    print("\n🌐 Test URLs to check manually:")
    print("   1. https://webauthn.io/ - Main test site")
    print("   2. chrome://settings/content/usbDevices - USB device permissions")
    print("   3. chrome://device-log/ - Device connection logs")
    
    print("\n⚠️  Common Issues:")
    print("   1. USB debugging mode might interfere with WebAuthn")
    print("   2. Chrome might need 'Allow USB devices' permission")
    print("   3. Android system might block external authenticators")
    print("   4. DIGIPASS device might not be in the right mode")

def check_android_webauthn_config():
    """Check Android WebAuthn configuration."""
    print("\n🤖 Android WebAuthn Configuration")
    print("=" * 40)
    
    print("\n📱 Android Requirements:")
    print("   1. ✅ Android 7.0+ (API level 24+)")
    print("   2. ✅ Chrome browser (not WebView)")
    print("   3. ✅ USB On-The-Go (OTG) support")
    print("   4. ✅ USB debugging enabled")
    
    print("\n🔌 Hardware Connection:")
    print("   1. DIGIPASS FX7 connected via USB OTG")
    print("   2. Device should show up in Android device manager")
    print("   3. No interference from other USB devices")
    
    print("\n🛠️  Debugging Steps:")
    print("   1. Check USB OTG adapter is working")
    print("   2. Try disconnecting/reconnecting DIGIPASS")
    print("   3. Restart Chrome browser")
    print("   4. Clear Chrome cache/cookies for webauthn.io")

def suggest_solutions():
    """Suggest potential solutions."""
    print("\n💡 Potential Solutions")
    print("=" * 25)
    
    solutions = [
        "Add explicit wait after clicking register button (3-5 seconds)",
        "Check if USB OTG permissions are granted to Chrome",
        "Verify DIGIPASS device is in FIDO2 mode (not FIDO U2F only)",
        "Try with Chrome in incognito mode to avoid extension interference",
        "Check Android USB settings - ensure 'Allow USB debugging' is on",
        "Restart Appium server and reconnect device",
        "Test with manual browser to confirm hardware setup works",
        "Check Android logcat for WebAuthn/USB related errors"
    ]
    
    for i, solution in enumerate(solutions, 1):
        print(f"   {i}. {solution}")

def create_manual_test_script():
    """Create a script for manual testing."""
    script = """
# Manual WebAuthn Test Steps
# =========================

1. Open Chrome on Android device manually
2. Navigate to https://webauthn.io/
3. Enter username: manual_test
4. Click "Register" button
5. Observe what happens:
   
   Expected: 
   - "Create a passkey" popup should appear
   - "Use a different device" option should be available
   - After clicking "Use a different device", PIN prompt should appear
   
   If popup doesn't appear:
   - Check Chrome permissions for USB devices
   - Check if DIGIPASS device LED is blinking (indicates FIDO mode)
   - Try disconnecting/reconnecting DIGIPASS
   
6. If popup appears, continue with DIGIPASS PIN entry
7. Check if user presence (button press) is requested

# WebAuthn.io Expected Flow:
# Username -> Register -> Popup -> Different Device -> PIN -> User Presence -> Success
"""
    
    with open("manual_webauthn_test.md", "w", encoding='utf-8') as f:
        f.write(script)
    
    print(f"\n📝 Created manual test guide: manual_webauthn_test.md")

if __name__ == "__main__":
    check_chrome_webauthn_settings()
    check_android_webauthn_config()
    suggest_solutions()
    create_manual_test_script()
    
    print("\n" + "=" * 60)
    print("🎯 NEXT STEPS:")
    print("1. Run manual test to confirm hardware setup")
    print("2. Check debug screenshots when available") 
    print("3. Review Chrome and Android settings")
    print("4. Try suggested solutions one by one")
