"""
MINIMAL IMPORTS FOR APP.PY - CRITICAL FIX
Replace lines 54-500 in app.py with THIS to fix "Too many open files" error

This keeps only ESSENTIAL imports at the top.
All other imports moved into their usage blocks (lazy loading).
"""

import streamlit as st
import json
import os
from datetime import datetime

# Browser history (optional)
try:
    from browser_history_handler import setup_history_listener, navigate_with_history
    BROWSER_HISTORY_ENABLED = True
except:
    BROWSER_HISTORY_ENABLED = False

# THAT'S IT! Only 6 imports at the top!
# All other imports will be lazy-loaded when actually needed

# Helper function for lazy imports
def safe_import(module_name, function_name=None):
    """Safely import a module/function at runtime"""
    try:
        if function_name:
            module = __import__(module_name, fromlist=[function_name])
            return getattr(module, function_name)
        else:
            return __import__(module_name)
    except Exception as e:
        print(f"Failed to import {module_name}: {e}")
        return None
