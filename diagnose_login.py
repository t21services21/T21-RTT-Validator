"""Diagnose login issue"""
import json
import hashlib

# Load database
with open("users_database.json", 'r') as f:
    users = json.load(f)

student_email = "t.owonifari@t21services.co.uk"

print("=" * 70)
print("LOGIN DIAGNOSIS")
print("=" * 70)

if student_email in users:
    student = users[student_email]
    stored_hash = student["password_hash"]
    
    print(f"Email: {student_email}")
    print(f"Name: {student['full_name']}")
    print(f"\nStored password hash in database:")
    print(stored_hash)
    print()
    
    # Test passwords
    test_passwords = ["Admin123", "admin123", "ADMIN123", "student123"]
    
    print("Testing passwords:")
    print("-" * 70)
    
    for pwd in test_passwords:
        test_hash = hashlib.sha256(pwd.encode()).hexdigest()
        match = "✓ MATCH!" if test_hash == stored_hash else "✗ No match"
        print(f"{pwd:20} -> {match}")
        if test_hash == stored_hash:
            print()
            print("=" * 70)
            print(f"CORRECT PASSWORD IS: {pwd}")
            print("=" * 70)
            break
    else:
        print()
        print("None of the tested passwords match!")
        print("The student needs to tell you what they used during registration.")
        
print("=" * 70)
