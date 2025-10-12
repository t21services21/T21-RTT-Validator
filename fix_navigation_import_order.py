"""
CRITICAL FIX: Move parent path addition BEFORE navigation import
The navigation.py import was failing because parent dir wasn't in path yet!
"""

import os
import re

def fix_module(filepath):
    """Fix import order in a module file"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if has navigation import
    if 'from navigation import' not in content:
        return False
    
    # Pattern: Find the navigation import line
    nav_import_pattern = r'from navigation import render_navigation\n'
    
    # Pattern: Find the parent_dir setup
    parent_dir_pattern = r'# Add parent directory to path.*?\n.*?parent_dir = .*?\n.*?if parent_dir not in sys\.path:.*?\n.*?sys\.path\.insert.*?\n'
    
    # Check if navigation import comes BEFORE parent_dir setup
    nav_match = re.search(nav_import_pattern, content)
    parent_match = re.search(parent_dir_pattern, content, re.DOTALL)
    
    if not nav_match or not parent_match:
        return False
    
    # If navigation import is BEFORE parent setup, we need to fix it
    if nav_match.start() < parent_match.start():
        # Remove navigation import from its current location
        content = re.sub(nav_import_pattern, '', content)
        
        # Add it AFTER the parent_dir setup
        parent_end = parent_match.end()
        content = content[:parent_end] + '\nfrom navigation import render_navigation\n' + content[parent_end:]
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"[OK] Fixed: {os.path.basename(filepath)}")
        return True
    
    return False

if __name__ == "__main__":
    print("Fixing navigation import order in all modules...")
    print("=" * 50)
    
    pages_dir = 'pages'
    fixed_count = 0
    
    for filename in os.listdir(pages_dir):
        if filename.endswith('.py'):
            filepath = os.path.join(pages_dir, filename)
            if fix_module(filepath):
                fixed_count += 1
    
    print("=" * 50)
    print(f"Complete! Fixed {fixed_count} files")
