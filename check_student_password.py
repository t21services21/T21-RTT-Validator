"""Check student password"""
import json
import hashlib

# Load database
with open("users_database.json", 'r') as f:
    users = json.load(f)

student_email = "t.owonifari@t21services.co.uk"

if student_email in users:
    student = users[student_email]
    stored_hash = student["password_hash"]
    
    print("=" * 60)
    print("STUDENT PASSWORD CHECK")
    print("=" * 60)
    print(f"Email: {student_email}")
    print(f"Name: {student['full_name']}")
    print(f"Stored password hash: {stored_hash}")
    print()
    print("Try these common passwords:")
    print()
    
    # Test common passwords
    test_passwords = [
        "Admin123",
        "admin123",
        "ADMIN123",
        "password",
        "Password123",
        "owonifari",
        "Owonifari",
        "OWONIFARI",
        "tosin",
        "Tosin"
    ]
    
    for pwd in test_passwords:
        test_hash = hashlib.sha256(pwd.encode()).hexdigest()
        if test_hash == stored_hash:
            print(f"[MATCH] Password is: {pwd}")
            print("=" * 60)
            break
    else:
        print("[NOT FOUND] Password not in common list")
        print()
        print("Student needs to register again with a simple password")
        print("=" * 60)
else:
    print(f"Student {student_email} not found in database!")
