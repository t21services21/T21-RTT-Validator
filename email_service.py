"""
T21 SERVICES - EMAIL NOTIFICATION SYSTEM
Powered by SendGrid for professional email communications

Features:
- Welcome emails
- Password reset
- Trial expiry warnings
- Upgrade confirmations
- Admin bulk emails
"""

import streamlit as st
from datetime import datetime
import random
import string

# SendGrid integration
try:
    from sendgrid import SendGridAPIClient
    from sendgrid.helpers.mail import Mail, Email, To, Content
    SENDGRID_AVAILABLE = True
except ImportError:
    SENDGRID_AVAILABLE = False


def send_email(to_email, subject, html_content, from_name="T21 Services"):
    """Send email via SendGrid"""
    try:
        if not SENDGRID_AVAILABLE:
            print("SendGrid not available")
            return False
        
        # Get API key and from email from secrets
        api_key = st.secrets.get("SENDGRID_API_KEY")
        from_email = st.secrets.get("FROM_EMAIL", "admin@t21services.co.uk")
        
        if not api_key:
            print("SendGrid API key not found")
            return False
        
        # Create email
        message = Mail(
            from_email=Email(from_email, from_name),
            to_emails=To(to_email),
            subject=subject,
            html_content=Content("text/html", html_content)
        )
        
        # Send via SendGrid
        sg = SendGridAPIClient(api_key)
        response = sg.send(message)
        
        return response.status_code in [200, 201, 202]
        
    except Exception as e:
        print(f"Email error: {e}")
        return False


def send_welcome_email(user_email, user_name, trial_hours=48):
    """Send welcome email to new user"""
    subject = "🎉 Welcome to T21 RTT Training Platform!"
    
    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #e0e0e0; border-radius: 10px;">
            <h1 style="color: #0066cc;">Welcome to T21 Services! 🎉</h1>
            
            <p>Hi {user_name},</p>
            
            <p>Thank you for joining the <strong>T21 RTT Pathway Intelligence & Validation Training Platform!</strong></p>
            
            <div style="background-color: #f0f8ff; padding: 15px; border-left: 4px solid #0066cc; margin: 20px 0;">
                <h3 style="margin-top: 0;">🎁 Your {trial_hours}-Hour FREE Trial Starts NOW!</h3>
                <p><strong>You have FULL ACCESS to:</strong></p>
                <ul>
                    <li>✅ RTT Pathway Validator (Unlimited)</li>
                    <li>✅ AI RTT Tutor (Unlimited)</li>
                    <li>✅ 40+ Training Scenarios</li>
                    <li>✅ Interactive Quizzes & Games</li>
                    <li>✅ PAS Practice System</li>
                    <li>✅ Interview Prep Tool</li>
                    <li>✅ CV Builder</li>
                    <li>✅ And ALL other features!</li>
                </ul>
            </div>
            
            <div style="background-color: #fff3cd; padding: 15px; border-left: 4px solid #ffc107; margin: 20px 0;">
                <p><strong>⏰ Your trial ends in {trial_hours} hours</strong></p>
                <p>Make the most of your trial! After {trial_hours} hours, you'll need to upgrade to continue.</p>
            </div>
            
            <p><strong>🚀 Get Started:</strong></p>
            <ol>
                <li>Login to your dashboard</li>
                <li>Try the RTT Pathway Validator</li>
                <li>Chat with AI RTT Tutor</li>
                <li>Take interactive quizzes</li>
                <li>Practice on PAS simulator</li>
            </ol>
            
            <div style="text-align: center; margin: 30px 0;">
                <a href="https://t21-rtt-validator.streamlit.app" 
                   style="background-color: #0066cc; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; display: inline-block; font-weight: bold;">
                    LOGIN NOW →
                </a>
            </div>
            
            <p><strong>Need help?</strong> Reply to this email or contact us at admin@t21services.co.uk</p>
            
            <p>Best regards,<br>
            <strong>T21 Services Team</strong><br>
            Your RTT Training Experts</p>
            
            <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 20px 0;">
            <p style="font-size: 12px; color: #666;">
                © 2025 T21 Services. All rights reserved.<br>
                64 Upper Parliament Street, Liverpool, L8 7LF, United Kingdom
            </p>
        </div>
    </body>
    </html>
    """
    
    return send_email(user_email, subject, html_content)


def send_password_reset_email(user_email, reset_code):
    """Send password reset email with code"""
    subject = "🔐 Password Reset Code - T21 Services"
    
    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #e0e0e0; border-radius: 10px;">
            <h1 style="color: #0066cc;">Password Reset Request 🔐</h1>
            
            <p>You requested to reset your password for your T21 Services account.</p>
            
            <div style="background-color: #f0f8ff; padding: 20px; border-left: 4px solid #0066cc; margin: 20px 0; text-align: center;">
                <p style="margin: 0; font-size: 14px; color: #666;">Your Password Reset Code:</p>
                <h2 style="margin: 10px 0; font-size: 36px; letter-spacing: 5px; color: #0066cc;">{reset_code}</h2>
                <p style="margin: 0; font-size: 12px; color: #666;">This code expires in 15 minutes</p>
            </div>
            
            <p><strong>To reset your password:</strong></p>
            <ol>
                <li>Go to the password reset page</li>
                <li>Enter this code: <strong>{reset_code}</strong></li>
                <li>Create your new password</li>
            </ol>
            
            <div style="background-color: #fff3cd; padding: 15px; border-left: 4px solid #ffc107; margin: 20px 0;">
                <p><strong>⚠️ Didn't request this?</strong></p>
                <p>If you didn't request a password reset, please ignore this email. Your password will remain unchanged.</p>
            </div>
            
            <p>Best regards,<br>
            <strong>T21 Services Team</strong></p>
            
            <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 20px 0;">
            <p style="font-size: 12px; color: #666;">
                © 2025 T21 Services. All rights reserved.
            </p>
        </div>
    </body>
    </html>
    """
    
    return send_email(user_email, subject, html_content)


def send_trial_expiry_warning(user_email, user_name, hours_remaining):
    """Send trial expiry warning email"""
    subject = f"⏰ Your Trial Expires in {hours_remaining} Hours - T21 Services"
    
    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #e0e0e0; border-radius: 10px;">
            <h1 style="color: #ff6600;">⏰ Your Trial is Ending Soon!</h1>
            
            <p>Hi {user_name},</p>
            
            <div style="background-color: #fff3cd; padding: 20px; border-left: 4px solid #ffc107; margin: 20px 0; text-align: center;">
                <h2 style="margin: 0; color: #ff6600;">Only {hours_remaining} Hours Left!</h2>
                <p>Your free trial ends soon. Upgrade now to keep learning!</p>
            </div>
            
            <p><strong>Don't lose access to:</strong></p>
            <ul>
                <li>✅ RTT Pathway Validator</li>
                <li>✅ AI RTT Tutor</li>
                <li>✅ 40+ Training Scenarios</li>
                <li>✅ Interactive Quizzes</li>
                <li>✅ PAS Practice System</li>
                <li>✅ Interview Prep & CV Builder</li>
                <li>✅ Certification Exam</li>
            </ul>
            
            <div style="text-align: center; margin: 30px 0;">
                <a href="https://t21-rtt-validator.streamlit.app" 
                   style="background-color: #ff6600; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; display: inline-block; font-weight: bold; font-size: 18px;">
                    UPGRADE NOW →
                </a>
            </div>
            
            <p><strong>🎁 Special Offer:</strong></p>
            <ul>
                <li><strong>Basic:</strong> £299 / 3 months</li>
                <li><strong>Professional:</strong> £599 / 6 months (MOST POPULAR!)</li>
                <li><strong>Premium:</strong> £999 / 12 months (BEST VALUE!)</li>
            </ul>
            
            <p>Questions? Contact us at admin@t21services.co.uk</p>
            
            <p>Best regards,<br>
            <strong>T21 Services Team</strong></p>
            
            <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 20px 0;">
            <p style="font-size: 12px; color: #666;">
                © 2025 T21 Services. All rights reserved.
            </p>
        </div>
    </body>
    </html>
    """
    
    return send_email(user_email, subject, html_content)


def send_trial_expired_email(user_email, user_name):
    """Send trial expired notification"""
    subject = "❌ Your Trial Has Ended - Upgrade to Continue"
    
    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #e0e0e0; border-radius: 10px;">
            <h1 style="color: #cc0000;">Your Trial Has Ended</h1>
            
            <p>Hi {user_name},</p>
            
            <p>Your 48-hour free trial has expired. We hope you enjoyed exploring the T21 RTT Training Platform!</p>
            
            <div style="background-color: #ffebee; padding: 20px; border-left: 4px solid #cc0000; margin: 20px 0;">
                <h3 style="margin-top: 0;">🔒 Your Account is Now Locked</h3>
                <p>To continue your RTT training journey, please upgrade to a paid plan.</p>
            </div>
            
            <div style="text-align: center; margin: 30px 0;">
                <a href="https://t21-rtt-validator.streamlit.app" 
                   style="background-color: #0066cc; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; display: inline-block; font-weight: bold; font-size: 18px;">
                    UPGRADE NOW →
                </a>
            </div>
            
            <p><strong>Choose Your Plan:</strong></p>
            <ul>
                <li><strong>Basic:</strong> £299 / 3 months - Perfect for beginners</li>
                <li><strong>Professional:</strong> £599 / 6 months - MOST POPULAR!</li>
                <li><strong>Premium:</strong> £999 / 12 months - BEST VALUE + Job Support!</li>
            </ul>
            
            <p>Questions? We're here to help! Contact us at admin@t21services.co.uk</p>
            
            <p>Best regards,<br>
            <strong>T21 Services Team</strong></p>
            
            <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 20px 0;">
            <p style="font-size: 12px; color: #666;">
                © 2025 T21 Services. All rights reserved.
            </p>
        </div>
    </body>
    </html>
    """
    
    return send_email(user_email, subject, html_content)


def send_bulk_email(to_emails, subject, message):
    """Send bulk email to multiple users"""
    success_count = 0
    failed_emails = []
    
    for email in to_emails:
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #e0e0e0; border-radius: 10px;">
                <div style="text-align: center; margin-bottom: 20px;">
                    <h2 style="color: #0066cc;">T21 Services</h2>
                </div>
                
                <div style="background-color: #f9f9f9; padding: 20px; border-radius: 5px;">
                    {message}
                </div>
                
                <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 20px 0;">
                <p style="font-size: 12px; color: #666;">
                    © 2025 T21 Services. All rights reserved.<br>
                    64 Upper Parliament Street, Liverpool, L8 7LF, United Kingdom
                </p>
            </div>
        </body>
        </html>
        """
        
        if send_email(email, subject, html_content):
            success_count += 1
        else:
            failed_emails.append(email)
    
    return success_count, failed_emails


def generate_reset_code():
    """Generate 6-digit reset code"""
    return ''.join(random.choices(string.digits, k=6))
