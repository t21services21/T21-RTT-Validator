"""
T21 ADVANCED USER TRACKING SYSTEM
Complete user geolocation, activity tracking, and management

Features:
- IP address tracking
- Geolocation (country, state, city, street)
- Login history
- Device information
- Browser fingerprinting
- Activity monitoring
- Security alerts
"""

import json
import os
from datetime import datetime
import hashlib

# Database files
TRACKING_DB = "data/user_tracking.json"
LOGIN_HISTORY_DB = "data/login_history.json"

# Ensure data directory exists
os.makedirs("data", exist_ok=True)

def load_tracking_db():
    """Load user tracking database"""
    if os.path.exists(TRACKING_DB):
        try:
            with open(TRACKING_DB, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_tracking_db(db):
    """Save user tracking database"""
    with open(TRACKING_DB, 'w') as f:
        json.dump(db, f, indent=2)

def load_login_history_db():
    """Load login history database"""
    if os.path.exists(LOGIN_HISTORY_DB):
        try:
            with open(LOGIN_HISTORY_DB, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_login_history_db(db):
    """Save login history database"""
    with open(LOGIN_HISTORY_DB, 'w') as f:
        json.dump(db, f, indent=2)


def get_user_ip():
    """
    Get user's IP address
    
    In production, use st.experimental_user or request headers
    For now, returns placeholder
    """
    # In Streamlit Cloud, you can use:
    # import streamlit as st
    # ip = st.experimental_user.get("ip_address", "Unknown")
    
    # For local testing, return placeholder
    return "Unknown (Local)"


def get_geolocation_from_ip(ip_address):
    """
    Get geolocation data from IP address
    
    Uses free IP geolocation API
    Returns: country, region, city, lat, lon, zip, street estimate
    """
    
    if ip_address == "Unknown (Local)" or ip_address == "127.0.0.1":
        return {
            "ip": ip_address,
            "country": "United Kingdom",
            "country_code": "GB",
            "region": "England",
            "region_code": "ENG",
            "city": "Liverpool",
            "zip": "L8 7LF",
            "lat": 53.3811,
            "lon": -2.9775,
            "timezone": "Europe/London",
            "isp": "Local Network",
            "org": "Development Environment",
            "as": "AS0000",
            "street_estimate": "64 Upper Parliament Street (Company HQ)",
            "accuracy": "City Level (Local Testing)"
        }
    
    try:
        import requests
        
        # Using free ipapi.co service (100 requests/day free)
        response = requests.get(f"https://ipapi.co/{ip_address}/json/", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            
            return {
                "ip": ip_address,
                "country": data.get("country_name", "Unknown"),
                "country_code": data.get("country_code", "Unknown"),
                "region": data.get("region", "Unknown"),
                "region_code": data.get("region_code", "Unknown"),
                "city": data.get("city", "Unknown"),
                "zip": data.get("postal", "Unknown"),
                "lat": data.get("latitude", 0),
                "lon": data.get("longitude", 0),
                "timezone": data.get("timezone", "Unknown"),
                "isp": data.get("org", "Unknown"),
                "org": data.get("org", "Unknown"),
                "as": data.get("asn", "Unknown"),
                "street_estimate": f"{data.get('city', 'Unknown')} Area (IP-based estimate)",
                "accuracy": "City Level (IP Geolocation)"
            }
    except Exception as e:
        return {
            "ip": ip_address,
            "country": "Unknown",
            "error": str(e),
            "accuracy": "Failed"
        }
    
    return {
        "ip": ip_address,
        "country": "Unknown",
        "accuracy": "Failed"
    }


def get_device_info():
    """
    Get user device information
    
    Returns browser, OS, device type
    """
    # In production with Streamlit, can get from headers
    # For now, return placeholder
    
    return {
        "browser": "Chrome/Edge",
        "os": "Windows 10/11",
        "device": "Desktop/Laptop",
        "screen_resolution": "1920x1080",
        "user_agent": "Mozilla/5.0..."
    }


def track_user_login(email, ip_address=None, success=True):
    """
    Track user login attempt
    
    Args:
        email: User email
        ip_address: User IP (optional, will auto-detect)
        success: Whether login was successful
    """
    
    if ip_address is None:
        ip_address = get_user_ip()
    
    # Get geolocation
    geo_data = get_geolocation_from_ip(ip_address)
    
    # Get device info
    device_info = get_device_info()
    
    # Load login history
    history_db = load_login_history_db()
    
    if email not in history_db:
        history_db[email] = []
    
    # Create login record
    login_record = {
        "timestamp": datetime.now().isoformat(),
        "ip_address": ip_address,
        "geolocation": geo_data,
        "device": device_info,
        "success": success,
        "login_method": "Email/Password"
    }
    
    # Add to history (keep last 100 logins per user)
    history_db[email].append(login_record)
    history_db[email] = history_db[email][-100:]  # Keep last 100
    
    # Save
    save_login_history_db(history_db)
    
    # Update user tracking
    tracking_db = load_tracking_db()
    
    if email not in tracking_db:
        tracking_db[email] = {
            "email": email,
            "first_seen": datetime.now().isoformat(),
            "total_logins": 0,
            "successful_logins": 0,
            "failed_logins": 0,
            "unique_ips": [],
            "unique_locations": [],
            "last_login": None,
            "last_ip": None,
            "last_location": None
        }
    
    # Update stats
    tracking_db[email]["total_logins"] += 1
    
    if success:
        tracking_db[email]["successful_logins"] += 1
        tracking_db[email]["last_login"] = datetime.now().isoformat()
        tracking_db[email]["last_ip"] = ip_address
        tracking_db[email]["last_location"] = f"{geo_data.get('city', 'Unknown')}, {geo_data.get('country', 'Unknown')}"
        
        # Track unique IPs
        if ip_address not in tracking_db[email]["unique_ips"]:
            tracking_db[email]["unique_ips"].append(ip_address)
        
        # Track unique locations
        location_str = f"{geo_data.get('city')}, {geo_data.get('country')}"
        if location_str not in tracking_db[email]["unique_locations"]:
            tracking_db[email]["unique_locations"].append(location_str)
    else:
        tracking_db[email]["failed_logins"] += 1
    
    # Save
    save_tracking_db(tracking_db)
    
    return login_record


def get_user_login_history(email, limit=50):
    """
    Get login history for a user
    
    Args:
        email: User email
        limit: Number of recent logins to return
    
    Returns:
        List of login records
    """
    history_db = load_login_history_db()
    
    if email in history_db:
        return history_db[email][-limit:][::-1]  # Most recent first
    
    return []


def get_user_tracking_summary(email):
    """
    Get tracking summary for a user
    
    Returns complete tracking profile
    """
    tracking_db = load_tracking_db()
    
    if email in tracking_db:
        return tracking_db[email]
    
    return None


def get_all_users_tracking():
    """
    Get tracking data for ALL users
    
    Returns complete tracking database
    """
    return load_tracking_db()


def detect_suspicious_login(email, current_ip, current_location):
    """
    Detect suspicious login patterns
    
    Returns:
        {
            "suspicious": bool,
            "reasons": [],
            "risk_level": "LOW/MEDIUM/HIGH"
        }
    """
    
    tracking = get_user_tracking_summary(email)
    
    if not tracking:
        return {
            "suspicious": False,
            "reasons": [],
            "risk_level": "LOW",
            "message": "First time login"
        }
    
    suspicious = False
    reasons = []
    
    # Check 1: New IP from different country
    if current_ip not in tracking["unique_ips"]:
        last_location = tracking.get("last_location", "")
        
        if current_location and last_location:
            # Simple check - different country
            if "," in current_location and "," in last_location:
                current_country = current_location.split(",")[-1].strip()
                last_country = last_location.split(",")[-1].strip()
                
                if current_country != last_country:
                    suspicious = True
                    reasons.append(f"Login from new country: {current_country} (previous: {last_country})")
    
    # Check 2: Too many failed logins recently
    failed = tracking.get("failed_logins", 0)
    total = tracking.get("total_logins", 1)
    
    if total > 5 and (failed / total) > 0.3:  # 30% failure rate
        suspicious = True
        reasons.append(f"High failure rate: {failed}/{total} attempts")
    
    # Check 3: Rapid location changes (impossible travel)
    # Would need timestamp comparison - implement if needed
    
    # Determine risk level
    risk_level = "LOW"
    if len(reasons) >= 2:
        risk_level = "HIGH"
    elif len(reasons) == 1:
        risk_level = "MEDIUM"
    
    return {
        "suspicious": suspicious,
        "reasons": reasons,
        "risk_level": risk_level,
        "message": " | ".join(reasons) if reasons else "Normal login pattern"
    }


def track_user_activity(email, activity_type, details=None):
    """
    Track user activity (page views, feature usage, etc.)
    
    Args:
        email: User email
        activity_type: Type of activity (e.g., "page_view", "feature_use", "download")
        details: Additional details (dict)
    """
    
    activity_file = "data/user_activity.json"
    
    # Load existing activity
    if os.path.exists(activity_file):
        with open(activity_file, 'r') as f:
            activity_db = json.load(f)
    else:
        activity_db = {}
    
    if email not in activity_db:
        activity_db[email] = []
    
    # Create activity record
    activity_record = {
        "timestamp": datetime.now().isoformat(),
        "type": activity_type,
        "details": details or {}
    }
    
    # Add to activity (keep last 1000 per user)
    activity_db[email].append(activity_record)
    activity_db[email] = activity_db[email][-1000:]
    
    # Save
    with open(activity_file, 'w') as f:
        json.dump(activity_db, f, indent=2)


def get_user_activity_summary(email, days=7):
    """
    Get activity summary for user in last X days
    
    Returns:
        {
            "page_views": int,
            "features_used": list,
            "active_days": int,
            "last_activity": datetime
        }
    """
    activity_file = "data/user_activity.json"
    
    if not os.path.exists(activity_file):
        return {
            "page_views": 0,
            "features_used": [],
            "active_days": 0,
            "last_activity": None
        }
    
    with open(activity_file, 'r') as f:
        activity_db = json.load(f)
    
    if email not in activity_db:
        return {
            "page_views": 0,
            "features_used": [],
            "active_days": 0,
            "last_activity": None
        }
    
    # Filter by date range
    from datetime import timedelta
    cutoff = datetime.now() - timedelta(days=days)
    
    recent_activity = []
    for activity in activity_db[email]:
        activity_time = datetime.fromisoformat(activity["timestamp"])
        if activity_time >= cutoff:
            recent_activity.append(activity)
    
    # Calculate summary
    page_views = len([a for a in recent_activity if a["type"] == "page_view"])
    features_used = list(set([a["details"].get("feature") for a in recent_activity if a["type"] == "feature_use"]))
    
    # Get unique days
    active_dates = set([datetime.fromisoformat(a["timestamp"]).date() for a in recent_activity])
    active_days = len(active_dates)
    
    last_activity = max([datetime.fromisoformat(a["timestamp"]) for a in recent_activity]) if recent_activity else None
    
    return {
        "page_views": page_views,
        "features_used": features_used,
        "active_days": active_days,
        "last_activity": last_activity.isoformat() if last_activity else None,
        "total_activities": len(recent_activity)
    }


# Initialize databases on import
if not os.path.exists(TRACKING_DB):
    save_tracking_db({})

if not os.path.exists(LOGIN_HISTORY_DB):
    save_login_history_db({})

# User Tracking System Initialized (no unicode output)
