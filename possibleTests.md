# DIGIPASS FX7 - Possible Test Scenarios

Based on the DIGIPASS FX7 User Manual, this document outlines comprehensive test scenarios to validate the hardware security key functionality.

## Test Categories

- [Device Connection and Power Tests](#device-connection-and-power-tests)
- [PIN Management Tests](#pin-management-tests)
- [FIDO Registration Tests](#fido-registration-tests)
- [FIDO Authentication Tests](#fido-authentication-tests)
- [LED Behavior Tests](#led-behavior-tests)
- [Credential Management Tests](#credential-management-tests)
- [Device Reset Tests](#device-reset-tests)
- [Security and Lockout Tests](#security-and-lockout-tests)
- [Platform Compatibility Tests](#platform-compatibility-tests)
- [Error Handling and Edge Cases](#error-handling-and-edge-cases)

---

## Device Connection and Power Tests

### TEST-001: Basic Device Connection
**Action:** Connect DIGIPASS FX7 to USB-C port on computer/mobile device  
**Expected Result:** 
- Device LED briefly turns solid white indicating device is ready
- Device is recognized by the operating system
- No error messages displayed

### TEST-002: USB-A to USB-C Adapter Connection
**Action:** Connect DIGIPASS FX7 using USB-A to USB-C adapter  
**Expected Result:** 
- Device functions identically to direct USB-C connection
- LED indicates device is ready
- All FIDO operations work normally

### TEST-003: Device Disconnection During Idle
**Action:** Disconnect device when not in use  
**Expected Result:** 
- Device powers off immediately
- No data loss or corruption
- Device reconnects normally when plugged back in

### TEST-004: Power Supply Voltage Range
**Action:** Test device with USB power supply between 4.40-5.50 volts  
**Expected Result:** 
- Device operates normally throughout voltage range
- LED functions properly
- All FIDO operations complete successfully

---

## PIN Management Tests

### TEST-010: Initial PIN Setup - Minimum Length
**Action:** Set PIN with exactly 4 decimal digits (e.g., "1234")  
**Expected Result:** 
- PIN is accepted and saved successfully
- Device can be used for FIDO operations
- PIN verification works correctly

### TEST-011: Initial PIN Setup - Maximum Length ASCII
**Action:** Set PIN with 63 ASCII characters  
**Expected Result:** 
- PIN is accepted and saved successfully
- All 63 characters are stored correctly
- PIN verification works with full-length PIN

### TEST-012: Initial PIN Setup - Maximum Length UTF-8
**Action:** Set PIN with special characters approaching UTF-8 byte limit  
**Expected Result:** 
- Device correctly calculates UTF-8 byte length
- PIN is rejected if exceeding 63 bytes
- PIN is accepted if within 63-byte limit

### TEST-013: PIN Setup - Alphanumeric Characters
**Action:** Set PIN using mix of letters and numbers (e.g., "Test123!")  
**Expected Result:** 
- PIN is accepted and saved successfully
- Case sensitivity is preserved
- Special characters are handled correctly

### TEST-014: PIN Setup - International Characters
**Action:** Set PIN using accented or international characters  
**Expected Result:** 
- Characters are accepted if within UTF-8 byte limit
- PIN verification works correctly with international characters
- Proper encoding/decoding of special characters

### TEST-015: PIN Change Operation
**Action:** Change existing PIN to new PIN following platform-specific steps  
**Expected Result:** 
- Old PIN is required for verification
- New PIN is accepted and replaces old PIN
- Device works with new PIN for subsequent operations

### TEST-016: PIN Change - Invalid Old PIN
**Action:** Attempt to change PIN with incorrect old PIN  
**Expected Result:** 
- Operation is rejected
- Error message indicates incorrect old PIN
- Original PIN remains unchanged

---

## FIDO Registration Tests

### TEST-020: First-Time Registration
**Action:** Register device with webauthn.io using fresh device with PIN set  
**Expected Result:** 
- Registration process completes successfully
- Device prompts for PIN entry
- User presence button press is required
- Success message displayed on website

### TEST-021: Registration Without PIN Set
**Action:** Attempt registration on device without PIN configured  
**Expected Result:** 
- System automatically initiates PIN setup procedure
- Registration continues after PIN is set
- Complete process succeeds

### TEST-022: Registration - PIN Entry During Process
**Action:** Complete registration flow including PIN entry step  
**Expected Result:** 
- PIN prompt appears during registration
- Correct PIN allows process to continue
- User presence step follows PIN entry
- Registration completes successfully

### TEST-023: Registration - User Presence Required
**Action:** Complete registration but delay button press for user presence  
**Expected Result:** 
- LED blinks white indicating user presence needed
- Process waits for button press
- Button press completes registration
- Success confirmation received

### TEST-024: Multiple Credential Registration
**Action:** Register device with multiple different services/accounts  
**Expected Result:** 
- Each registration creates separate credential
- Device stores up to 100 discoverable credentials
- No interference between different registrations
- All credentials remain functional

### TEST-025: Registration with Different Usernames
**Action:** Register same device with different usernames on same service  
**Expected Result:** 
- Each username creates separate credential
- Credentials are stored independently
- Authentication works correctly for each username
- No credential conflicts occur

---

## FIDO Authentication Tests

### TEST-030: Basic Authentication
**Action:** Authenticate using previously registered credential  
**Expected Result:** 
- Authentication prompt appears
- PIN entry required (if configured by service)
- User presence button press required
- Authentication succeeds and user is logged in

### TEST-031: Authentication - PIN Required
**Action:** Authenticate with service that requires PIN verification  
**Expected Result:** 
- PIN prompt appears during authentication
- Correct PIN allows process to continue
- User presence follows PIN verification
- Authentication completes successfully

### TEST-032: Authentication - PIN Not Required
**Action:** Authenticate with service that doesn't require PIN  
**Expected Result:** 
- Only user presence (button press) required
- No PIN prompt appears
- Authentication completes with button press only
- User is successfully authenticated

### TEST-033: Discoverable Credential Authentication
**Action:** Authenticate using discoverable credential without username  
**Expected Result:** 
- Device presents list of available credentials
- User can select appropriate credential
- Authentication proceeds with selected credential
- Login succeeds for correct user account

### TEST-034: Authentication After Device Reconnection
**Action:** Disconnect and reconnect device, then authenticate  
**Expected Result:** 
- Device reconnects and initializes properly
- All previously registered credentials still work
- Authentication process functions normally
- No data loss or credential corruption

---

## LED Behavior Tests

### TEST-040: Device Ready Indicator
**Action:** Connect device to USB port  
**Expected Result:** 
- LED briefly turns solid white upon connection
- Indicates device is ready for operation
- LED turns off after initial indication

### TEST-041: User Presence Request Indicator
**Action:** Initiate FIDO operation requiring user presence  
**Expected Result:** 
- LED starts blinking white
- Blinking continues until button is pressed
- LED stops blinking after button press
- Operation continues after user presence provided

### TEST-042: LED During PIN Entry
**Action:** Monitor LED behavior during PIN entry phase  
**Expected Result:** 
- LED behavior is consistent and appropriate
- No misleading or confusing LED states
- LED clearly indicates when user action is needed

### TEST-043: LED During Error Conditions
**Action:** Trigger error conditions and observe LED  
**Expected Result:** 
- LED behavior helps indicate error state
- Distinguishable from normal operation states
- Consistent across different error types

---

## Credential Management Tests

### TEST-050: View Stored Credentials
**Action:** Use Chrome security settings to view stored credentials  
**Expected Result:** 
- List of discoverable credentials is displayed
- Credential information is accurate
- All registered accounts are shown
- Credential count is correct

### TEST-051: Delete Single Credential
**Action:** Delete one specific credential using Chrome settings  
**Expected Result:** 
- Selected credential is removed
- Other credentials remain unaffected
- Deleted credential no longer works for authentication
- Remaining credentials function normally

### TEST-052: Delete All Credentials
**Action:** Delete all stored credentials individually  
**Expected Result:** 
- All credentials are successfully removed
- Device shows no stored credentials
- Authentication fails for all previously registered accounts
- Device ready for new registrations

### TEST-053: Credential Storage Limit
**Action:** Register maximum number of discoverable credentials (100)  
**Expected Result:** 
- Device accepts up to 100 credentials
- All 100 credentials can be stored
- Device rejects 101st credential or manages storage appropriately
- All stored credentials remain functional

---

## Device Reset Tests

### TEST-060: Factory Reset - Windows
**Action:** Perform factory reset using Windows Settings app  
**Expected Result:** 
- Reset process completes successfully
- All credentials are deleted
- PIN is removed
- Device reverts to factory state
- Device ready for new setup

### TEST-061: Factory Reset - Chrome
**Action:** Perform factory reset using Chrome security settings  
**Expected Result:** 
- Reset confirmation process works correctly
- Device requires disconnect/reconnect as specified
- Button press confirmation within 10 seconds works
- Complete reset removes all data

### TEST-062: Reset After PIN Lockout
**Action:** Lock device with 8 wrong PIN attempts, then reset  
**Expected Result:** 
- Locked device can be successfully reset
- Reset removes PIN lockout condition
- Device returns to usable state
- New PIN can be set after reset

### TEST-063: Reset Verification
**Action:** Verify device state after factory reset  
**Expected Result:** 
- No credentials remain on device
- PIN is completely removed
- All user data is erased
- Device behaves like new device
- Can set new PIN and register new credentials

---

## Security and Lockout Tests

### TEST-070: PIN Lockout - 3 Consecutive Attempts
**Action:** Enter wrong PIN 3 times consecutively  
**Expected Result:** 
- After 3rd wrong attempt, device requires USB re-insertion
- Error message indicates need to reconnect device
- Device cannot be used until disconnected and reconnected
- PIN attempt counter resets after reconnection

### TEST-071: PIN Lockout - 8 Total Attempts
**Action:** Enter wrong PIN 8 times total (across multiple sessions)  
**Expected Result:** 
- After 8th wrong attempt, device becomes locked
- Device cannot be used for any FIDO operations
- Only factory reset can restore device functionality
- Clear error message indicates device is locked

### TEST-072: PIN Retry After USB Reconnection
**Action:** Trigger 3-attempt lockout, reconnect, then retry PIN  
**Expected Result:** 
- Device allows PIN attempts after reconnection
- Correct PIN works normally after reconnection
- Wrong PIN starts new attempt counter
- Device functions normally with correct PIN

### TEST-073: Partial Lockout Recovery
**Action:** Test PIN entry after various numbers of wrong attempts  
**Expected Result:** 
- Device tracks attempt count correctly
- Behavior is consistent with documented lockout rules
- Recovery process works as specified
- No unexpected lockout conditions

---

## Platform Compatibility Tests

### TEST-080: Windows 10/11 Compatibility
**Action:** Test device on Windows 10 version 1903+ and Windows 11  
**Expected Result:** 
- Device is recognized properly
- Windows Settings app can manage device
- All FIDO operations work correctly
- Native Windows Hello integration functions

### TEST-081: macOS Compatibility
**Action:** Test device on macOS 13 or later  
**Expected Result:** 
- Device is recognized by macOS
- Chrome security settings can manage device
- Safari and Chrome FIDO operations work
- No macOS-specific issues occur

### TEST-082: Linux Compatibility
**Action:** Test device on Ubuntu 22.04.2 or later  
**Expected Result:** 
- Device is recognized by Linux
- Chrome security settings work correctly
- FIDO operations function in supported browsers
- No permission or driver issues

### TEST-083: Android Compatibility
**Action:** Test device on Android 12 or later with USB-C  
**Expected Result:** 
- Device is recognized by Android
- FIDO operations work in mobile browsers
- USB-C connection is stable
- Mobile-specific features function correctly

### TEST-084: Browser Compatibility
**Action:** Test device with Chrome 111+, Firefox, Safari, Edge  
**Expected Result:** 
- All browsers supporting WebAuthn API work correctly
- FIDO operations are consistent across browsers
- No browser-specific compatibility issues
- WebAuthn API functions properly

---

## Error Handling and Edge Cases

### TEST-090: Authentication Without Registration
**Action:** Attempt to authenticate without prior registration  
**Expected Result:** 
- Clear error message indicates no credentials found
- Process fails gracefully
- User receives appropriate guidance
- No device errors or confusion

### TEST-091: Registration with Same Username
**Action:** Attempt to register same username twice on same service  
**Expected Result:** 
- System handles duplicate registration appropriately
- Either overwrites previous credential or rejects duplicate
- Behavior is consistent and documented
- No data corruption occurs

### TEST-092: Device Removal During Operation
**Action:** Disconnect device during active FIDO operation  
**Expected Result:** 
- Operation fails gracefully
- Clear error message about device disconnection
- No data corruption on device
- Device works normally when reconnected

### TEST-093: Rapid Operation Attempts
**Action:** Perform multiple FIDO operations in quick succession  
**Expected Result:** 
- Device handles rapid requests appropriately
- No race conditions or conflicts occur
- Each operation completes correctly
- Device remains stable throughout

### TEST-094: Invalid PIN Format
**Action:** Attempt to set PIN with invalid characters or length  
**Expected Result:** 
- PIN validation rejects invalid formats
- Clear error message explains requirements
- PIN setup can be retried with valid input
- No device state corruption

### TEST-095: Timeout Scenarios
**Action:** Start FIDO operation but don't complete user actions  
**Expected Result:** 
- Operations timeout appropriately
- Clear timeout error messages
- Device returns to ready state
- Subsequent operations work normally

### TEST-096: Power Interruption Recovery
**Action:** Disconnect device during various operation phases  
**Expected Result:** 
- Device recovers gracefully from power loss
- No credential corruption occurs
- Device state remains consistent
- Operations can be retried successfully

### TEST-097: Maximum Credential Limit
**Action:** Attempt to register 101st credential  
**Expected Result:** 
- Device properly enforces 100-credential limit
- Clear error message about storage limit
- Existing credentials remain unaffected
- User can delete credentials to make space

### TEST-098: Cross-Platform Credential Usage
**Action:** Register on one platform, authenticate on another  
**Expected Result:** 
- Credentials work across different platforms
- No platform-specific credential issues
- Authentication succeeds regardless of registration platform
- Credential portability is maintained

### TEST-099: Long-Term Storage Reliability
**Action:** Test credentials after extended periods without use  
**Expected Result:** 
- Credentials remain valid over time
- No degradation in authentication success
- Device maintains data integrity
- Long-term reliability is demonstrated

---

## Test Environment Requirements

### Hardware Requirements
- DIGIPASS FX7 device
- Computers/devices with USB-C or USB-A ports
- USB-A to USB-C adapters for testing
- Power supply testing equipment (4.40-5.50V range)

### Software Requirements
- Windows 10 version 1903+ / Windows 11
- macOS 13+
- Ubuntu 22.04.2+
- Android 12+
- Chrome 111+, Firefox, Safari, Edge browsers
- Access to webauthn.io or similar FIDO test sites

### Network Requirements
- Internet access for FIDO service testing
- Access to various FIDO2-enabled services
- Ability to test both local and remote authentication

---

## Test Execution Notes

1. **Test Order**: Execute tests in logical sequence (setup → basic functions → edge cases)
2. **Device State**: Reset device to known state between major test categories
3. **Documentation**: Record exact error messages and device responses
4. **Timing**: Note response times for operations (user experience impact)
5. **Reproducibility**: Verify that issues can be consistently reproduced
6. **Platform Testing**: Execute core test scenarios on all supported platforms
7. **Security Focus**: Pay special attention to lockout and reset functionality
8. **User Experience**: Evaluate clarity of error messages and LED indicators

---

## Success Criteria

Each test should meet these criteria:
- **Functionality**: Device performs expected operation correctly
- **Security**: Security mechanisms work as documented
- **Usability**: User interface and feedback are clear and helpful
- **Reliability**: Operations are consistent and repeatable
- **Compatibility**: Device works correctly across supported platforms
- **Error Handling**: Errors are handled gracefully with clear feedback
- **Documentation Accuracy**: Device behavior matches user manual specifications
