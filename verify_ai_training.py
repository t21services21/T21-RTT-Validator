"""
VERIFY AI TRAINING SYSTEM
Quick script to check if AI Training system is properly set up
"""

import os
import sys

print("=" * 60)
print("AI TRAINING SYSTEM VERIFICATION")
print("=" * 60)

# Check required files
required_files = [
    "admin_ai_training.py",
    "ai_knowledge_base.py",
    "document_processor.py"
]

print("\n1. CHECKING REQUIRED FILES:")
all_files_exist = True
for file in required_files:
    exists = os.path.exists(file)
    status = "✅" if exists else "❌"
    print(f"   {status} {file}")
    if not exists:
        all_files_exist = False

# Check if imported in app.py
print("\n2. CHECKING app.py INTEGRATION:")
try:
    with open("app.py", "r", encoding="utf-8") as f:
        app_content = f.read()
    
    checks = [
        ("from admin_ai_training import", "Import statement"),
        ("render_ai_training_admin", "Render function"),
        ('"🤖 AI Training"', "Tab in Admin Panel"),
        ("with admin_tab9:", "Tab rendering")
    ]
    
    for check_text, description in checks:
        found = check_text in app_content
        status = "✅" if found else "❌"
        print(f"   {status} {description}")
except Exception as e:
    print(f"   ❌ Error reading app.py: {e}")

# Summary
print("\n" + "=" * 60)
if all_files_exist:
    print("✅ ALL FILES PRESENT")
    print("\n📍 TO ACCESS AI TRAINING:")
    print("   1. Login as ADMIN")
    print("   2. Go to '🔧 Admin Panel' in sidebar")
    print("   3. Click Tab 9: '🤖 AI Training'")
else:
    print("❌ MISSING FILES - Deploy all files first!")

print("=" * 60)
