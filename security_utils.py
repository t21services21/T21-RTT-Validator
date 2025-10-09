"""
T21 SERVICES - SECURITY UTILITIES
NHS-Grade Security Functions
"""

import re
from datetime import datetime, timedelta


def validate_password_strength(password):
    """
    Validate password against NHS security requirements
    
    Requirements:
    - At least 12 characters
    - Contains uppercase letter
    - Contains lowercase letter
    - Contains number
    - Contains special character
    - No common passwords
    - No sequential characters
    
    Returns:
        dict: {
            'valid': bool,
            'score': int (0-100),
            'feedback': list of strings,
            'strength': str ('Weak', 'Fair', 'Good', 'Strong', 'Excellent')
        }
    """
    
    feedback = []
    score = 0
    
    # Common weak passwords (add more as needed)
    common_passwords = [
        'password', 'password123', '12345678', 'qwerty', 'abc123',
        'password1', 'admin', 'letmein', 'welcome', 'monkey',
        'dragon', 'master', 'sunshine', 'princess', 'football'
    ]
    
    # Length check
    if len(password) < 12:
        feedback.append("❌ Password must be at least 12 characters long")
    elif len(password) >= 12:
        score += 20
        feedback.append("✅ Good length")
    
    if len(password) >= 16:
        score += 10
        feedback.append("✅ Excellent length!")
    
    # Uppercase check
    if not re.search(r'[A-Z]', password):
        feedback.append("❌ Must contain at least one uppercase letter")
    else:
        score += 15
        feedback.append("✅ Contains uppercase")
    
    # Lowercase check
    if not re.search(r'[a-z]', password):
        feedback.append("❌ Must contain at least one lowercase letter")
    else:
        score += 15
        feedback.append("✅ Contains lowercase")
    
    # Number check
    if not re.search(r'[0-9]', password):
        feedback.append("❌ Must contain at least one number")
    else:
        score += 15
        feedback.append("✅ Contains number")
    
    # Special character check
    if not re.search(r'[!@#$%^&*(),.?":{}|<>_\-+=\[\]\\\/~`]', password):
        feedback.append("❌ Must contain at least one special character (!@#$%^&*)")
    else:
        score += 15
        feedback.append("✅ Contains special character")
    
    # Common password check
    if password.lower() in common_passwords:
        feedback.append("❌ This is a commonly used password - choose something unique")
        score -= 30
    else:
        score += 10
    
    # Sequential characters check
    if re.search(r'(012|123|234|345|456|567|678|789|890|abc|bcd|cde|def)', password.lower()):
        feedback.append("⚠️ Avoid sequential characters")
        score -= 10
    
    # Repeated characters check
    if re.search(r'(.)\1{2,}', password):
        feedback.append("⚠️ Avoid repeating characters (e.g., aaa, 111)")
        score -= 10
    
    # Ensure score is between 0-100
    score = max(0, min(100, score))
    
    # Determine strength
    if score >= 90:
        strength = "Excellent"
        color = "🟢"
    elif score >= 70:
        strength = "Strong"
        color = "🟢"
    elif score >= 50:
        strength = "Good"
        color = "🟡"
    elif score >= 30:
        strength = "Fair"
        color = "🟠"
    else:
        strength = "Weak"
        color = "🔴"
    
    # Valid if score is at least 70 (Strong)
    valid = score >= 70
    
    return {
        'valid': valid,
        'score': score,
        'feedback': feedback,
        'strength': f"{color} {strength}",
        'color': color
    }


def check_password_age(last_changed_date, max_days=90):
    """
    Check if password needs to be changed
    NHS requirement: Change password every 90 days
    
    Args:
        last_changed_date: datetime when password was last changed
        max_days: maximum days before password expires
    
    Returns:
        dict: {
            'expired': bool,
            'days_remaining': int,
            'message': str
        }
    """
    if not last_changed_date:
        return {
            'expired': True,
            'days_remaining': 0,
            'message': '⚠️ Password has never been changed'
        }
    
    days_since_change = (datetime.now() - last_changed_date).days
    days_remaining = max_days - days_since_change
    
    if days_remaining <= 0:
        return {
            'expired': True,
            'days_remaining': 0,
            'message': f'❌ Password expired {abs(days_remaining)} days ago - change immediately!'
        }
    elif days_remaining <= 7:
        return {
            'expired': False,
            'days_remaining': days_remaining,
            'message': f'⚠️ Password expires in {days_remaining} days - change soon!'
        }
    else:
        return {
            'expired': False,
            'days_remaining': days_remaining,
            'message': f'✅ Password expires in {days_remaining} days'
        }


def check_failed_login_attempts(email, max_attempts=3):
    """
    Track failed login attempts and lock account if needed
    NHS requirement: Lock after 3 failed attempts
    
    This function should be integrated with your user tracking system
    """
    # This will integrate with your existing user_tracking_system
    pass


def generate_strong_password(length=16):
    """
    Generate a strong random password
    Useful for password reset functionality
    """
    import random
    import string
    
    # Ensure we have all required character types
    uppercase = random.choice(string.ascii_uppercase)
    lowercase = random.choice(string.ascii_lowercase)
    digit = random.choice(string.digits)
    special = random.choice('!@#$%^&*')
    
    # Fill the rest randomly
    all_chars = string.ascii_letters + string.digits + '!@#$%^&*'
    remaining = ''.join(random.choice(all_chars) for _ in range(length - 4))
    
    # Combine and shuffle
    password = uppercase + lowercase + digit + special + remaining
    password_list = list(password)
    random.shuffle(password_list)
    
    return ''.join(password_list)


def sanitize_input(user_input):
    """
    Sanitize user input to prevent SQL injection and XSS attacks
    """
    # Remove potentially dangerous characters
    sanitized = user_input.strip()
    
    # Remove HTML tags
    sanitized = re.sub(r'<[^>]*>', '', sanitized)
    
    # Remove SQL injection attempts
    dangerous_patterns = [
        r'(\b(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|EXEC|EXECUTE)\b)',
        r'(--|;|\/\*|\*\/)',
        r'(\bOR\b.*=.*)',
        r'(\bAND\b.*=.*)'
    ]
    
    for pattern in dangerous_patterns:
        if re.search(pattern, sanitized, re.IGNORECASE):
            raise ValueError("⚠️ Invalid input detected - potential security risk")
    
    return sanitized
