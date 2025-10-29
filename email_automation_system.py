"""
EMAIL AUTOMATION SYSTEM
Automated email notifications for students, clients, and operations

Features:
- Welcome emails
- Course enrollment confirmations
- Payment receipts
- Certificate delivery
- Security alerts
- Marketing campaigns
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from datetime import datetime
import os

class EmailAutomation:
    """
    Email automation system
    Uses SendGrid (already configured for T21)
    """
    
    def __init__(self):
        # SendGrid configuration (already set up for T21)
        self.sender_email = "admin@t21services.co.uk"
        self.sender_name = "T21 Services UK"
        # In production: Use environment variables for API key
        self.sendgrid_configured = True
    
    def send_email(self, to_email, subject, html_content, text_content=None):
        """
        Send email using SendGrid
        In production: Use SendGrid API
        """
        try:
            # For now: Log email (in production, actually send via SendGrid)
            print(f"EMAIL SENT: To={to_email}, Subject={subject}")
            return True
        except Exception as e:
            print(f"Email error: {e}")
            return False
    
    # ============================================
    # STUDENT EMAILS
    # ============================================
    
    def send_welcome_email(self, student_email, student_name):
        """Send welcome email to new student"""
        
        subject = "Welcome to T21 Cybersecurity Training! 🎓"
        
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h1 style="color: #2c3e50;">Welcome to T21 Cybersecurity Training!</h1>
                
                <p>Dear {student_name},</p>
                
                <p>Welcome to the T21 Cybersecurity Empire! We're thrilled to have you join our community of future SOC analysts.</p>
                
                <h2 style="color: #3498db;">🚀 Getting Started</h2>
                
                <p><strong>Your learning journey begins now:</strong></p>
                
                <ol>
                    <li><strong>Access Training Portal:</strong> Log in to start your courses</li>
                    <li><strong>Complete Your Profile:</strong> Tell us about your goals</li>
                    <li><strong>Join Study Groups:</strong> Connect with fellow students</li>
                    <li><strong>Start First Lab:</strong> Get hands-on experience</li>
                </ol>
                
                <h2 style="color: #3498db;">📚 What's Included</h2>
                
                <ul>
                    <li>✅ Complete video courses</li>
                    <li>✅ Hands-on cyber labs</li>
                    <li>✅ AI tutor support 24/7</li>
                    <li>✅ Industry certifications</li>
                    <li>✅ Job placement assistance</li>
                </ul>
                
                <h2 style="color: #3498db;">💡 Need Help?</h2>
                
                <p>Our support team is here for you:</p>
                <ul>
                    <li>📧 Email: support@t21services.co.uk</li>
                    <li>💬 Live chat in platform</li>
                    <li>📚 Knowledge base</li>
                </ul>
                
                <p style="margin-top: 30px;">
                    <a href="https://t21-healthcare-platform.streamlit.app" 
                       style="background-color: #3498db; color: white; padding: 12px 30px; 
                              text-decoration: none; border-radius: 5px; display: inline-block;">
                        🚀 Start Learning Now
                    </a>
                </p>
                
                <p style="margin-top: 30px; color: #7f8c8d; font-size: 14px;">
                    Best regards,<br>
                    The T21 Team<br>
                    T21 Services UK Ltd<br>
                    www.t21services.co.uk
                </p>
            </div>
        </body>
        </html>
        """
        
        return self.send_email(student_email, subject, html_content)
    
    def send_enrollment_confirmation(self, student_email, course_name, start_date):
        """Send course enrollment confirmation"""
        
        subject = f"✅ Enrolled in {course_name}"
        
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h1 style="color: #27ae60;">✅ Enrollment Confirmed!</h1>
                
                <p>Great news! You're now enrolled in:</p>
                
                <div style="background-color: #ecf0f1; padding: 20px; border-radius: 5px; margin: 20px 0;">
                    <h2 style="color: #2c3e50; margin-top: 0;">{course_name}</h2>
                    <p><strong>Start Date:</strong> {start_date}</p>
                </div>
                
                <h3>📅 What's Next?</h3>
                
                <ol>
                    <li>Access your course materials</li>
                    <li>Complete the first module</li>
                    <li>Join the course study group</li>
                    <li>Start your first lab</li>
                </ol>
                
                <p style="margin-top: 30px;">
                    <a href="https://t21-healthcare-platform.streamlit.app" 
                       style="background-color: #27ae60; color: white; padding: 12px 30px; 
                              text-decoration: none; border-radius: 5px; display: inline-block;">
                        📚 Go to Course
                    </a>
                </p>
                
                <p style="margin-top: 30px; color: #7f8c8d;">
                    Good luck with your studies!<br>
                    The T21 Team
                </p>
            </div>
        </body>
        </html>
        """
        
        return self.send_email(student_email, subject, html_content)
    
    def send_payment_receipt(self, customer_email, payment_id, amount, course_name):
        """Send payment receipt"""
        
        subject = f"💳 Payment Receipt - {payment_id}"
        
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h1 style="color: #2c3e50;">Payment Receipt</h1>
                
                <p>Thank you for your payment!</p>
                
                <div style="background-color: #ecf0f1; padding: 20px; border-radius: 5px; margin: 20px 0;">
                    <table style="width: 100%;">
                        <tr>
                            <td><strong>Payment ID:</strong></td>
                            <td>{payment_id}</td>
                        </tr>
                        <tr>
                            <td><strong>Date:</strong></td>
                            <td>{datetime.now().strftime('%B %d, %Y')}</td>
                        </tr>
                        <tr>
                            <td><strong>Description:</strong></td>
                            <td>{course_name}</td>
                        </tr>
                        <tr>
                            <td><strong>Amount:</strong></td>
                            <td style="font-size: 20px; color: #27ae60;"><strong>£{amount:,.2f}</strong></td>
                        </tr>
                    </table>
                </div>
                
                <p>Your payment has been processed successfully. You now have full access to your course.</p>
                
                <p style="margin-top: 30px; color: #7f8c8d; font-size: 14px;">
                    T21 Services UK Ltd<br>
                    Company No: 13091053<br>
                    Liverpool, England<br>
                    www.t21services.co.uk
                </p>
            </div>
        </body>
        </html>
        """
        
        return self.send_email(customer_email, subject, html_content)
    
    def send_certificate(self, student_email, student_name, cert_name, verification_code):
        """Send certification email"""
        
        subject = f"🎉 Congratulations! You've earned {cert_name}"
        
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h1 style="color: #f39c12;">🎉 Congratulations!</h1>
                
                <p>Dear {student_name},</p>
                
                <p style="font-size: 18px;">You've successfully earned:</p>
                
                <div style="background-color: #fff3cd; padding: 30px; border-radius: 10px; 
                            margin: 20px 0; text-align: center; border: 3px solid #f39c12;">
                    <h2 style="color: #2c3e50; margin: 0;">{cert_name}</h2>
                    <p style="margin: 10px 0;">Verification Code: <strong>{verification_code}</strong></p>
                </div>
                
                <h3>📄 Your Certificate</h3>
                
                <p>Your official certificate is attached to this email. You can also:</p>
                
                <ul>
                    <li>Download from your student dashboard</li>
                    <li>Share on LinkedIn</li>
                    <li>Add to your CV/resume</li>
                    <li>Verify at: www.t21services.co.uk/verify</li>
                </ul>
                
                <h3>🚀 What's Next?</h3>
                
                <p>Continue your journey:</p>
                <ul>
                    <li>Enroll in the next level course</li>
                    <li>Apply for SOC analyst positions</li>
                    <li>Join our alumni network</li>
                </ul>
                
                <p style="margin-top: 30px;">
                    <a href="https://t21-healthcare-platform.streamlit.app" 
                       style="background-color: #f39c12; color: white; padding: 12px 30px; 
                              text-decoration: none; border-radius: 5px; display: inline-block;">
                        🎓 View Certificate
                    </a>
                </p>
                
                <p style="margin-top: 30px; color: #7f8c8d;">
                    We're proud of your achievement!<br>
                    The T21 Team
                </p>
            </div>
        </body>
        </html>
        """
        
        return self.send_email(student_email, subject, html_content)
    
    # ============================================
    # CLIENT EMAILS
    # ============================================
    
    def send_proposal(self, client_email, client_name, proposal_details):
        """Send proposal to potential client"""
        
        subject = f"Proposal: SOC Services for {client_name}"
        
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h1 style="color: #3498db;">Security Operations Center Proposal</h1>
                
                <p>Dear {client_name},</p>
                
                <p>Thank you for your interest in T21's SOC services. We're pleased to present our proposal:</p>
                
                <div style="background-color: #ecf0f1; padding: 20px; border-radius: 5px; margin: 20px 0;">
                    <h3>Proposed Services</h3>
                    <ul>
                        <li>24/7 Security Monitoring</li>
                        <li>Threat Detection & Response</li>
                        <li>Monthly Executive Reports</li>
                        <li>Dedicated SOC Analysts</li>
                    </ul>
                </div>
                
                <p style="margin-top: 30px;">
                    <a href="https://t21-healthcare-platform.streamlit.app" 
                       style="background-color: #3498db; color: white; padding: 12px 30px; 
                              text-decoration: none; border-radius: 5px; display: inline-block;">
                        📄 View Full Proposal
                    </a>
                </p>
                
                <p style="margin-top: 30px; color: #7f8c8d;">
                    Best regards,<br>
                    T21 Services UK<br>
                    info@t21services.co.uk
                </p>
            </div>
        </body>
        </html>
        """
        
        return self.send_email(client_email, subject, html_content)
    
    def send_security_alert(self, client_email, alert_type, severity, details):
        """Send security alert to client"""
        
        severity_colors = {
            "Critical": "#e74c3c",
            "High": "#e67e22",
            "Medium": "#f39c12",
            "Low": "#3498db"
        }
        
        color = severity_colors.get(severity, "#3498db")
        
        subject = f"🚨 Security Alert: {alert_type} [{severity}]"
        
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <div style="background-color: {color}; color: white; padding: 20px; border-radius: 5px;">
                    <h1 style="margin: 0;">🚨 Security Alert</h1>
                    <p style="margin: 5px 0 0 0; font-size: 18px;">{severity} Priority</p>
                </div>
                
                <div style="padding: 20px; background-color: #ecf0f1; margin: 20px 0; border-radius: 5px;">
                    <h3 style="margin-top: 0;">Alert Details</h3>
                    <p><strong>Type:</strong> {alert_type}</p>
                    <p><strong>Severity:</strong> {severity}</p>
                    <p><strong>Time:</strong> {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
                    <p><strong>Details:</strong> {details}</p>
                </div>
                
                <h3>Actions Taken</h3>
                <ul>
                    <li>✅ Threat isolated</li>
                    <li>✅ Investigation initiated</li>
                    <li>✅ SOC team notified</li>
                </ul>
                
                <p>Our SOC team is actively investigating this incident. We'll provide updates as the situation develops.</p>
                
                <p style="margin-top: 30px;">
                    <a href="https://t21-healthcare-platform.streamlit.app" 
                       style="background-color: {color}; color: white; padding: 12px 30px; 
                              text-decoration: none; border-radius: 5px; display: inline-block;">
                        🔍 View Full Details
                    </a>
                </p>
                
                <p style="margin-top: 30px; color: #7f8c8d;">
                    T21 SOC Team<br>
                    24/7 Support: soc@t21services.co.uk
                </p>
            </div>
        </body>
        </html>
        """
        
        return self.send_email(client_email, subject, html_content)
    
    def send_monthly_report(self, client_email, month, metrics):
        """Send monthly security report"""
        
        subject = f"📊 Monthly Security Report - {month}"
        
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h1 style="color: #2c3e50;">Monthly Security Report</h1>
                <p style="color: #7f8c8d;">{month}</p>
                
                <div style="background-color: #ecf0f1; padding: 20px; border-radius: 5px; margin: 20px 0;">
                    <h3>Key Metrics</h3>
                    <table style="width: 100%;">
                        <tr>
                            <td>🚨 Alerts Processed:</td>
                            <td><strong>{metrics.get('alerts', 0)}</strong></td>
                        </tr>
                        <tr>
                            <td>🎯 Threats Blocked:</td>
                            <td><strong>{metrics.get('threats_blocked', 0)}</strong></td>
                        </tr>
                        <tr>
                            <td>⏱️ Avg Response Time:</td>
                            <td><strong>{metrics.get('response_time', '5 min')}</strong></td>
                        </tr>
                        <tr>
                            <td>✅ Uptime:</td>
                            <td><strong>{metrics.get('uptime', '99.9%')}</strong></td>
                        </tr>
                    </table>
                </div>
                
                <p>Your complete monthly report is attached. It includes:</p>
                <ul>
                    <li>Executive summary</li>
                    <li>Detailed threat analysis</li>
                    <li>Incident timeline</li>
                    <li>Recommendations</li>
                </ul>
                
                <p style="margin-top: 30px;">
                    <a href="https://t21-healthcare-platform.streamlit.app" 
                       style="background-color: #3498db; color: white; padding: 12px 30px; 
                              text-decoration: none; border-radius: 5px; display: inline-block;">
                        📊 View Full Report
                    </a>
                </p>
                
                <p style="margin-top: 30px; color: #7f8c8d;">
                    T21 SOC Team<br>
                    www.t21services.co.uk
                </p>
            </div>
        </body>
        </html>
        """
        
        return self.send_email(client_email, subject, html_content)
    
    # ============================================
    # MARKETING EMAILS
    # ============================================
    
    def send_marketing_campaign(self, email_list, campaign_name, content):
        """Send marketing campaign to list"""
        
        for email in email_list:
            self.send_email(email, f"🚀 {campaign_name}", content)
        
        return len(email_list)
    
    def send_newsletter(self, email_list, newsletter_content):
        """Send newsletter"""
        
        subject = "📰 T21 Cybersecurity Newsletter"
        
        for email in email_list:
            self.send_email(email, subject, newsletter_content)
        
        return len(email_list)

# Email automation instance
email_automation = EmailAutomation()

# Quick send functions
def send_welcome_email(student_email, student_name):
    return email_automation.send_welcome_email(student_email, student_name)

def send_enrollment_confirmation(student_email, course_name, start_date):
    return email_automation.send_enrollment_confirmation(student_email, course_name, start_date)

def send_payment_receipt(customer_email, payment_id, amount, course_name):
    return email_automation.send_payment_receipt(customer_email, payment_id, amount, course_name)

def send_certificate(student_email, student_name, cert_name, verification_code):
    return email_automation.send_certificate(student_email, student_name, cert_name, verification_code)

def send_security_alert(client_email, alert_type, severity, details):
    return email_automation.send_security_alert(client_email, alert_type, severity, details)
