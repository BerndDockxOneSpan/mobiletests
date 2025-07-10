from shared.locator import Locator, Context

# Text
class WebAuthnText:
    REGISTER_SUCCESS        = "Success! Now try to authenticate..."
    UNKNOWN_EXCEPTION       = "An unknown error occurred while talking to the credential manager."
    NO_CREDENTIALS          = "That username has no registered credentials"
    PREVIOUSLY_REGISTERED   = "The authenticator was previously registered"
    TIMED_OUT_NOT_ALLOWED   = "The operation either timed out or was not allowed. See: https://www.w3.org/TR/webauthn-2/#sctn-privacy-considerations-client."

# Locators
class WebAuthnLocators:
    USERNAME_BOX            = Locator.by_attributes(Context.WEB, dict(id="input-email"))
    REGISTER_BUTTON         = Locator.by_attributes(Context.WEB, dict(id="register-button"))
    AUTHENTICATE_BUTTON     = Locator.by_attributes(Context.WEB, dict(id="login-button"))
    SUCCESS_BOX             = Locator.by_attributes(Context.WEB, {"class": "alert alert-success"})
    ERROR_BOX               = Locator.by_attributes(Context.WEB, {"class": "alert alert-danger"})
    LOGGED_IN_TEXT          = Locator.by_text(Context.WEB, "You're logged in!")
    LOG_OUT_BUTTON          = Locator.by_link_text(Context.WEB, "Try it again?")
    DELETE_BUTTON           = Locator.by_button_text(Context.WEB, "Delete")
