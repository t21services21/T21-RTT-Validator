"""
Check all users in all database files
"""
import json
import os

print("=" * 80)
print("CHECKING ALL USER DATABASES")
print("=" * 80)

# Check users_database.json (OLD database)
print("\n1. USERS_DATABASE.JSON (Old/Legacy Database)")
print("-" * 80)
if os.path.exists("users_database.json"):
    with open("users_database.json", 'r') as f:
        old_users = json.load(f)
    print(f"Total users: {len(old_users)}")
    print("\nUser List:")
    for i, (email, data) in enumerate(old_users.items(), 1):
        name = data.get("full_name", "Unknown")
        role = data.get("license", {}).get("role", "unknown")
        print(f"{i:2d}. {email:40s} | {name:30s} | {role}")
else:
    print("FILE NOT FOUND!")

# Check users_advanced.json (NEW database)
print("\n\n2. USERS_ADVANCED.JSON (New Advanced Database)")
print("-" * 80)
if os.path.exists("users_advanced.json"):
    with open("users_advanced.json", 'r') as f:
        new_users = json.load(f)
    print(f"Total users: {len(new_users)}")
    print("\nUser List:")
    for i, (email, data) in enumerate(new_users.items(), 1):
        name = data.get("full_name", "Unknown")
        role = data.get("role", "unknown")
        print(f"{i:2d}. {email:40s} | {name:30s} | {role}")
else:
    print("FILE NOT FOUND!")

# Check for students.json (if it exists)
print("\n\n3. STUDENTS.JSON (If exists)")
print("-" * 80)
if os.path.exists("students.json"):
    with open("students.json", 'r') as f:
        students = json.load(f)
    print(f"Total students: {len(students)}")
    print("\nStudent List:")
    for i, (email, data) in enumerate(students.items(), 1):
        name = data.get("full_name", "Unknown")
        role = data.get("role", "unknown")
        print(f"{i:2d}. {email:40s} | {name:30s} | {role}")
else:
    print("FILE NOT FOUND!")

# Check validation history for registered users
print("\n\n4. VALIDATION_HISTORY.JSON (Check for user activity)")
print("-" * 80)
if os.path.exists("validation_history.json"):
    with open("validation_history.json", 'r') as f:
        history = json.load(f)
    unique_users = set()
    for record in history:
        if "user_email" in record:
            unique_users.add(record["user_email"])
    print(f"Unique users with activity: {len(unique_users)}")
    if unique_users:
        print("\nActive users:")
        for i, email in enumerate(sorted(unique_users), 1):
            print(f"{i:2d}. {email}")
else:
    print("FILE NOT FOUND!")

# Summary
print("\n\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
total_old = len(old_users) if os.path.exists("users_database.json") else 0
total_new = len(new_users) if os.path.exists("users_advanced.json") else 0
print(f"users_database.json (old):     {total_old} users")
print(f"users_advanced.json (new):     {total_new} users")
print(f"TOTAL UNIQUE USERS:            {total_old + total_new - len(set(old_users.keys()) & set(new_users.keys())) if total_old and total_new else total_old + total_new} users")
print("=" * 80)

# Check for duplicates
if total_old and total_new:
    duplicates = set(old_users.keys()) & set(new_users.keys())
    if duplicates:
        print(f"\nWARNING: {len(duplicates)} users exist in BOTH databases:")
        for email in duplicates:
            print(f"  - {email}")
