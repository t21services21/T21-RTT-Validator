"""
INPUT VALIDATION UTILITIES
Ensures data quality and prevents invalid entries

NHS-Compliant Validation Rules:
- NHS Number: 10 digits with valid checksum
- Patient DOB: Valid date, not in future
- Email: Valid format
- Phone: UK format
- Postcode: UK format
"""

import re
from datetime import datetime, date
from typing import Tuple, Optional

def validate_nhs_number(nhs_number: str) -> Tuple[bool, str]:
    """
    Validate NHS number with checksum algorithm
    
    NHS Number Format: 10 digits (e.g., 123 456 7890)
    Checksum: Modulus 11 algorithm
    
    Returns: (is_valid, error_message)
    """
    if not nhs_number:
        return False, "NHS number is required"
    
    # Remove spaces and hyphens
    cleaned = re.sub(r'[\s-]', '', nhs_number)
    
    # Check length
    if len(cleaned) != 10:
        return False, "NHS number must be exactly 10 digits"
    
    # Check all digits
    if not cleaned.isdigit():
        return False, "NHS number must contain only digits"
    
    # Perform checksum validation (Modulus 11 algorithm)
    try:
        digits = [int(d) for d in cleaned[:9]]
        check_digit = int(cleaned[9])
        
        # Calculate checksum
        total = sum((10 - i) * digit for i, digit in enumerate(digits))
        remainder = total % 11
        calculated_check = 11 - remainder
        
        if calculated_check == 11:
            calculated_check = 0
        
        # Check digit 10 is invalid
        if calculated_check == 10:
            return False, "Invalid NHS number (checksum failed)"
        
        if calculated_check != check_digit:
            return False, "Invalid NHS number (checksum mismatch)"
        
        return True, ""
    
    except Exception as e:
        return False, f"Error validating NHS number: {str(e)}"


def validate_date_of_birth(dob: date) -> Tuple[bool, str]:
    """
    Validate patient date of birth
    
    Rules:
    - Must not be in the future
    - Must be reasonable (not more than 120 years ago)
    - Must be a valid date
    
    Returns: (is_valid, error_message)
    """
    if not dob:
        return False, "Date of birth is required"
    
    today = date.today()
    
    # Check not in future
    if dob > today:
        return False, "Date of birth cannot be in the future"
    
    # Check not more than 120 years ago
    age_years = (today - dob).days / 365.25
    if age_years > 120:
        return False, "Date of birth cannot be more than 120 years ago"
    
    # Check not newborn (should be at least 1 day old for admin purposes)
    if dob == today:
        return False, "Patient must be at least 1 day old"
    
    return True, ""


def validate_email(email: str) -> Tuple[bool, str]:
    """
    Validate email address format
    
    Returns: (is_valid, error_message)
    """
    if not email:
        return False, "Email address is required"
    
    # Basic email regex pattern
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not re.match(pattern, email):
        return False, "Invalid email format (e.g., name@example.com)"
    
    return True, ""


def validate_uk_phone(phone: str) -> Tuple[bool, str]:
    """
    Validate UK phone number
    
    Accepts formats:
    - 01234 567890
    - 07123 456789
    - +44 1234 567890
    - 020 1234 5678 (London)
    
    Returns: (is_valid, error_message)
    """
    if not phone:
        return True, ""  # Phone is optional
    
    # Remove spaces, hyphens, parentheses
    cleaned = re.sub(r'[\s\-()]', '', phone)
    
    # Check if starts with + or 0
    if cleaned.startswith('+44'):
        cleaned = '0' + cleaned[3:]
    
    # UK phone numbers are 10-11 digits starting with 0
    if not cleaned.startswith('0'):
        return False, "UK phone numbers must start with 0 or +44"
    
    if not cleaned.isdigit():
        return False, "Phone number must contain only digits"
    
    if len(cleaned) < 10 or len(cleaned) > 11:
        return False, "UK phone numbers must be 10-11 digits"
    
    return True, ""


def validate_uk_postcode(postcode: str) -> Tuple[bool, str]:
    """
    Validate UK postcode
    
    Formats accepted:
    - SW1A 1AA
    - M1 1AE
    - B33 8TH
    
    Returns: (is_valid, error_message)
    """
    if not postcode:
        return True, ""  # Postcode is optional
    
    # UK postcode regex (simplified)
    pattern = r'^[A-Z]{1,2}\d{1,2}[A-Z]?\s?\d[A-Z]{2}$'
    
    cleaned = postcode.upper().strip()
    
    if not re.match(pattern, cleaned):
        return False, "Invalid UK postcode format (e.g., SW1A 1AA)"
    
    return True, ""


def validate_patient_name(name: str) -> Tuple[bool, str]:
    """
    Validate patient name
    
    Rules:
    - Not empty
    - At least 2 characters
    - Only letters, spaces, hyphens, apostrophes
    
    Returns: (is_valid, error_message)
    """
    if not name:
        return False, "Patient name is required"
    
    if len(name.strip()) < 2:
        return False, "Patient name must be at least 2 characters"
    
    # Allow letters, spaces, hyphens, apostrophes
    pattern = r"^[A-Za-z\s\-']+$"
    
    if not re.match(pattern, name):
        return False, "Patient name can only contain letters, spaces, hyphens, and apostrophes"
    
    return True, ""


def format_nhs_number(nhs_number: str) -> str:
    """Format NHS number as XXX XXX XXXX"""
    cleaned = re.sub(r'[\s-]', '', nhs_number)
    if len(cleaned) == 10:
        return f"{cleaned[:3]} {cleaned[3:6]} {cleaned[6:]}"
    return nhs_number


def format_uk_phone(phone: str) -> str:
    """Format UK phone number nicely"""
    cleaned = re.sub(r'[\s\-()]', '', phone)
    
    if cleaned.startswith('07') and len(cleaned) == 11:
        # Mobile: 07XXX XXXXXX
        return f"{cleaned[:5]} {cleaned[5:]}"
    elif cleaned.startswith('0') and len(cleaned) == 10:
        # Landline: 01XXX XXXXXX
        return f"{cleaned[:5]} {cleaned[5:]}"
    elif cleaned.startswith('0') and len(cleaned) == 11:
        # Landline: 01XX XXX XXXX
        return f"{cleaned[:4]} {cleaned[4:7]} {cleaned[7:]}"
    
    return phone


def format_uk_postcode(postcode: str) -> str:
    """Format UK postcode as XXXX XXX"""
    cleaned = postcode.upper().replace(' ', '')
    if len(cleaned) >= 5:
        return f"{cleaned[:-3]} {cleaned[-3:]}"
    return postcode


# Quick validation function for forms
def validate_patient_data(patient_data: dict) -> Tuple[bool, list]:
    """
    Validate complete patient data
    
    Returns: (is_valid, list_of_errors)
    """
    errors = []
    
    # Validate name
    if 'name' in patient_data:
        is_valid, msg = validate_patient_name(patient_data['name'])
        if not is_valid:
            errors.append(msg)
    
    # Validate NHS number
    if 'nhs_number' in patient_data:
        is_valid, msg = validate_nhs_number(patient_data['nhs_number'])
        if not is_valid:
            errors.append(msg)
    
    # Validate DOB
    if 'dob' in patient_data:
        is_valid, msg = validate_date_of_birth(patient_data['dob'])
        if not is_valid:
            errors.append(msg)
    
    # Validate email
    if 'email' in patient_data and patient_data['email']:
        is_valid, msg = validate_email(patient_data['email'])
        if not is_valid:
            errors.append(msg)
    
    # Validate phone
    if 'phone' in patient_data and patient_data['phone']:
        is_valid, msg = validate_uk_phone(patient_data['phone'])
        if not is_valid:
            errors.append(msg)
    
    # Validate postcode
    if 'postcode' in patient_data and patient_data['postcode']:
        is_valid, msg = validate_uk_postcode(patient_data['postcode'])
        if not is_valid:
            errors.append(msg)
    
    return (len(errors) == 0, errors)


def generate_fake_nhs_number() -> str:
    """
    Generate realistic fake NHS number for training purposes only
    Uses Modulus 11 algorithm to ensure valid checksum
    
    IMPORTANT: For training/simulation ONLY! 
    Real NHS systems MUST use NHS Spine/PDS for real NHS numbers.
    
    Returns: Formatted NHS number (e.g., "123 456 7890")
    """
    import random
    
    # Generate first 9 digits
    first_nine = ''.join([str(random.randint(0, 9)) for _ in range(9)])
    
    # Calculate check digit using Modulus 11 algorithm
    total = 0
    for i, digit in enumerate(first_nine):
        multiplier = 10 - i
        total += int(digit) * multiplier
    
    remainder = total % 11
    check_digit = 11 - remainder
    
    # Handle special cases
    if check_digit == 11:
        check_digit = 0
    elif check_digit == 10:
        # Invalid - regenerate
        return generate_fake_nhs_number()
    
    # Create full NHS number
    nhs_number = first_nine + str(check_digit)
    
    # Format as "123 456 7890"
    return format_nhs_number(nhs_number)


def is_training_mode(user_role: str) -> bool:
    """
    Determine if user is in training mode
    
    Training roles: student, learner, trial
    Real roles: nhs_staff, nhs_coordinator, admin
    """
    training_roles = ['student', 'learner', 'trial', 'teacher']
    return user_role.lower() in training_roles


# Export all validation functions
__all__ = [
    'validate_nhs_number',
    'validate_date_of_birth',
    'validate_email',
    'validate_uk_phone',
    'validate_uk_postcode',
    'validate_patient_name',
    'format_nhs_number',
    'format_uk_phone',
    'format_uk_postcode',
    'validate_patient_data',
    'generate_fake_nhs_number',  # NEW!
    'is_training_mode'  # NEW!
]
