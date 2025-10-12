"""
TEST PAGE - Simple test to see if imports work
"""

import streamlit as st

st.set_page_config(page_title="Test CRUD", page_icon="🧪", layout="wide")

st.title("🧪 CRUD Import Test")

# Test 1: Basic imports
st.markdown("## Test 1: Basic Imports")
try:
    import os
    import sys
    st.success("✅ os and sys imported successfully")
except Exception as e:
    st.error(f"❌ Error importing os/sys: {e}")

# Test 2: Parent directory path
st.markdown("## Test 2: Path Resolution")
try:
    import os
    current_file = os.path.abspath(__file__)
    st.info(f"Current file: {current_file}")
    
    parent_dir = os.path.dirname(os.path.dirname(current_file))
    st.info(f"Parent directory: {parent_dir}")
    
    import sys
    st.info(f"sys.path: {sys.path[:3]}...")  # Show first 3 paths
    
    st.success("✅ Path resolution works")
except Exception as e:
    st.error(f"❌ Error with paths: {e}")

# Test 3: Import universal_crud
st.markdown("## Test 3: Import Universal CRUD")
try:
    import os
    import sys
    
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)
    
    from universal_crud import read_all_records
    st.success("✅ universal_crud imported successfully!")
    
    # Test function call
    records = read_all_records('test_module')
    st.info(f"read_all_records() returned: {records}")
    st.success("✅ CRUD functions work!")
    
except ImportError as e:
    st.error(f"❌ ImportError: {e}")
    st.info("universal_crud.py might not be in the right location")
except Exception as e:
    st.error(f"❌ Error: {e}")
    import traceback
    st.code(traceback.format_exc())

# Test 4: Check if universal_crud.py exists
st.markdown("## Test 4: File Existence Check")
try:
    import os
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    crud_file = os.path.join(parent_dir, 'universal_crud.py')
    
    if os.path.exists(crud_file):
        st.success(f"✅ universal_crud.py found at: {crud_file}")
        
        # Show file size
        size = os.path.getsize(crud_file)
        st.info(f"File size: {size} bytes")
    else:
        st.error(f"❌ universal_crud.py NOT FOUND at: {crud_file}")
        
        # List what IS in parent directory
        files = os.listdir(parent_dir)
        st.warning(f"Files in parent directory: {files[:10]}")  # Show first 10
        
except Exception as e:
    st.error(f"❌ Error checking file: {e}")

st.markdown("---")
st.markdown("### 📋 Diagnosis")
st.info("""
If all tests pass ✅: The CRUD system is working, issue is elsewhere
If Test 3 fails ❌: Import path problem
If Test 4 fails ❌: universal_crud.py not deployed to Streamlit Cloud
""")
