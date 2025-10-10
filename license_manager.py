"""
T21 LICENSE MANAGER
Generate and validate license keys
"""

import random
import string
import hashlib
from datetime import datetime

def generate_license_key():
    """
    Generate a unique license key
    Format: XXXX-XXXX-XXXX-XXXX
    """
    segments = []
    for _ in range(4):
        segment = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        segments.append(segment)
    
    return '-'.join(segments)


def validate_license_key(key):
    """
    Validate license key format
    Returns: True if valid format, False otherwise
    """
    if not key:
        return False
    
    # Check format: XXXX-XXXX-XXXX-XXXX
    parts = key.split('-')
    if len(parts) != 4:
        return False
    
    for part in parts:
        if len(part) != 4:
            return False
        if not all(c in string.ascii_uppercase + string.digits for c in part):
            return False
    
    return True


def generate_license_batch(count=10, role="tier1"):
    """
    Generate multiple license keys for a specific tier
    
    Args:
        count: Number of licenses to generate
        role: License tier (tier1, tier2, tier3, taster)
    
    Returns:
        List of license keys
    """
    licenses = []
    for _ in range(count):
        key = generate_license_key()
        licenses.append({
            'key': key,
            'role': role,
            'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'status': 'unused'
        })
    
    return licenses


if __name__ == "__main__":
    # Test license generation
    print("Testing License Manager")
    print("="*50)
    
    # Generate single key
    key = generate_license_key()
    print(f"Generated Key: {key}")
    print(f"Valid: {validate_license_key(key)}")
    
    # Generate batch
    print("\nGenerating 5 Tier 2 licenses:")
    batch = generate_license_batch(5, "tier2")
    for lic in batch:
        print(f"  {lic['key']} - {lic['role']}")
