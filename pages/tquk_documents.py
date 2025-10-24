"""
TQUK Document Library - Page Version
Accessible directly from pages menu
"""

import streamlit as st
import sys
from pathlib import Path

# Add parent directory to path to import modules
parent_dir = str(Path(__file__).parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Import the document library
from tquk_document_library import render_tquk_documents

# Page config
st.set_page_config(
    page_title="TQUK Documents",
    page_icon="📚",
    layout="wide"
)

# Render the document library
render_tquk_documents()
