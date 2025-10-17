"""
COMPREHENSIVE ACCOUNT SECURITY & ANTI-SHARING SYSTEM
Prevents account sharing, tracks suspicious activity, enforces device limits
Makes T21 stand out as most secure NHS training platform!
"""

import streamlit as st
import json
import os
from datetime import datetime, timedelta
import hashlib
import uuid
from typing import Dict, List, Optional, Tuple

# Security configuration
SECURITY_CONFIG = {
    'max_concurrent_sessions': 1,  # Only 1 active session at a time
    'max_devices': 3,  # Maximum 3 registered devices
    'session_timeout_minutes': 15,  # Auto logout after 15 min inactivity
    'suspicious_login_threshold': 3,  # Flag after 3 locations in 24 hours
    'require_2fa_for_tiers': ['certified', 'premium'],  # Require 2FA for paid tiers
    'exam_verification_required': True,  # Email verification for exams
    'ip_change_notification': True,  # Email when IP changes
    'device_fingerprint_enabled': True,  # Track unique device characteristics
}

SECURITY_DB_FILE = "security_data.json"


def load_security_db() -> dict:
    """Load security database"""
    if os.path.exists(SECURITY_DB_FILE):
        try:
            with open(SECURITY_DB_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}


def save_security_db(db: dict):
    """Save security database"""
    with open(SECURITY_DB_FILE, 'w') as f:
        json.dump(db, f, indent=2)


def get_device_fingerprint() -> str:
    """
    Generate unique device fingerprint based on browser/system characteristics
    This helps identify when same account used on different devices
    """
    import streamlit.web.server.websocket_headers as websocket_headers
    
    try:
        headers = websocket_headers.get()
        if headers:
            # Combine multiple characteristics for unique fingerprint
            user_agent = headers.get('User-Agent', 'unknown')
            accept_language = headers.get('Accept-Language', 'unknown')
            
            # Create hash from characteristics
            fingerprint_data = f"{user_agent}_{accept_language}"
            fingerprint = hashlib.sha256(fingerprint_data.encode()).hexdigest()[:16]
            return fingerprint
    except:
        pass
    
    # Fallback: generate random but consistent per session
    if 'device_fingerprint' not in st.session_state:
        st.session_state.device_fingerprint = str(uuid.uuid4())[:16]
    
    return st.session_state.device_fingerprint


def get_user_ip() -> str:
    """Get user's IP address (approximate)"""
    try:
        import streamlit.web.server.websocket_headers as websocket_headers
        headers = websocket_headers.get()
        if headers:
            # Try to get real IP (might be proxy)
            ip = headers.get('X-Forwarded-For', headers.get('Remote-Addr', 'unknown'))
            return ip.split(',')[0].strip()  # First IP if multiple
    except:
        pass
    return "unknown"


def get_user_location_estimate(ip: str) -> str:
    """
    Estimate user location from IP (very rough)
    In production, use IP geolocation service like ipapi.co or ip-api.com
    """
    # This is placeholder - in production integrate with IP geolocation API
    if ip == "unknown":
        return "Unknown Location"
    
    # For now, just return IP range indicator
    ip_parts = ip.split('.')
    if len(ip_parts) >= 2:
        return f"IP Range: {ip_parts[0]}.{ip_parts[1]}.x.x"
    
    return "Unknown Location"


def register_device(email: str, device_fingerprint: str, device_name: str = None) -> Tuple[bool, str]:
    """
    Register a new device for user
    Returns (success, message)
    """
    db = load_security_db()
    
    if email not in db:
        db[email] = {
            'devices': [],
            'sessions': [],
            'login_history': [],
            'suspicious_activity': []
        }
    
    user_data = db[email]
    
    # Check if device already registered
    for device in user_data['devices']:
        if device['fingerprint'] == device_fingerprint:
            # Update last used
            device['last_used'] = datetime.now().isoformat()
            save_security_db(db)
            return True, "Device already registered"
    
    # Check device limit
    if len(user_data['devices']) >= SECURITY_CONFIG['max_devices']:
        return False, f"Maximum {SECURITY_CONFIG['max_devices']} devices allowed! Remove old devices first."
    
    # Register new device
    device_info = {
        'fingerprint': device_fingerprint,
        'name': device_name or f"Device {len(user_data['devices']) + 1}",
        'registered': datetime.now().isoformat(),
        'last_used': datetime.now().isoformat(),
        'ip': get_user_ip(),
        'location': get_user_location_estimate(get_user_ip())
    }
    
    user_data['devices'].append(device_info)
    save_security_db(db)
    
    return True, f"Device registered successfully! ({len(user_data['devices'])}/{SECURITY_CONFIG['max_devices']})"


def check_concurrent_sessions(email: str) -> Tuple[bool, str]:
    """
    Check if user has too many active sessions
    Returns (allowed, message)
    """
    db = load_security_db()
    
    if email not in db:
        return True, "No active sessions"
    
    user_data = db[email]
    
    # Clean up expired sessions (older than session timeout)
    current_time = datetime.now()
    timeout_minutes = SECURITY_CONFIG['session_timeout_minutes']
    
    active_sessions = []
    for session in user_data.get('sessions', []):
        session_time = datetime.fromisoformat(session['last_activity'])
        if current_time - session_time < timedelta(minutes=timeout_minutes):
            active_sessions.append(session)
    
    # Update active sessions
    user_data['sessions'] = active_sessions
    save_security_db(db)
    
    # Check concurrent session limit
    if len(active_sessions) >= SECURITY_CONFIG['max_concurrent_sessions']:
        return False, f"Account already in use! Only {SECURITY_CONFIG['max_concurrent_sessions']} active session allowed. Log out from other device first."
    
    return True, f"Active sessions: {len(active_sessions)}/{SECURITY_CONFIG['max_concurrent_sessions']}"


def create_session(email: str, device_fingerprint: str) -> str:
    """
    Create new session for user
    Returns session_id
    """
    db = load_security_db()
    
    if email not in db:
        db[email] = {
            'devices': [],
            'sessions': [],
            'login_history': [],
            'suspicious_activity': []
        }
    
    user_data = db[email]
    
    # Create session
    session_id = str(uuid.uuid4())
    session_info = {
        'session_id': session_id,
        'device_fingerprint': device_fingerprint,
        'created': datetime.now().isoformat(),
        'last_activity': datetime.now().isoformat(),
        'ip': get_user_ip(),
        'location': get_user_location_estimate(get_user_ip())
    }
    
    user_data['sessions'].append(session_info)
    
    # Log login to history
    user_data['login_history'].append({
        'timestamp': datetime.now().isoformat(),
        'ip': get_user_ip(),
        'location': get_user_location_estimate(get_user_ip()),
        'device_fingerprint': device_fingerprint,
        'success': True
    })
    
    save_security_db(db)
    
    return session_id


def update_session_activity(email: str, session_id: str):
    """Update last activity time for session"""
    db = load_security_db()
    
    if email in db:
        for session in db[email].get('sessions', []):
            if session['session_id'] == session_id:
                session['last_activity'] = datetime.now().isoformat()
                save_security_db(db)
                break


def end_session(email: str, session_id: str):
    """End a specific session"""
    db = load_security_db()
    
    if email in db:
        user_data = db[email]
        user_data['sessions'] = [s for s in user_data['sessions'] if s['session_id'] != session_id]
        save_security_db(db)


def end_all_sessions(email: str):
    """End all sessions for user (force logout everywhere)"""
    db = load_security_db()
    
    if email in db:
        db[email]['sessions'] = []
        save_security_db(db)


def detect_suspicious_activity(email: str) -> List[dict]:
    """
    Analyze login patterns and detect suspicious activity
    Returns list of suspicious activities
    """
    db = load_security_db()
    
    if email not in db:
        return []
    
    user_data = db[email]
    suspicious = []
    
    # Check 1: Multiple locations in short time
    recent_logins = user_data.get('login_history', [])[-10:]  # Last 10 logins
    if len(recent_logins) >= 3:
        locations = set()
        for login in recent_logins[-3:]:
            locations.add(login.get('location', 'unknown'))
        
        if len(locations) >= 3:
            suspicious.append({
                'type': 'multiple_locations',
                'severity': 'high',
                'message': f'Account accessed from {len(locations)} different locations recently',
                'details': list(locations)
            })
    
    # Check 2: Too many devices
    device_count = len(user_data.get('devices', []))
    if device_count >= SECURITY_CONFIG['max_devices']:
        suspicious.append({
            'type': 'max_devices',
            'severity': 'medium',
            'message': f'Maximum devices registered ({device_count}/{SECURITY_CONFIG["max_devices"]})',
            'details': [d['name'] for d in user_data['devices']]
        })
    
    # Check 3: Unusual activity patterns
    # (Could add more sophisticated detection here)
    
    return suspicious


def remove_device(email: str, device_fingerprint: str) -> Tuple[bool, str]:
    """Remove a registered device"""
    db = load_security_db()
    
    if email not in db:
        return False, "No devices registered"
    
    user_data = db[email]
    original_count = len(user_data['devices'])
    
    # Remove device
    user_data['devices'] = [d for d in user_data['devices'] if d['fingerprint'] != device_fingerprint]
    
    # End any sessions from that device
    user_data['sessions'] = [s for s in user_data['sessions'] if s['device_fingerprint'] != device_fingerprint]
    
    save_security_db(db)
    
    if len(user_data['devices']) < original_count:
        return True, "Device removed successfully"
    else:
        return False, "Device not found"


def get_user_security_info(email: str) -> dict:
    """Get all security info for user"""
    db = load_security_db()
    
    if email not in db:
        return {
            'devices': [],
            'active_sessions': 0,
            'login_history': [],
            'suspicious_activity': []
        }
    
    user_data = db[email]
    
    # Count active sessions
    current_time = datetime.now()
    timeout_minutes = SECURITY_CONFIG['session_timeout_minutes']
    
    active_sessions = 0
    for session in user_data.get('sessions', []):
        session_time = datetime.fromisoformat(session['last_activity'])
        if current_time - session_time < timedelta(minutes=timeout_minutes):
            active_sessions += 1
    
    return {
        'devices': user_data.get('devices', []),
        'active_sessions': active_sessions,
        'login_history': user_data.get('login_history', [])[-20:],  # Last 20 logins
        'suspicious_activity': detect_suspicious_activity(email)
    }


def require_verification_for_action(email: str, action: str) -> bool:
    """
    Check if action requires additional verification
    Returns True if verification needed
    """
    # Actions that always require verification
    high_security_actions = [
        'take_exam',
        'download_certificate',
        'join_live_session',
        'change_password',
        'remove_device'
    ]
    
    if action in high_security_actions:
        return True
    
    # Check if user's tier requires 2FA
    # (Would integrate with user license system here)
    
    return False


def log_security_event(email: str, event_type: str, details: dict):
    """Log security-related events"""
    db = load_security_db()
    
    if email not in db:
        db[email] = {
            'devices': [],
            'sessions': [],
            'login_history': [],
            'suspicious_activity': []
        }
    
    event = {
        'timestamp': datetime.now().isoformat(),
        'type': event_type,
        'details': details
    }
    
    if 'security_events' not in db[email]:
        db[email]['security_events'] = []
    
    db[email]['security_events'].append(event)
    
    # Keep only last 100 events
    db[email]['security_events'] = db[email]['security_events'][-100:]
    
    save_security_db(db)


def check_and_enforce_security(email: str) -> Tuple[bool, str]:
    """
    Main security check - called on every page load
    Returns (allowed, message)
    """
    # Get device fingerprint
    device_fingerprint = get_device_fingerprint()
    
    # Check 1: Is device registered?
    db = load_security_db()
    if email in db:
        user_data = db[email]
        device_registered = any(d['fingerprint'] == device_fingerprint for d in user_data.get('devices', []))
        
        if not device_registered:
            # Try to register device
            success, message = register_device(email, device_fingerprint)
            if not success:
                return False, message
    
    # Check 2: Concurrent sessions
    allowed, message = check_concurrent_sessions(email)
    if not allowed:
        return False, message
    
    # Check 3: Update or create session
    if 'security_session_id' not in st.session_state:
        session_id = create_session(email, device_fingerprint)
        st.session_state.security_session_id = session_id
    else:
        update_session_activity(email, st.session_state.security_session_id)
    
    # Check 4: Detect suspicious activity
    suspicious = detect_suspicious_activity(email)
    if suspicious:
        high_severity = [s for s in suspicious if s['severity'] == 'high']
        if high_severity:
            # Flag but don't block (yet)
            log_security_event(email, 'suspicious_activity_detected', {'activities': high_severity})
    
    return True, "Security check passed"


# Export functions
__all__ = [
    'check_and_enforce_security',
    'get_user_security_info',
    'remove_device',
    'end_session',
    'end_all_sessions',
    'require_verification_for_action',
    'log_security_event',
    'SECURITY_CONFIG'
]
