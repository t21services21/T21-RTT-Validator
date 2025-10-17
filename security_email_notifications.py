"""
SECURITY EMAIL NOTIFICATIONS
Sends email alerts for security events (new device, suspicious activity, etc.)
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import Optional


def send_security_email(
    recipient_email: str,
    subject: str,
    message: str,
    event_type: str = "security_alert"
) -> bool:
    """
    Send security notification email
    Returns True if successful
    """
    
    # Email configuration from Streamlit secrets (NEVER hardcode passwords!)
    import streamlit as st
    
    SMTP_SERVER = st.secrets.get("SMTP_SERVER", "smtp.gmail.com")
    SMTP_PORT = st.secrets.get("SMTP_PORT", 587)
    SENDER_EMAIL = st.secrets.get("SENDER_EMAIL", "security@t21services.co.uk")
    SENDER_PASSWORD = st.secrets.get("SENDER_PASSWORD", "")
    
    # Don't send emails if password not configured
    if not SENDER_PASSWORD:
        print("Warning: SENDER_PASSWORD not configured in Streamlit secrets")
        return False
    
    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['From'] = f"T21 Security Team <{SENDER_EMAIL}>"
        msg['To'] = recipient_email
        msg['Subject'] = subject
        
        # HTML email template
        html_content = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                          padding: 20px; text-align: center; color: white; }}
                .content {{ padding: 20px; background-color: #f9f9f9; }}
                .alert-box {{ background-color: #fff3cd; border-left: 4px solid #ffc107; 
                             padding: 15px; margin: 20px 0; }}
                .info-box {{ background-color: #d1ecf1; border-left: 4px solid #0c5460; 
                            padding: 15px; margin: 20px 0; }}
                .footer {{ padding: 20px; text-align: center; font-size: 12px; color: #666; }}
                .button {{ background-color: #667eea; color: white; padding: 12px 24px; 
                          text-decoration: none; border-radius: 5px; display: inline-block; 
                          margin: 10px 0; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🔒 T21 Healthcare Intelligence Platform</h1>
                <p>Security Notification</p>
            </div>
            
            <div class="content">
                <h2>Security Alert</h2>
                <p>Hello,</p>
                
                <div class="alert-box">
                    {message}
                </div>
                
                <p><strong>Time:</strong> {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
                
                <div class="info-box">
                    <h3>What should I do?</h3>
                    <ul>
                        <li>If this was you, no action needed</li>
                        <li>If this wasn't you, change your password immediately</li>
                        <li>Review your recent login activity</li>
                        <li>Contact support if you notice anything suspicious</li>
                    </ul>
                </div>
                
                <a href="https://t21-healthcare-platform.streamlit.app" class="button">
                    View Security Dashboard
                </a>
                
                <p>Stay safe,<br>
                T21 Security Team</p>
            </div>
            
            <div class="footer">
                <p>T21 Services Limited | Company No: 13091053 | Liverpool, England</p>
                <p>🌐 www.t21services.co.uk | 📧 security@t21services.co.uk</p>
                <p>This is an automated security notification. Please do not reply to this email.</p>
            </div>
        </body>
        </html>
        """
        
        # Attach HTML content
        html_part = MIMEText(html_content, 'html')
        msg.attach(html_part)
        
        # Send email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        
        return True
        
    except Exception as e:
        print(f"Failed to send security email: {e}")
        return False


def notify_new_device(email: str, device_name: str, location: str, ip: str):
    """Send notification when new device is registered"""
    
    subject = "🔒 New Device Registered on Your T21 Account"
    
    message = f"""
    <h3>New Device Detected</h3>
    <p>A new device has been registered to your T21 account:</p>
    <ul>
        <li><strong>Device:</strong> {device_name}</li>
        <li><strong>Location:</strong> {location}</li>
        <li><strong>IP Address:</strong> {ip}</li>
    </ul>
    """
    
    send_security_email(email, subject, message, "new_device")


def notify_login_from_new_location(email: str, location: str, ip: str):
    """Send notification when login from new location detected"""
    
    subject = "🌍 Login from New Location on Your T21 Account"
    
    message = f"""
    <h3>New Location Detected</h3>
    <p>Your T21 account was accessed from a new location:</p>
    <ul>
        <li><strong>Location:</strong> {location}</li>
        <li><strong>IP Address:</strong> {ip}</li>
    </ul>
    """
    
    send_security_email(email, subject, message, "new_location")


def notify_suspicious_activity(email: str, activity_details: str):
    """Send notification for suspicious activity"""
    
    subject = "⚠️ Suspicious Activity Detected on Your T21 Account"
    
    message = f"""
    <h3>Security Alert</h3>
    <p>We've detected suspicious activity on your T21 account:</p>
    <div style="background-color: #fff; padding: 15px; border-radius: 5px; margin: 10px 0;">
        {activity_details}
    </div>
    <p><strong style="color: #d32f2f;">Action Required:</strong> Please review your account security immediately.</p>
    """
    
    send_security_email(email, subject, message, "suspicious_activity")


def notify_max_devices_reached(email: str, device_count: int):
    """Send notification when device limit reached"""
    
    subject = "⚠️ Device Limit Reached on Your T21 Account"
    
    message = f"""
    <h3>Maximum Devices Registered</h3>
    <p>Your T21 account has reached the maximum device limit:</p>
    <ul>
        <li><strong>Registered Devices:</strong> {device_count}/3</li>
    </ul>
    <p>To add a new device, please remove an old device from your Security Dashboard.</p>
    """
    
    send_security_email(email, subject, message, "max_devices")


def notify_concurrent_session_blocked(email: str):
    """Send notification when concurrent session attempt is blocked"""
    
    subject = "🚫 Multiple Login Attempt Blocked on Your T21 Account"
    
    message = """
    <h3>Concurrent Login Blocked</h3>
    <p>Someone tried to log into your T21 account while you were already logged in.</p>
    <p>Only 1 active session is allowed at a time to prevent account sharing.</p>
    <p><strong>What happened:</strong> The login attempt was blocked to protect your account.</p>
    """
    
    send_security_email(email, subject, message, "concurrent_session_blocked")


def notify_all_sessions_terminated(email: str):
    """Send notification when user logs out from all devices"""
    
    subject = "🚪 All Sessions Terminated on Your T21 Account"
    
    message = """
    <h3>Security Action Performed</h3>
    <p>All active sessions on your T21 account have been terminated.</p>
    <p>You have been logged out from all devices.</p>
    <p>If you did not perform this action, please change your password immediately.</p>
    """
    
    send_security_email(email, subject, message, "sessions_terminated")


def notify_password_changed(email: str):
    """Send notification when password is changed"""
    
    subject = "🔐 Password Changed on Your T21 Account"
    
    message = """
    <h3>Password Changed Successfully</h3>
    <p>Your T21 account password has been changed.</p>
    <p>If you did not make this change, please contact support immediately at security@t21services.co.uk</p>
    """
    
    send_security_email(email, subject, message, "password_changed")


def notify_failed_login_attempts(email: str, attempt_count: int):
    """Send notification about multiple failed login attempts"""
    
    subject = "⚠️ Failed Login Attempts on Your T21 Account"
    
    message = f"""
    <h3>Multiple Failed Login Attempts</h3>
    <p>There have been {attempt_count} failed login attempts on your T21 account in the last hour.</p>
    <p>Your account is secure, but someone may be trying to access it.</p>
    <p><strong>Recommended Actions:</strong></p>
    <ul>
        <li>Change your password if you haven't recently</li>
        <li>Enable Two-Factor Authentication (2FA)</li>
        <li>Review your security settings</li>
    </ul>
    """
    
    send_security_email(email, subject, message, "failed_attempts")


# Export functions
__all__ = [
    'notify_new_device',
    'notify_login_from_new_location',
    'notify_suspicious_activity',
    'notify_max_devices_reached',
    'notify_concurrent_session_blocked',
    'notify_all_sessions_terminated',
    'notify_password_changed',
    'notify_failed_login_attempts'
]
