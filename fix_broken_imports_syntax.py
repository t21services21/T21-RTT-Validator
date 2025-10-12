"""
FIX BROKEN IMPORTS - The navigation import got mixed into universal_crud import!
"""

import os
import re

def fix_module(filepath):
    """Fix broken import syntax"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to find the broken import
    # Looking for: from universal_crud import ( ... from navigation ... )
    broken_pattern = r'from universal_crud import \(\s*create_\s*from navigation import render_navigation\s*record,'
    
    if re.search(broken_pattern, content):
        # Fix the broken import
        content = re.sub(
            r'from universal_crud import \(\s*create_\s*from navigation import render_navigation\s*record, read_all_records.*?\)',
            '''from navigation import render_navigation
from universal_crud import (
    create_record, read_all_records, read_record_by_id,
    update_record, delete_record, search_records, export_to_csv
)''',
            content,
            flags=re.DOTALL
        )
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"[OK] Fixed: {os.path.basename(filepath)}")
        return True
    
    return False

if __name__ == "__main__":
    print("Fixing broken import syntax in all modules...")
    print("=" * 50)
    
    fixed_count = 0
    for filename in os.listdir('pages'):
        if filename.endswith('.py'):
            filepath = os.path.join('pages', filename)
            if fix_module(filepath):
                fixed_count += 1
    
    print("=" * 50)
    print(f"Fixed {fixed_count} files")
