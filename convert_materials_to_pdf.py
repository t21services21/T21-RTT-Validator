"""
CONVERT ALL LEVEL 3 MATERIALS TO PDF
Simple script to convert markdown files to PDF for printing and TQUK submission
"""

import os
import subprocess

# List of files to convert
files_to_convert = [
    "LEVEL3_ADULT_CARE_LEARNER_HANDBOOK.md",
    "LEVEL3_UNIT1_DUTY_OF_CARE_COMPLETE.md",
    "LEVEL3_UNIT2_EQUALITY_DIVERSITY_COMPLETE.md",
    "LEVEL3_UNIT3_PERSON_CENTRED_CARE_COMPLETE.md",
    "LEVEL3_ASSESSMENT_PACK_TEMPLATES.md",
    "LEVEL3_COMPLETE_DELIVERY_PACKAGE.md",
    "TQUK_CDA_SUBMISSION_PACKAGE.md",
    "EMAIL_TO_TQUK_CDA_APPROVAL.md"
]

# Create output folder
output_folder = "LEVEL3_PDF_MATERIALS"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

print("=" * 60)
print("CONVERTING LEVEL 3 MATERIALS TO PDF")
print("=" * 60)
print()

# Method 1: Using markdown-pdf (if installed)
print("Attempting to convert using markdown-pdf...")
print()

for file in files_to_convert:
    if os.path.exists(file):
        output_file = os.path.join(output_folder, file.replace('.md', '.pdf'))
        print(f"Converting: {file}")
        
        try:
            # Try using markdown-pdf
            subprocess.run(['markdown-pdf', file, '-o', output_file], check=True)
            print(f"✅ Success: {output_file}")
        except:
            print(f"⚠️  markdown-pdf not installed. Please use manual method below.")
            break
        print()

print()
print("=" * 60)
print("MANUAL CONVERSION INSTRUCTIONS")
print("=" * 60)
print()
print("If automatic conversion didn't work, follow these steps:")
print()
print("METHOD 1: Using VS Code")
print("-" * 60)
print("1. Install 'Markdown PDF' extension in VS Code")
print("2. Open each .md file")
print("3. Right-click → 'Markdown PDF: Export (pdf)'")
print("4. Save to LEVEL3_PDF_MATERIALS folder")
print()
print("METHOD 2: Using Online Converter")
print("-" * 60)
print("1. Go to: https://www.markdowntopdf.com/")
print("2. Upload each .md file")
print("3. Download PDF")
print("4. Save to LEVEL3_PDF_MATERIALS folder")
print()
print("METHOD 3: Using Browser")
print("-" * 60)
print("1. Open each .md file in VS Code")
print("2. Click 'Open Preview' (Ctrl+Shift+V)")
print("3. Right-click preview → 'Print'")
print("4. Choose 'Save as PDF'")
print("5. Save to LEVEL3_PDF_MATERIALS folder")
print()
print("=" * 60)
print("FILES TO CONVERT:")
print("=" * 60)
for i, file in enumerate(files_to_convert, 1):
    print(f"{i}. {file}")
print()
print("=" * 60)
print("AFTER CONVERSION:")
print("=" * 60)
print("1. Check LEVEL3_PDF_MATERIALS folder")
print("2. You should have 8 PDF files")
print("3. Email them to: support@tquk.org")
print("4. Print copies for your learner")
print()
print("✅ ALL MATERIALS ARE READY!")
print("=" * 60)
