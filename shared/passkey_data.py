from shared.locator import Locator, Context

class PasskeyText:
    # Depending on Android version we can have different strings
    CREATE_PASSKEY_1                = "Create passkey to sign in to "
    CREATE_PASSKEY_2                = "Create a passkey"
    WRONG_PIN                       = "Wrong PIN"
    ENTER_PIN_SECURITY_KEY          = "Enter the PIN for your security key"
    SEVEN_ATTEMPTS_REMAINING        = "7 attempts remaining for confirming PIN"

# Locators
class PasskeyLocators:
    CONFIRM_BUTTON                  = Locator.by_id(Context.NATIVE, "com.google.android.gms:id/confirmButton")
    CANCEL_BUTTON                   = Locator.by_id(Context.NATIVE, "com.google.android.gms:id/cancelButton")
    CREATE_PASSKEY_TEXT_1           = Locator.by_contains_text(Context.NATIVE, PasskeyText.CREATE_PASSKEY_1)
    CREATE_PASSKEY_TEXT_2           = Locator.by_text(Context.NATIVE, PasskeyText.CREATE_PASSKEY_2)
    PIN_INPUT_FIELD_DEVICE          = Locator.by_id(Context.NATIVE, "com.android.systemui:id/lockPassword")
    PIN_ERROR_TEXT_DEVICE           = Locator.by_id(Context.NATIVE, "com.android.systemui:id/error")
    PIN_INPUT_FIELD_KEY             = Locator.by_text(Context.NATIVE, PasskeyText.ENTER_PIN_SECURITY_KEY)
    DIFFERENT_DEVICE                = Locator.by_id(Context.NATIVE, "com.google.android.gms:id/use_another_device_button")
    CONNECT_KEY                     = Locator.by_id(Context.NATIVE, "com.google.android.gms:id/fido_usb_instructions_title_textview")
    PIN_ERROR_TEXT_KEY              = Locator.by_id(Context.NATIVE, "com.google.android.gms:id/textinput_error")
    DISCOVERABLE_TITLE = Locator.by_id(Context.NATIVE, "com.android.chrome:id/touch_to_fill_sheet_title")
    DISCOVERABLE_DIFFERENT_DEVICE   = Locator.by_id(Context.NATIVE, "com.android.chrome:id/touch_to_fill_sheet_use_passkeys_other_device")
