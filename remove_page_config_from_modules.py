"""
CRITICAL FIX: Remove st.set_page_config from all module pages
This is causing silent crashes when navigating via st.switch_page()
"""

import os
import re

def fix_module(filepath):
    """Remove st.set_page_config from a module file"""
    
    if not os.path.exists(filepath):
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if has set_page_config
    if 'st.set_page_config' not in content:
        print(f"[SKIP] {os.path.basename(filepath)} - no page config")
        return False
    
    # Remove the entire st.set_page_config line(s)
    # It can be single line or multi-line
    content = re.sub(
        r'st\.set_page_config\([^)]*\)\n?',
        '',
        content
    )
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"[OK] Fixed: {os.path.basename(filepath)}")
    return True

if __name__ == "__main__":
    print("Removing st.set_page_config from all modules...")
    print("=" * 50)
    
    # Get all Python files in pages directory
    pages_dir = 'pages'
    fixed_count = 0
    
    for filename in os.listdir(pages_dir):
        if filename.endswith('.py'):
            filepath = os.path.join(pages_dir, filename)
            if fix_module(filepath):
                fixed_count += 1
    
    print("=" * 50)
    print(f"Complete! Fixed {fixed_count} files")
    print("\nPages will now load correctly via st.switch_page()!")
