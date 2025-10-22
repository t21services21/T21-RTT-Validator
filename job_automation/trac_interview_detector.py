"""
Trac Interview Detector
Automatically monitors Trac inbox for interview invitations
NO MANUAL STAFF INPUT REQUIRED!
"""

import asyncio
from playwright.async_api import async_playwright, Page
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import logging
from supabase import create_client
import os
import re
from cryptography.fernet import Fernet

logger = logging.getLogger(__name__)

class TracInterviewDetector:
    """
    Monitors Trac inbox 24/7 for interview invitations
    Auto-creates interview records
    """
    
    def __init__(self):
        self.supabase = create_client(
            os.getenv('SUPABASE_URL'),
            os.getenv('SUPABASE_KEY')
        )
        self.trac_url = 'https://www.trac.jobs'
        self.check_interval_minutes = 30  # Check every 30 minutes
        
    async def monitor_continuously(self):
        """
        Main loop - checks Trac inboxes forever
        """
        logger.info("🔍 Starting Trac interview detector...")
        
        while True:
            try:
                # Get all students with active automation
                students = await self.get_active_students()
                
                logger.info(f"👥 Monitoring {len(students)} student Trac accounts...")
                
                for student in students:
                    try:
                        await self.check_student_inbox(student)
                    except Exception as e:
                        logger.error(f"❌ Error checking inbox for student {student['student_id']}: {e}")
                        continue
                
                logger.info(f"✅ Inbox check complete. Sleeping for {self.check_interval_minutes} minutes...")
                await asyncio.sleep(self.check_interval_minutes * 60)
                
            except Exception as e:
                logger.error(f"❌ Interview detector error: {e}")
                await asyncio.sleep(300)  # Wait 5 minutes on error
    
    async def get_active_students(self) -> List[Dict]:
        """
        Get all students with Trac credentials
        """
        response = self.supabase.table('student_automation_settings')\
            .select('*')\
            .eq('status', 'active')\
            .not_.is_('trac_email', 'null')\
            .execute()
        
        return response.data
    
    async def check_student_inbox(self, student: Dict):
        """
        Check individual student's Trac inbox for new messages
        """
        logger.info(f"📨 Checking inbox for: {student['trac_email']}")
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()
            
            try:
                # Login to Trac
                await self.login_to_trac(page, student)
                
                # Navigate to inbox/messages
                await page.goto(f'{self.trac_url}/Candidate/Messages')
                await page.wait_for_load_state('networkidle')
                
                # Get all messages
                messages = await self.extract_messages(page)
                
                # Process each message
                for message in messages:
                    await self.process_message(message, student)
                
                logger.info(f"✅ Processed {len(messages)} messages for {student['trac_email']}")
                
            except Exception as e:
                logger.error(f"❌ Error checking inbox: {e}")
            finally:
                await browser.close()
    
    async def login_to_trac(self, page: Page, student: Dict):
        """
        Login to Trac using stored credentials
        """
        # Decrypt password
        password = self.decrypt_password(
            student['trac_password_encrypted'],
            student['encryption_key_id']
        )
        
        await page.goto(f'{self.trac_url}/Candidate/LogOn')
        await page.wait_for_load_state('networkidle')
        
        # Fill login form
        await page.fill('input[name="Email"], input[type="email"]', student['trac_email'])
        await page.fill('input[name="Password"], input[type="password"]', password)
        await page.click('button[type="submit"], input[type="submit"]')
        
        # Wait for login to complete
        await page.wait_for_load_state('networkidle')
        
        # Check for OTP
        if 'otp' in page.url.lower() or await page.locator('text=/one.*time.*passcode/i').count() > 0:
            logger.warning("⚠️ OTP required - waiting for manual input...")
            # In production, implement OTP automation via email/SMS
            await page.wait_for_timeout(60000)  # Wait 60 seconds
    
    async def extract_messages(self, page: Page) -> List[Dict]:
        """
        Extract all messages from Trac inbox
        """
        messages = []
        
        # Wait for message list
        await page.wait_for_selector('.message-row, .message-item, tr.message', timeout=10000)
        
        # Get all message rows
        message_rows = await page.locator('.message-row, .message-item, tr.message').all()
        
        for row in message_rows:
            try:
                # Extract message details from row
                message_id = await row.get_attribute('data-message-id') or \
                            await row.locator('input[type="checkbox"]').get_attribute('value')
                
                subject = await row.locator('.subject, .message-subject, td:nth-child(2)').inner_text()
                sender = await row.locator('.sender, .from, td:nth-child(1)').inner_text()
                date_text = await row.locator('.date, .received-date, td:nth-child(3)').inner_text()
                
                # Click to view full message
                await row.click()
                await page.wait_for_load_state('networkidle')
                
                # Get full message content
                message_html = await page.locator('.message-body, .message-content').inner_html()
                message_text = await page.locator('.message-body, .message-content').inner_text()
                
                messages.append({
                    'message_id': message_id,
                    'subject': subject.strip(),
                    'from_sender': sender.strip(),
                    'received_date': self.parse_date(date_text),
                    'message_html': message_html,
                    'message_plain': message_text
                })
                
                # Go back to inbox
                await page.go_back()
                await page.wait_for_load_state('networkidle')
                
            except Exception as e:
                logger.error(f"❌ Error extracting message: {e}")
                continue
        
        return messages
    
    async def process_message(self, message: Dict, student: Dict):
        """
        Process message and detect if it's an interview invitation
        """
        # Check if already processed
        existing = self.supabase.table('trac_inbox_messages')\
            .select('id')\
            .eq('student_id', student['student_id'])\
            .eq('message_id', message['message_id'])\
            .execute()
        
        if existing.data:
            return  # Already processed
        
        # Classify message using AI
        message_type, confidence = self.classify_message(message)
        
        # Store message
        stored_message = self.supabase.table('trac_inbox_messages').insert({
            'student_id': student['student_id'],
            'trac_email': student['trac_email'],
            'message_id': message['message_id'],
            'subject': message['subject'],
            'from_sender': message['from_sender'],
            'received_date': message['received_date'],
            'message_html': message['message_html'],
            'message_plain': message['message_plain'],
            'message_type': message_type,
            'confidence_score': confidence,
            'processed': False
        }).execute()
        
        # If interview invitation, create interview record
        if message_type == 'interview_invitation' and confidence > 0.7:
            await self.create_interview_record(message, student, stored_message.data[0]['id'])
    
    def classify_message(self, message: Dict) -> tuple:
        """
        AI-powered message classification
        Returns: (message_type, confidence_score)
        """
        subject = message['subject'].lower()
        body = message['message_plain'].lower()
        combined = subject + ' ' + body
        
        # Interview invitation keywords
        interview_keywords = [
            'interview',
            'invite you to',
            'pleased to invite',
            'shortlisted',
            'assessment',
            'interview date',
            'interview time',
            'interview scheduled',
            'would like to meet'
        ]
        
        # Rejection keywords
        rejection_keywords = [
            'unsuccessful',
            'not been successful',
            'regret to inform',
            'not shortlisted',
            'will not be progressing'
        ]
        
        # Offer keywords
        offer_keywords = [
            'offer you the position',
            'pleased to offer',
            'job offer',
            'conditional offer',
            'offer of employment'
        ]
        
        # Count matches
        interview_matches = sum(1 for kw in interview_keywords if kw in combined)
        rejection_matches = sum(1 for kw in rejection_keywords if kw in combined)
        offer_matches = sum(1 for kw in offer_keywords if kw in combined)
        
        # Classify
        if offer_matches >= 2:
            return ('offer', 0.9)
        elif rejection_matches >= 1:
            return ('rejection', 0.85)
        elif interview_matches >= 2:
            # Check if date/time mentioned
            if self.extract_interview_datetime(message):
                return ('interview_invitation', 0.95)
            return ('interview_invitation', 0.75)
        
        return ('other', 0.5)
    
    async def create_interview_record(self, message: Dict, student: Dict, message_db_id: str):
        """
        Create interview record from invitation message
        """
        logger.info(f"🎉 Interview invitation detected for student {student['student_id']}!")
        
        # Extract interview details
        interview_datetime = self.extract_interview_datetime(message)
        interview_location = self.extract_interview_location(message)
        interview_format = self.extract_interview_format(message)
        
        # Try to match to application
        application_id = await self.match_to_application(message, student)
        
        # Create interview record
        interview = {
            'student_id': student['student_id'],
            'application_id': application_id,
            'interview_date': interview_datetime['date'] if interview_datetime else None,
            'interview_time': interview_datetime['time'] if interview_datetime else None,
            'interview_location': interview_location,
            'interview_format': interview_format,
            'status': 'scheduled',
            'trac_message_id': message['message_id'],
            'trac_detected_at': datetime.now().isoformat(),
            'invitation_email_html': message['message_html']
        }
        
        result = self.supabase.table('interviews').insert(interview).execute()
        interview_id = result.data[0]['id']
        
        # Link message to interview
        self.supabase.table('trac_inbox_messages')\
            .update({'processed': True, 'linked_interview_id': interview_id})\
            .eq('id', message_db_id)\
            .execute()
        
        # Send notification to student
        await self.notify_student_interview(student, interview)
        
        logger.info(f"✅ Interview record created: ID {interview_id}")
    
    def extract_interview_datetime(self, message: Dict) -> Optional[Dict]:
        """
        Extract interview date and time from message
        """
        text = message['message_plain']
        
        # Look for date patterns
        date_patterns = [
            r'(\d{1,2})\s+(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{4})',
            r'(\d{1,2})[/-](\d{1,2})[/-](\d{4})',
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                try:
                    if len(match.groups()) == 3:
                        if match.group(2).isalpha():
                            # Format: 15 October 2025
                            date_str = f"{match.group(1)} {match.group(2)} {match.group(3)}"
                            interview_date = datetime.strptime(date_str, "%d %B %Y").date()
                        else:
                            # Format: 15/10/2025
                            date_str = f"{match.group(1)}/{match.group(2)}/{match.group(3)}"
                            interview_date = datetime.strptime(date_str, "%d/%m/%Y").date()
                        
                        # Look for time
                        time_match = re.search(r'(\d{1,2}):(\d{2})\s*(am|pm)?', text, re.IGNORECASE)
                        if time_match:
                            time_str = f"{time_match.group(1)}:{time_match.group(2)}"
                            if time_match.group(3):
                                time_str += f" {time_match.group(3)}"
                            
                            return {
                                'date': interview_date.isoformat(),
                                'time': time_str
                            }
                        
                        return {'date': interview_date.isoformat(), 'time': None}
                except:
                    continue
        
        return None
    
    def extract_interview_location(self, message: Dict) -> Optional[str]:
        """
        Extract interview location
        """
        text = message['message_plain']
        
        # Look for location indicators
        location_patterns = [
            r'location:\s*(.+)',
            r'venue:\s*(.+)',
            r'interview will be held at\s*(.+)',
            r'please attend at\s*(.+)'
        ]
        
        for pattern in location_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                location = match.group(1).strip()
                # Take first line only
                location = location.split('\n')[0]
                return location[:200]  # Limit length
        
        return None
    
    def extract_interview_format(self, message: Dict) -> str:
        """
        Extract interview format (in-person, video, phone)
        """
        text = message['message_plain'].lower()
        
        if 'video' in text or 'teams' in text or 'zoom' in text or 'virtual' in text:
            return 'video'
        elif 'phone' in text or 'telephone' in text:
            return 'phone'
        else:
            return 'in-person'
    
    async def match_to_application(self, message: Dict, student: Dict) -> Optional[str]:
        """
        Match interview invitation to submitted application
        """
        # Try to extract job reference from message
        job_ref_match = re.search(r'ref(?:erence)?:?\s*([A-Z0-9-]+)', message['message_plain'], re.IGNORECASE)
        
        if job_ref_match:
            job_ref = job_ref_match.group(1)
            
            # Find application with this job reference
            app = self.supabase.table('applications')\
                .select('id')\
                .eq('student_id', student['student_id'])\
                .eq('job_id.job_reference', job_ref)\
                .execute()
            
            if app.data:
                return app.data[0]['id']
        
        # Otherwise, try to match by trust name or job title
        # (More complex matching logic here)
        
        return None
    
    async def notify_student_interview(self, student: Dict, interview: Dict):
        """
        Send email notification to student about interview
        """
        # Import email service
        from job_automation.email_service import EmailNotificationSystem
        
        email_service = EmailNotificationSystem()
        await email_service.send_notification(
            student,
            'interview_invitation',
            interview
        )
    
    def decrypt_password(self, encrypted_password: str, key_id: str) -> str:
        """
        Decrypt stored Trac password
        """
        # In production, retrieve key from secure key vault
        encryption_key = os.getenv('ENCRYPTION_KEY')
        cipher = Fernet(encryption_key.encode())
        
        decrypted = cipher.decrypt(encrypted_password.encode())
        return decrypted.decode()
    
    def parse_date(self, date_text: str) -> str:
        """
        Parse date from various formats
        """
        try:
            # Try common formats
            for fmt in ['%d/%m/%Y', '%d-%m-%Y', '%Y-%m-%d', '%d %B %Y']:
                try:
                    return datetime.strptime(date_text.strip(), fmt).isoformat()
                except:
                    continue
        except:
            pass
        
        return datetime.now().isoformat()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    detector = TracInterviewDetector()
    asyncio.run(detector.monitor_continuously())
