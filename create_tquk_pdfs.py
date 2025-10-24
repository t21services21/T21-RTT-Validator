"""
TQUK PDF CREATOR
Automatically creates PDFs with T21 Services branding for TQUK submission
"""

import os
from pathlib import Path

# Company branding
HEADER = """
================================================================================

                            T21 SERVICES LIMITED
                    Company Number: 13091053
                    TQUK Approved Centre #36257481088
                Level 3 Diploma in Adult Care (RQF) - 610/0103/6

================================================================================

REGISTERED OFFICE:
T21 SERVICES LIMITED
64 Upper Parliament Street
Liverpool
L8 7LF
United Kingdom

CONTACT DETAILS:
📧 Email: t.owonifari@t21services.co.uk
📞 Phone: 07447459420
🌐 Website: www.t21services.co.uk

CENTRE INFORMATION:
Centre Number: 36257481088
Centre Manager: H.E. Ambassador Tosin Michael Owonifari
Awarding Organization: TQUK (Training Qualifications UK)
Qualification: Level 3 Diploma in Adult Care (RQF)
Qualification Code: 610/0103/6

================================================================================

"""

FOOTER = """

================================================================================

T21 SERVICES LIMITED | TQUK Centre #36257481088
📧 t.owonifari@t21services.co.uk | 📞 07447459420
Level 3 Diploma in Adult Care (RQF) - 610/0103/6

© 2025 T21 SERVICES LIMITED. All Rights Reserved.
Company Number: 13091053
This document is the property of T21 SERVICES LIMITED and may not be 
reproduced without permission.

================================================================================
"""

# Files to process for TQUK submission
TQUK_FILES = [
    "TQUK_CDA_SUBMISSION_PACKAGE.md",
    "EMAIL_TO_TQUK_CDA_APPROVAL.md",
    "LEVEL3_UNIT1_DUTY_OF_CARE_COMPLETE.md",
    "LEVEL3_UNIT2_EQUALITY_DIVERSITY_COMPLETE.md",
    "LEVEL3_UNIT3_PERSON_CENTRED_CARE_COMPLETE.md",
    "LEVEL3_ASSESSMENT_PACK_TEMPLATES.md"
]


def create_branded_files():
    """Create branded versions of all TQUK files"""
    
    # Get current directory
    current_dir = Path(__file__).parent
    
    # Create output directory on Desktop
    desktop = Path.home() / "Desktop"
    output_dir = desktop / "TQUK_Submission_Documents"
    output_dir.mkdir(exist_ok=True)
    
    print(f"\n{'='*80}")
    print("T21 SERVICES - TQUK DOCUMENT CREATOR")
    print(f"{'='*80}\n")
    
    created_files = []
    missing_files = []
    
    for filename in TQUK_FILES:
        file_path = current_dir / filename
        
        if file_path.exists():
            print(f"✅ Processing: {filename}")
            
            # Read original content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Add branding
            branded_content = HEADER + content + FOOTER
            
            # Create output filename
            output_filename = filename.replace('.md', '_OFFICIAL.txt')
            output_path = output_dir / output_filename
            
            # Write branded version
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(branded_content)
            
            created_files.append(output_filename)
            print(f"   ✓ Created: {output_filename}")
        else:
            print(f"❌ Missing: {filename}")
            missing_files.append(filename)
    
    print(f"\n{'='*80}")
    print("SUMMARY")
    print(f"{'='*80}\n")
    
    print(f"✅ Created {len(created_files)} files")
    print(f"📁 Location: {output_dir}\n")
    
    if created_files:
        print("Files created:")
        for f in created_files:
            print(f"  • {f}")
    
    if missing_files:
        print(f"\n⚠️  Missing {len(missing_files)} files:")
        for f in missing_files:
            print(f"  • {f}")
    
    print(f"\n{'='*80}")
    print("NEXT STEPS:")
    print(f"{'='*80}\n")
    print("1. Go to your Desktop")
    print("2. Open folder: TQUK_Submission_Documents")
    print("3. Open each .txt file in Microsoft Word")
    print("4. File → Save As → PDF")
    print("5. Email PDFs to: support@tquk.org")
    print(f"\n{'='*80}\n")


if __name__ == "__main__":
    try:
        create_branded_files()
        input("\nPress Enter to close...")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        input("\nPress Enter to close...")
