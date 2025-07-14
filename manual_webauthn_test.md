
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
