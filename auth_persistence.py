"""
T21 PERSISTENT AUTHENTICATION
Keeps users logged in across page refreshes using secure cookies
"""

import streamlit as st
import hashlib
import json
from datetime import datetime, timedelta
import base64

try:
    import extra_streamlit_components as stx
    COOKIES_AVAILABLE = True
except ImportError:
    COOKIES_AVAILABLE = False
    print("⚠️ Install extra-streamlit-components for persistent login: pip install extra-streamlit-components")


def get_cookie_manager():
    """
    Get cookie manager instance (singleton pattern)
    Creates only once per session to avoid duplicate key errors
    """
    if not COOKIES_AVAILABLE:
        return None
    
    # Use session state to ensure only one instance
    if '_cookie_manager' not in st.session_state:
        try:
            st.session_state._cookie_manager = stx.CookieManager(key='t21_cookie_manager')
        except Exception as e:
            print(f"Cookie manager initialization error: {e}")
            st.session_state._cookie_manager = None
    
    return st.session_state._cookie_manager


def generate_auth_token(email: str, password_hash: str) -> str:
    """
    Generate secure authentication token
    """
    timestamp = datetime.now().isoformat()
    token_data = f"{email}:{password_hash}:{timestamp}"
    token = base64.b64encode(token_data.encode()).decode()
    return token


def verify_auth_token(token: str) -> dict:
    """
    Verify and decode authentication token
    Returns user data if valid, None if invalid
    """
    try:
        decoded = base64.b64decode(token.encode()).decode()
        parts = decoded.split(':')
        
        if len(parts) != 3:
            return None
        
        email, password_hash, timestamp = parts
        
        # Check token age (expire after 30 days)
        token_time = datetime.fromisoformat(timestamp)
        if datetime.now() - token_time > timedelta(days=30):
            return None
        
        return {
            'email': email,
            'password_hash': password_hash,
            'timestamp': timestamp
        }
    except:
        return None


def save_auth_cookie(email: str, password_hash: str, user_data: dict):
    """
    Save authentication to browser cookie
    """
    cookie_manager = get_cookie_manager()
    
    if not cookie_manager:
        return False
    
    try:
        # Generate secure token
        token = generate_auth_token(email, password_hash)
        
        # Store in cookie (expires in 30 days)
        cookie_manager.set(
            cookie='t21_auth_token',
            val=token,
            expires_at=datetime.now() + timedelta(days=30)
        )
        
        # Store user info separately (for display)
        user_info = {
            'email': email,
            'full_name': user_data.get('full_name', email),
            'user_type': user_data.get('user_type', 'student'),
            'role': user_data.get('role', 'student')
        }
        
        cookie_manager.set(
            cookie='t21_user_info',
            val=json.dumps(user_info),
            expires_at=datetime.now() + timedelta(days=30)
        )
        
        return True
    except Exception as e:
        print(f"Cookie save error: {e}")
        return False


def load_auth_from_cookie():
    """
    Load authentication from browser cookie
    Returns user data if valid session exists, None otherwise
    """
    cookie_manager = get_cookie_manager()
    
    if not cookie_manager:
        return None
    
    try:
        # Get auth token
        cookies = cookie_manager.get_all()
        token = cookies.get('t21_auth_token')
        
        if not token:
            return None
        
        # Verify token
        token_data = verify_auth_token(token)
        
        if not token_data:
            # Invalid token - clear cookies
            clear_auth_cookie()
            return None
        
        # Get user info
        user_info_str = cookies.get('t21_user_info')
        if user_info_str:
            user_info = json.loads(user_info_str)
        else:
            user_info = {'email': token_data['email']}
        
        # Verify password hash is still valid
        email = token_data['email']
        password_hash = token_data['password_hash']
        
        # Try Supabase verification
        try:
            from supabase_database import get_user_by_email
            supabase_user = get_user_by_email(email)
            
            if supabase_user and supabase_user.get('password_hash') == password_hash:
                return supabase_user
        except:
            pass
        
        # Try local JSON verification
        try:
            from admin_management import load_users_db
            users_db = load_users_db()
            
            if email in users_db:
                user_data = users_db[email]
                
                # Handle both dict and UserAccount object
                if hasattr(user_data, 'password_hash'):
                    stored_hash = user_data.password_hash
                elif isinstance(user_data, dict):
                    stored_hash = user_data.get('password_hash')
                else:
                    return None
                
                if stored_hash == password_hash:
                    return user_data
        except:
            pass
        
        # Invalid credentials - clear cookie
        clear_auth_cookie()
        return None
        
    except Exception as e:
        print(f"Cookie load error: {e}")
        return None


def clear_auth_cookie():
    """
    Clear authentication cookies (logout)
    """
    cookie_manager = get_cookie_manager()
    
    if not cookie_manager:
        return
    
    try:
        cookie_manager.delete('t21_auth_token')
        cookie_manager.delete('t21_user_info')
    except:
        pass


def initialize_auth_session():
    """
    Initialize authentication session
    Call this at the start of every page to restore login state
    """
    # Skip if already logged in
    if st.session_state.get('logged_in'):
        return True
    
    # Try to restore from cookie
    user_data = load_auth_from_cookie()
    
    if user_data:
        # Restore session
        class SimpleUser:
            def __init__(self, data):
                if isinstance(data, dict):
                    self.email = data.get('email')
                    self.full_name = data.get('full_name', data.get('email'))
                    self.role = data.get('role', 'student')
                    self.user_type = data.get('user_type', 'student')
                else:
                    # UserAccount object
                    self.email = data.email
                    self.full_name = data.full_name
                    self.role = data.role
                    self.user_type = data.user_type
        
        user_obj = SimpleUser(user_data)
        
        st.session_state.logged_in = True
        st.session_state.user_license = user_obj
        st.session_state.user_email = user_obj.email
        st.session_state.session_email = user_obj.email
        st.session_state.auth_restored_from_cookie = True
        
        return True
    
    return False


def logout_user():
    """
    Complete logout - clear session and cookies
    """
    # Clear cookies
    clear_auth_cookie()
    
    # Clear session
    keys_to_clear = [
        'logged_in',
        'user_license',
        'user_email',
        'session_email',
        'auth_source',
        'auth_restored_from_cookie',
        'show_2fa_prompt',
        'pending_2fa_user'
    ]
    
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]
