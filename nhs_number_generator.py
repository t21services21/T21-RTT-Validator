"""
NHS NUMBER GENERATOR
Generates valid 10-digit NHS numbers with check digit
"""

import random
from datetime import datetime


def calculate_nhs_check_digit(first_nine_digits):
    """
    Calculate NHS number check digit using modulus 11 algorithm
    
    NHS number format: ABC DEF GHI J
    Where J is the check digit
    
    Algorithm:
    1. Multiply each of the first 9 digits by (11 - position)
    2. Add all the results
    3. Divide by 11 and get remainder
    4. Subtract remainder from 11 = check digit
    5. If check digit is 11, use 0. If 10, number is invalid
    """
    
    # Weights: position 1=11, 2=10, 3=9, etc.
    weights = [11, 10, 9, 8, 7, 6, 5, 4, 3]
    
    # Calculate weighted sum
    total = sum(int(digit) * weight for digit, weight in zip(first_nine_digits, weights))
    
    # Calculate check digit
    remainder = total % 11
    check_digit = 11 - remainder
    
    # Handle special cases
    if check_digit == 11:
        check_digit = 0
    elif check_digit == 10:
        # Invalid - need to generate new first 9 digits
        return None
    
    return check_digit


def generate_nhs_number():
    """
    Generate a valid NHS number
    Returns: String in format "123 456 7890"
    """
    
    max_attempts = 100
    
    for _ in range(max_attempts):
        # Generate first 9 digits
        # First digit should not be 0
        first_digit = random.randint(1, 9)
        other_digits = ''.join([str(random.randint(0, 9)) for _ in range(8)])
        first_nine = str(first_digit) + other_digits
        
        # Calculate check digit
        check_digit = calculate_nhs_check_digit(first_nine)
        
        if check_digit is not None:
            # Valid NHS number
            nhs_number = first_nine + str(check_digit)
            
            # Format with spaces: 123 456 7890
            formatted = f"{nhs_number[:3]} {nhs_number[3:6]} {nhs_number[6:]}"
            
            return formatted
    
    # Fallback if we couldn't generate valid number
    return "999 999 9999"


def validate_nhs_number(nhs_number):
    """
    Validate an NHS number
    Returns: (is_valid: bool, message: str)
    """
    
    # Remove spaces and dashes
    clean = nhs_number.replace(' ', '').replace('-', '')
    
    # Must be 10 digits
    if len(clean) != 10:
        return False, "NHS number must be 10 digits"
    
    if not clean.isdigit():
        return False, "NHS number must contain only digits"
    
    # Check digit validation
    first_nine = clean[:9]
    provided_check = int(clean[9])
    
    calculated_check = calculate_nhs_check_digit(first_nine)
    
    if calculated_check is None:
        return False, "Invalid NHS number (check digit cannot be calculated)"
    
    if calculated_check != provided_check:
        return False, f"Invalid check digit (expected {calculated_check}, got {provided_check})"
    
    return True, "Valid NHS number"


def format_nhs_number(nhs_number):
    """
    Format NHS number with spaces: 123 456 7890
    """
    clean = nhs_number.replace(' ', '').replace('-', '')
    
    if len(clean) == 10:
        return f"{clean[:3]} {clean[3:6]} {clean[6:]}"
    
    return nhs_number


def generate_batch_nhs_numbers(count=100):
    """
    Generate a batch of unique NHS numbers
    Returns: List of NHS numbers
    """
    nhs_numbers = set()
    
    while len(nhs_numbers) < count:
        nhs_num = generate_nhs_number()
        nhs_numbers.add(nhs_num)
    
    return sorted(list(nhs_numbers))


# Test the generator
if __name__ == "__main__":
    print("=" * 70)
    print("NHS NUMBER GENERATOR TEST")
    print("=" * 70)
    
    # Generate 10 NHS numbers
    print("\nGenerating 10 valid NHS numbers:")
    for i in range(10):
        nhs_num = generate_nhs_number()
        is_valid, msg = validate_nhs_number(nhs_num)
        status = "✅" if is_valid else "❌"
        print(f"{i+1}. {nhs_num} {status} {msg}")
    
    # Test validation
    print("\n" + "=" * 70)
    print("VALIDATION TESTS")
    print("=" * 70)
    
    test_numbers = [
        "123 456 7890",  # Will check if valid
        "999 999 9999",  # Will check if valid
        "111 111 1116",  # Known valid format
        "12345",  # Too short
        "abc def ghij",  # Non-numeric
    ]
    
    for test_num in test_numbers:
        is_valid, msg = validate_nhs_number(test_num)
        status = "✅" if is_valid else "❌"
        print(f"{status} {test_num}: {msg}")
    
    print("\n" + "=" * 70)
