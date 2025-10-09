"""
T21 SERVICES - TWO-FACTOR AUTHENTICATION (2FA)
NHS-Grade Security with TOTP (Time-based One-Time Password)
Compatible with Google Authenticator, Microsoft Authenticator, Authy
"""

import pyotp
import qrcode
from io import BytesIO
import base64


def generate_2fa_secret(user_email):
    """
    Generate a new 2FA secret for a user
    
    Args:
        user_email: User's email address
    
    Returns:
        str: Base32 encoded secret key
    """
    return pyotp.random_base32()


def get_totp_uri(user_email, secret, issuer_name="T21 Services"):
    """
    Generate provisioning URI for QR code
    
    Args:
        user_email: User's email
        secret: Base32 secret
        issuer_name: App name shown in authenticator
    
    Returns:
        str: otpauth:// URI
    """
    totp = pyotp.TOTP(secret)
    return totp.provisioning_uri(
        name=user_email,
        issuer_name=issuer_name
    )


def generate_qr_code(uri):
    """
    Generate QR code image from URI
    
    Args:
        uri: otpauth:// URI
    
    Returns:
        BytesIO: QR code image in memory
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(uri)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Save to BytesIO
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    
    return buffer


def get_qr_code_base64(uri):
    """
    Get QR code as base64 string for display in Streamlit
    
    Args:
        uri: otpauth:// URI
    
    Returns:
        str: Base64 encoded image
    """
    buffer = generate_qr_code(uri)
    img_base64 = base64.b64encode(buffer.getvalue()).decode()
    return img_base64


def verify_2fa_code(secret, user_code):
    """
    Verify a 6-digit TOTP code
    
    Args:
        secret: User's Base32 secret
        user_code: 6-digit code from authenticator app
    
    Returns:
        bool: True if code is valid
    """
    totp = pyotp.TOTP(secret)
    
    # Verify with window of 1 (allows 30 seconds before/after for clock drift)
    return totp.verify(user_code, valid_window=1)


def get_current_code(secret):
    """
    Get current valid code (for testing/debugging only)
    
    Args:
        secret: Base32 secret
    
    Returns:
        str: Current 6-digit code
    """
    totp = pyotp.TOTP(secret)
    return totp.now()


def generate_backup_codes(count=10):
    """
    Generate backup codes for account recovery
    
    Args:
        count: Number of backup codes to generate
    
    Returns:
        list: List of backup codes
    """
    import secrets
    import string
    
    codes = []
    for _ in range(count):
        # Generate 8-character alphanumeric code
        code = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(8))
        # Format as XXXX-XXXX for readability
        formatted = f"{code[:4]}-{code[4:]}"
        codes.append(formatted)
    
    return codes


def enable_2fa_for_user(user_email):
    """
    Complete 2FA setup process for a user
    
    Returns:
        dict: {
            'secret': str,
            'qr_uri': str,
            'qr_base64': str,
            'backup_codes': list
        }
    """
    secret = generate_2fa_secret(user_email)
    uri = get_totp_uri(user_email, secret)
    qr_base64 = get_qr_code_base64(uri)
    backup_codes = generate_backup_codes()
    
    return {
        'secret': secret,
        'qr_uri': uri,
        'qr_base64': qr_base64,
        'backup_codes': backup_codes
    }


def is_2fa_enabled(user_data):
    """
    Check if user has 2FA enabled
    
    Args:
        user_data: User dict from database
    
    Returns:
        bool: True if 2FA is enabled
    """
    return user_data.get('two_factor_secret') is not None and user_data.get('two_factor_secret') != ''


def verify_backup_code(user_backup_codes, provided_code):
    """
    Verify a backup code and mark as used
    
    Args:
        user_backup_codes: List of user's backup codes
        provided_code: Code provided by user
    
    Returns:
        tuple: (valid: bool, remaining_codes: list)
    """
    if provided_code in user_backup_codes:
        # Remove used code
        remaining = [code for code in user_backup_codes if code != provided_code]
        return True, remaining
    
    return False, user_backup_codes
