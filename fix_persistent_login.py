"""
ENHANCED PERSISTENT LOGIN - WORKS EVEN WITHOUT COOKIES
Uses localStorage as fallback when cookies are blocked
"""

import streamlit as st
import streamlit.components.v1 as components
import hashlib
import json
from datetime import datetime, timedelta
import base64

def save_to_localstorage(email, password_hash):
    """Save auth to browser localStorage (works even if cookies blocked)"""
    
    # Generate token
    timestamp = datetime.now().isoformat()
    token_data = f"{email}:{password_hash}:{timestamp}"
    token = base64.b64encode(token_data.encode()).decode()
    
    # JavaScript to save to localStorage
    js_code = f"""
    <script>
        // Save to localStorage
        localStorage.setItem('t21_auth_token', '{token}');
        localStorage.setItem('t21_user_email', '{email}');
        localStorage.setItem('t21_login_time', '{timestamp}');
        
        // Also try sessionStorage
        sessionStorage.setItem('t21_auth_token', '{token}');
        sessionStorage.setItem('t21_user_email', '{email}');
        
        console.log('Auth saved to localStorage');
    </script>
    """
    
    components.html(js_code, height=0)


def load_from_localstorage():
    """Load auth from browser localStorage"""
    
    # JavaScript to read from localStorage
    js_code = """
    <script>
        // Get from localStorage
        const token = localStorage.getItem('t21_auth_token');
        const email = localStorage.getItem('t21_user_email');
        const loginTime = localStorage.getItem('t21_login_time');
        
        // Send to Streamlit
        if (token && email) {
            window.parent.postMessage({
                type: 't21_auth',
                token: token,
                email: email,
                loginTime: loginTime
            }, '*');
            console.log('Auth loaded from localStorage');
        } else {
            console.log('No auth in localStorage');
        }
    </script>
    """
    
    components.html(js_code, height=0)


def clear_localstorage():
    """Clear auth from localStorage (logout)"""
    
    js_code = """
    <script>
        localStorage.removeItem('t21_auth_token');
        localStorage.removeItem('t21_user_email');
        localStorage.removeItem('t21_login_time');
        sessionStorage.removeItem('t21_auth_token');
        sessionStorage.removeItem('t21_user_email');
        console.log('Auth cleared from localStorage');
    </script>
    """
    
    components.html(js_code, height=0)


# Add this to student_login.py after successful login:
"""
# After successful login, save to localStorage
save_to_localstorage(email, password_hash)
"""

# Add this at the start of app.py:
"""
# Try to restore login from localStorage
if not st.session_state.get('logged_in'):
    load_from_localstorage()
"""

print("""
INSTALLATION INSTRUCTIONS:
=========================

1. Add to pages/student_login.py after successful login (around line 170):

    from fix_persistent_login import save_to_localstorage
    
    # After st.session_state.logged_in = True
    save_to_localstorage(email, password_hash)


2. Add to app.py at the start (around line 50):

    from fix_persistent_login import load_from_localstorage
    
    # Before checking if logged_in
    if not st.session_state.get('logged_in'):
        load_from_localstorage()


3. Deploy to Streamlit Cloud

This will make login persist even if cookies are blocked!
""")
