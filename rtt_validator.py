"""
T21 RTT Pathway Validation Logic Module
Core validation functions for NHS RTT pathways

ENHANCED WITH AI CAPABILITIES:
- NLP Letter Reading (OpenAI GPT-4)
- Audio Transcription (Whisper)
- Handwriting OCR (Vision API)
- Auto-Fix Engine
- Bulk Processing
"""

from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import json
import re

# AI ENHANCEMENTS - Safe imports with fallbacks
try:
    from nlp_letter_reader import NLPLetterReader
    NLP_AVAILABLE = True
except:
    NLP_AVAILABLE = False

try:
    from audio_transcription_service import AudioTranscriptionService
    AUDIO_AVAILABLE = True
except:
    AUDIO_AVAILABLE = False

try:
    from handwriting_ocr_service import HandwritingOCRService
    OCR_AVAILABLE = True
except:
    OCR_AVAILABLE = False

try:
    from auto_fix_engine import AutoFixEngine
    AUTOFIX_AVAILABLE = True
except:
    AUTOFIX_AVAILABLE = False

try:
    from batch_validation_engine import BatchValidationEngine
    BATCH_AVAILABLE = True
except:
    BATCH_AVAILABLE = False


def parse_date(date_str: str) -> Optional[datetime]:
    """Parse date string in various formats (DD/MM/YYYY, YYYY-MM-DD, etc.)"""
    if not date_str or date_str.strip() == "":
        return None
    
    date_str = date_str.strip()
    
    # Try DD/MM/YYYY format first
    formats = [
        "%d/%m/%Y",
        "%d-%m-%Y",
        "%Y-%m-%d",
        "%Y/%m/%d",
        "%d.%m.%Y"
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except:
            continue
    
    return None


def calculate_weeks(start_date: datetime, end_date: datetime, pause_weeks: int = 0) -> int:
    """Calculate weeks between two dates minus any pause weeks"""
    if not start_date or not end_date:
        return 0
    delta = end_date - start_date
    total_weeks = delta.days // 7
    adjusted_weeks = total_weeks - pause_weeks
    return max(0, adjusted_weeks)


def get_breach_flag(weeks: int) -> str:
    """Determine breach tier based on weeks elapsed"""
    if weeks >= 52:
        return "52-week breach"
    elif weeks >= 26:
        return "26-week breach"
    elif weeks > 18:
        return "18-week breach"
    else:
        return "None"


def validate_pathway(data: Dict) -> Dict:
    """
    Main pathway validator (T21 RTT Pathway Intelligence v1.1)
    """
    # Parse dates
    referral_date = parse_date(data.get('referral_date', ''))
    first_appt_date = parse_date(data.get('first_appt_date', ''))
    treatment_date = parse_date(data.get('treatment_date', ''))
    
    # Extract pause information
    pause_text = data.get('delays_pauses', '').lower()
    pause_weeks = 0
    if 'week' in pause_text:
        # Try to extract number of weeks
        import re
        match = re.search(r'(\d+)[\s-]*week', pause_text)
        if match:
            pause_weeks = int(match.group(1))
    
    # Current event code
    current_code = data.get('current_rtt_event', '30')
    
    # Calculate weeks
    if referral_date and treatment_date:
        total_weeks = calculate_weeks(referral_date, treatment_date, pause_weeks)
    elif referral_date:
        total_weeks = calculate_weeks(referral_date, datetime.now(), pause_weeks)
    else:
        total_weeks = 0
    
    # Determine status
    if treatment_date:
        clock_status = "Stopped"
        recommended_action = "Stop"
    elif data.get('active_monitoring') in ['31_patient', '32_clinician']:
        clock_status = "Paused"
        recommended_action = "Pause"
    elif pause_weeks > 0:
        clock_status = "Paused"
        recommended_action = "Continue"
    elif referral_date:
        clock_status = "Active"
        recommended_action = "Continue"
    else:
        clock_status = "Incomplete"
        recommended_action = "Start"
    
    breach_flag = get_breach_flag(total_weeks)
    
    # Build explanation
    explanation = f"RTT pathway from {data.get('referral_date', 'N/A')} to "
    if treatment_date:
        explanation += f"{data.get('treatment_date')}. "
    else:
        explanation += "ongoing. "
    
    if pause_weeks > 0:
        explanation += f"Patient-initiated {pause_weeks}-week delay paused clock. "
    
    explanation += f"Total adjusted RTT weeks: {total_weeks}. "
    
    if breach_flag != "None":
        explanation += f"BREACH: {breach_flag}."
    else:
        explanation += "No breach."
    
    # PAS updates
    pas_updates = [
        f"Record code 10 (First activity) on first appointment date",
        f"Record code 92 for diagnostics if standalone event",
        f"Record code 20 for subsequent activities (decision to treat, pre-op)",
    ]
    
    if pause_weeks > 0:
        pas_updates.append(f"Document {pause_weeks}-week patient-initiated pause with start/end dates")
    
    if treatment_date:
        pas_updates.append(f"Confirm code 30 with treatment date {data.get('treatment_date')}")
        pas_updates.append(f"Set clock stop date as {data.get('treatment_date')}")
        pas_updates.append("Mark pathway as closed")
    
    # Generate comment line
    if treatment_date:
        comment_line = f"CS{data.get('treatment_date', '')}/{current_code} – FDT STARTED. RTT CLOSED {total_weeks}WKS. GP COPY SENT."
    elif data.get('active_monitoring'):
        am_code = '32' if '32' in data.get('active_monitoring', '') else '31'
        comment_line = f"AM{am_code}/{data.get('am_start_date', '')} – UNDER REVIEW. CONTINUE MONITORING."
    else:
        comment_line = f"RTT ACTIVE/{data.get('referral_date', '')} – {total_weeks}WKS ELAPSED. CONTINUE CODE 20."
    
    return {
        "RTT_Clock_Status": clock_status,
        "Weeks_Elapsed": str(total_weeks),
        "RTT_Code": current_code,
        "Breach_Flag": breach_flag,
        "Recommended_Action": recommended_action,
        "Duplicate_Code_Issues": [],
        "What_To_Change_In_PAS": pas_updates,
        "Explanation": explanation,
        "Confidence_Level": "High" if referral_date and (treatment_date or first_appt_date) else "Medium",
        "Policy_Reference": "NHS England RTT Rules and Guidance v17.0",
        "Standardised_Comment_Line": comment_line
    }


def validate_clinic_letter(letter_text: str, pas_summary: Dict) -> Dict:
    """
    Clinic Letter Interpreter (T21 v1.2)
    Interprets NHS letters and determines correct RTT code based on letter type and content
    
    Key principle: Distinguish between:
    1. PAST ACTIONS - What has already been done (should be in PAS)
    2. FUTURE ACTIONS - What needs to be done next (check if ordered/booked)
    """
    letter_lower = letter_text.lower()
    
    # ============================================
    # PARSE LETTER INTO PAST vs FUTURE ACTIONS
    # ============================================
    
    # PAST TENSE INDICATORS (things already done)
    past_indicators = [
        'was performed', 'were performed', 'has been', 'have been',
        'performed appropriately', 'results from', 'findings from',
        'showed', 'demonstrated', 'revealed', 'indicated',
        'underwent', 'received', 'completed', 'was done',
        'have returned', 'came back', 'test showed'
    ]
    
    # FUTURE/REQUEST INDICATORS (things to be done)
    future_indicators = [
        'please arrange', 'please book', 'please order',
        'i recommend', 'would recommend', 'advise',
        'needs to', 'should', 'must', 'require',
        'to be ordered', 'to be booked', 'to arrange',
        'kindly arrange', 'arrange for', 'book for'
    ]
    
    def is_past_action(text, keyword, window=150):
        """
        Check if a keyword appears in PAST context (already done) vs FUTURE (to be ordered)
        Returns: 'past', 'future', or 'unclear'
        
        Works for ANY action: appointments, tests, treatments, letters, waiting lists, etc.
        """
        # Find all occurrences of the keyword
        idx = text.find(keyword)
        if idx == -1:
            return 'unclear'
        
        # Get surrounding context (before and after)
        start = max(0, idx - window)
        end = min(len(text), idx + len(keyword) + window)
        context = text[start:end].lower()
        
        # Check for past indicators
        for indicator in past_indicators:
            if indicator in context:
                return 'past'
        
        # Check for future indicators
        for indicator in future_indicators:
            if indicator in context:
                return 'future'
        
        # Check for results/findings context (past)
        if any(word in context for word in ['results', 'findings', 'report', 'showed']):
            return 'past'
        
        # Check for completion context (past)
        if any(word in context for word in ['completed', 'done', 'sent', 'added', 'booked already']):
            return 'past'
        
        # Check for ordering/requesting context (future)
        if any(word in context for word in ['please book', 'please arrange', 'please order', 'please add', 'kindly', 'request']):
            return 'future'
        
        # Check for planning context (future)
        if any(word in context for word in ['plan:', 'to be', 'will be', 'shall be', 'needs to be']):
            return 'future'
        
        return 'unclear'
    
    def parse_actions_from_letter(text):
        """
        Extract all actions from letter and categorize as PAST (done) or FUTURE (to do)
        Returns: {
            'appointments': {'past': [], 'future': []},
            'diagnostics': {'past': [], 'future': []},
            'waiting_list': {'past': [], 'future': []},
            'gp_letters': {'past': [], 'future': []},
            'treatment': {'past': [], 'future': []}
        }
        """
        actions = {
            'appointments': {'past': [], 'future': []},
            'diagnostics': {'past': [], 'future': []},
            'waiting_list': {'past': [], 'future': []},
            'gp_letters': {'past': [], 'future': []},
            'treatment': {'past': [], 'future': []},
            'referrals': {'past': [], 'future': []}
        }
        
        text_lower = text.lower()
        
        # APPOINTMENTS
        appt_keywords = ['appointment', 'follow-up', 'follow up', 'review appointment', 'clinic']
        for keyword in appt_keywords:
            if keyword in text_lower:
                action_type = is_past_action(text_lower, keyword)
                if action_type == 'past':
                    actions['appointments']['past'].append(keyword)
                elif action_type == 'future':
                    actions['appointments']['future'].append(keyword)
        
        # WAITING LIST
        wl_keywords = ['waiting list', 'surgical list', 'list for surgery', 'add to list']
        for keyword in wl_keywords:
            if keyword in text_lower:
                action_type = is_past_action(text_lower, keyword)
                if action_type == 'past':
                    actions['waiting_list']['past'].append(keyword)
                elif action_type == 'future':
                    actions['waiting_list']['future'].append(keyword)
        
        # GP LETTERS
        gp_keywords = ['gp letter', 'copy to gp', 'inform gp', 'letter to gp']
        for keyword in gp_keywords:
            if keyword in text_lower:
                action_type = is_past_action(text_lower, keyword)
                if action_type == 'past':
                    actions['gp_letters']['past'].append(keyword)
                elif action_type == 'future':
                    actions['gp_letters']['future'].append(keyword)
        
        # TREATMENT
        treatment_keywords = ['surgery', 'operation', 'procedure', 'treatment']
        for keyword in treatment_keywords:
            if keyword in text_lower:
                action_type = is_past_action(text_lower, keyword)
                if action_type == 'past':
                    actions['treatment']['past'].append(keyword)
                elif action_type == 'future':
                    actions['treatment']['future'].append(keyword)
        
        return actions
    
    # CODE 10 - REFERRAL LETTERS (PATHWAY START)
    # Check for GP/Consultant referral patterns FIRST
    referral_indicators = [
        'i am writing to refer',
        'i would like to refer',
        'please see this patient',
        're: referral',
        'referral for',
        'referred to your service',
        'referring this patient',
        'request referral',
        'kindly accept this referral'
    ]
    
    if any(indicator in letter_lower for indicator in referral_indicators):
        rtt_code = "10"
        rtt_action = "Start"
        clock_status = "Active"
        explanation = "GP/Consultant referral letter detected. Code 10 starts new RTT clock. This is the FIRST activity in the pathway."
    
    # CODE 30 - FIRST DEFINITIVE TREATMENT
    elif any(phrase in letter_lower for phrase in ['surgery performed', 'procedure completed', 'treatment started', 'operation performed', 'underwent surgery', 'treatment commenced']):
        rtt_code = "30"
        rtt_action = "Stop"
        clock_status = "Stopped"
        explanation = "First definitive treatment documented in letter. Code 30 stops RTT clock."
    
    # CODE 34 - DISCHARGE / NO TREATMENT NEEDED
    # Check for discharge/no treatment patterns EARLY (before diagnostic detection)
    elif any(phrase in letter_lower for phrase in [
        'discharge', 
        'no further treatment', 
        'back to gp', 
        'treatment not required',
        'no intervention is needed',
        'no intervention needed',
        'no medical intervention',
        'intervention is needed',  # catches "no...intervention is needed"
        'discharged to gp',
        'no treatment needed',
        'no treatment is required',
        'do not believe that any',
        'results...normal',  # Results normal often means discharge
        'routine follow'  # If just routine follow-up, likely discharge
    ]) or ('intervention' in letter_lower and 'not' in letter_lower and 'needed' in letter_lower):
        rtt_code = "34"
        rtt_action = "Stop"
        clock_status = "Stopped"
        explanation = "Clinical decision not to treat / discharge documented. Code 34 stops RTT clock."
    
    # CODE 35 - PATIENT DECLINED
    elif any(phrase in letter_lower for phrase in ['patient declined', 'refused treatment', 'patient refuses', 'declined the offer']):
        rtt_code = "35"
        rtt_action = "Stop"
        clock_status = "Stopped"
        explanation = "Patient declined offered treatment. Code 35 stops RTT clock."
    
    # CODE 33 - DNA (Did Not Attend)
    elif any(phrase in letter_lower for phrase in ['did not attend', 'dna', 'patient did not attend', 'failed to attend']):
        rtt_code = "33"
        rtt_action = "Continue"
        clock_status = "Active"
        explanation = "Patient DNA (Did Not Attend) documented. Code 33 - rebook within trust policy."
    
    # CODE 31/32 - ACTIVE MONITORING
    elif any(phrase in letter_lower for phrase in ['active monitoring', 'watchful waiting', 'watch and wait', 'conservative management', 'observe for']):
        if any(phrase in letter_lower for phrase in ['patient request', 'patient wishes', 'patient prefers']):
            rtt_code = "31"
            explanation = "Active monitoring initiated by patient request. Code 31 pauses RTT clock."
        else:
            rtt_code = "32"
            explanation = "Active monitoring initiated by clinician decision. Code 32 pauses RTT clock."
        rtt_action = "Pause"
        clock_status = "Paused"
    
    # CODE 21 - INTER-PROVIDER TRANSFER
    elif any(phrase in letter_lower for phrase in ['transfer to', 'transferring to', 'referred to another provider', 'transfer of care']):
        rtt_code = "21"
        rtt_action = "Transfer"
        clock_status = "Transferred"
        explanation = "Inter-provider transfer documented. Code 21 - clock transfers to receiving provider."
    
    # CODE 20 - DECISION TO TREAT / SUBSEQUENT ACTIVITY
    elif any(phrase in letter_lower for phrase in ['list for surgery', 'proceed to', 'book for', 'waiting list', 'decision to treat', 'plan:', 'management plan']):
        rtt_code = "20"
        rtt_action = "Continue"
        clock_status = "Active"
        explanation = "Decision to treat made / subsequent activity in RTT pathway. Clock continues with code 20 until treatment starts."
    
    # DEFAULT - SUBSEQUENT ACTIVITY
    else:
        rtt_code = "20"
        rtt_action = "Continue"
        clock_status = "Active"
        explanation = "Clinic outcome letter - subsequent activity in RTT pathway. Clock continues with code 20."
    
    # Check required actions based on letter type and code
    actions_required = []
    actions_in_pas = []
    gaps = []
    
    # CODE 10 (Referral) - COMPREHENSIVE VALIDATION & VERIFICATION
    if rtt_code == "10":
        # ============================================
        # SECTION 1: REFERRAL LOGGED IN SYSTEM CHECK
        # ============================================
        actions_required.append("CHECK: Referral logged in PAS system (Y/N)")
        gaps.append("VERIFY: Is referral actually recorded in system? (Check referral log)")
        
        # ============================================
        # SECTION 2: PATIENT DEMOGRAPHICS VALIDATION
        # ============================================
        actions_required.append("CHECK: Patient exists in PAS (Y/N)")
        actions_required.append("CHECK: Patient name on letter matches PAS (Y/N)")
        actions_required.append("CHECK: NHS number on letter matches PAS (Y/N)")
        actions_required.append("CHECK: DOB on letter matches PAS (Y/N)")
        actions_required.append("CHECK: Address correct in PAS (Y/N)")
        gaps.append("VERIFY: Patient name - Letter vs PAS")
        gaps.append("VERIFY: NHS number - Letter vs PAS")
        gaps.append("VERIFY: DOB - Letter vs PAS")
        
        # ============================================
        # SECTION 3: REFERRAL DETAILS VALIDATION
        # ============================================
        actions_required.append("CHECK: Referral source (GP/Consultant) recorded correctly (Y/N)")
        actions_required.append("CHECK: Referring GP name matches letter (Y/N)")
        actions_required.append("CHECK: GP practice address recorded (Y/N)")
        actions_required.append("CHECK: Specialty correctly assigned (Y/N)")
        actions_required.append("CHECK: Referral date matches letter date (Y/N)")
        gaps.append("VERIFY: Referral date in system = Referral date on letter")
        gaps.append("VERIFY: Referring GP details match letter")
        
        # ============================================
        # SECTION 4: PATHWAY CREATION CHECK
        # ============================================
        actions_required.append("CHECK: RTT pathway created in system (Y/N)")
        actions_required.append("CHECK: Pathway number assigned (Y/N)")
        actions_required.append("CHECK: District number assigned (Y/N)")
        actions_required.append("CHECK: Clock start date set = referral date (Y/N)")
        actions_required.append("CHECK: Clock status = Active (Y/N)")
        gaps.append("VERIFY: Pathway number assigned and recorded")
        gaps.append("VERIFY: Clock start date = referral date")
        
        # ============================================
        # SECTION 5: PARTIAL BOOKING LIST (PBL) CHECK
        # ============================================
        if any(phrase in letter_lower for phrase in ['partial booking', 'pbl', 'waiting for appointment', 'await appointment']):
            actions_required.append("CHECK: Patient added to Partial Booking List (PBL) (Y/N)")
            actions_required.append("CHECK: PBL entry date recorded (Y/N)")
            gaps.append("VERIFY: Patient on Partial Booking List - CHECK SYSTEM")
            gaps.append("FLAG: Letter says add to PBL - confirm PBL entry exists")
        else:
            # Default - all referrals should go to PBL until first appointment
            actions_required.append("CHECK: Patient on Partial Booking List (Y/N)")
            gaps.append("VERIFY: Patient should be on PBL awaiting first appointment")
        
        # ============================================
        # SECTION 6: FIRST APPOINTMENT BOOKING CHECK
        # ============================================
        if any(phrase in letter_lower for phrase in ['book appointment', 'first appointment', 'first outpatient', 'opa']):
            actions_required.append("CHECK: First appointment booked (Y/N)")
            actions_required.append("CHECK: Appointment date recorded (Y/N)")
            actions_required.append("CHECK: Appointment within target timeframe (Y/N)")
            gaps.append("VERIFY: First appointment booked - CHECK DIARY/SYSTEM")
            gaps.append("FLAG: Letter requests appointment - check if actually booked")
        
        # ============================================
        # SECTION 7: INVESTIGATIONS/DIAGNOSTICS CHECK
        # ============================================
        # Specific diagnostic tests mentioned in letter
        diagnostic_tests = {
            'ecg': 'ECG/Electrocardiogram',
            'angiogram': 'Coronary Angiogram',
            'mri': 'MRI Scan',
            'ct': 'CT Scan',
            'ultrasound': 'Ultrasound',
            'echo': 'Echocardiogram',
            'x-ray': 'X-Ray',
            'blood': 'Blood Tests',
            'biopsy': 'Biopsy'
        }
        
        tests_found = []
        for test_key, test_name in diagnostic_tests.items():
            if test_key in letter_lower:
                tests_found.append(test_name)
                actions_required.append(f"CHECK: {test_name} ordered in system (Y/N)")
                actions_required.append(f"CHECK: {test_name} booking date recorded (Y/N)")
                gaps.append(f"VERIFY: {test_name} - CHECK if booked in diagnostics system")
                gaps.append(f"FLAG: Letter requests {test_name} - confirm order exists")
        
        if tests_found:
            actions_required.append("CHECK: All requested investigations ordered (Y/N)")
        
        # ============================================
        # SECTION 8: PRIORITY/URGENCY CHECK
        # ============================================
        if any(word in letter_lower for word in ['urgent', '2ww', 'two week wait', 'cancer', 'suspected cancer']):
            actions_required.append("CHECK: Urgent/2WW flag set in system (Y/N)")
            actions_required.append("CHECK: Priority booking expedited (Y/N)")
            gaps.append("VERIFY: Urgent referral flag - CHECK PRIORITY STATUS")
            gaps.append("FLAG: URGENT/2WW - must be seen within 2 weeks")
        
        # ============================================
        # SECTION 9: DUPLICATE PATHWAY CHECK
        # ============================================
        actions_required.append("CHECK: No duplicate pathway for same specialty (Y/N)")
        gaps.append("VERIFY: Search for duplicate pathways (same patient, same specialty, last 6 months)")
        
        # ============================================
        # SECTION 10: ACKNOWLEDGMENT LETTER CHECK
        # ============================================
        actions_required.append("CHECK: Acknowledgment letter sent to GP (Y/N)")
        actions_required.append("CHECK: Acknowledgment date recorded (Y/N)")
        gaps.append("VERIFY: GP acknowledgment sent - CHECK correspondence log")
    
    # ============================================
    # CODE 20 - CLINIC OUTCOME / DECISION TO TREAT
    # ============================================
    elif rtt_code == "20":
        # WAITING LIST CHECKS (with past/future logic)
        if any(phrase in letter_lower for phrase in ['list for surgery', 'waiting list', 'surgical list', 'add to list', 'wl']):
            # Check if patient ALREADY added or NEEDS TO BE added
            wl_action = is_past_action(letter_lower, 'waiting list')
            
            if wl_action == 'future' or wl_action == 'unclear':
                # Patient NEEDS TO BE added to WL
                actions_required.append("CHECK: Patient added to surgical waiting list (Y/N)")
                actions_required.append("CHECK: Waiting list type recorded (Y/N)")
                actions_required.append("CHECK: Waiting list entry date = letter date (Y/N)")
                actions_required.append("CHECK: Procedure/operation recorded on WL (Y/N)")
                actions_required.append("CHECK: Specialty correct on WL entry (Y/N)")
                
                if pas_summary.get('waiting_list') == 'Y':
                    actions_in_pas.append("✅ Patient added to waiting list")
                else:
                    gaps.append("FLAG: Letter says add to waiting list - NOT FOUND IN SYSTEM")
                    gaps.append("VERIFY: Check WL system for patient entry")
            
            elif wl_action == 'past':
                # Patient ALREADY added - verify it's correct
                actions_required.append("VERIFY: Waiting list entry exists and is correct (Y/N)")
                actions_required.append("VERIFY: WL entry date matches letter (Y/N)")
        
        # TCI DATE (To Come In Date) CHECKS
        if any(phrase in letter_lower for phrase in ['tci', 'to come in', 'date for surgery', 'theatre date']):
            actions_required.append("CHECK: TCI date set in system (Y/N)")
            actions_required.append("CHECK: TCI date within 18 weeks of clock start (Y/N)")
            gaps.append("VERIFY: TCI date recorded - CHECK waiting list")
        
        # DIAGNOSTICS/INVESTIGATIONS CHECKS
        # Distinguish between PAST (already done) and FUTURE (to be ordered)
        diagnostic_keywords = {
            'ecg': 'ECG',
            'angiogram': 'Angiogram',
            'coronary angiography': 'Coronary Angiogram',
            'mri': 'MRI',
            'ct scan': 'CT Scan',
            'ultrasound': 'Ultrasound',
            'x-ray': 'X-Ray',
            'blood test': 'Blood Tests',
            'echo': 'Echocardiogram',
            'echocardiogram': 'Echocardiogram'
        }
        
        # Check each diagnostic test in context
        for test_key, test_name in diagnostic_keywords.items():
            if test_key in letter_lower:
                # Determine if this is PAST (already done) or FUTURE (to be ordered)
                action_type = is_past_action(letter_lower, test_key)
                
                if action_type == 'future':
                    # Test needs to be ORDERED
                    actions_required.append(f"CHECK: {test_name} ordered in system (Y/N)")
                    actions_required.append(f"CHECK: {test_name} booking date recorded (Y/N)")
                    
                    if pas_summary.get('diagnostics_ordered') == 'Y':
                        actions_in_pas.append(f"✅ Diagnostics ordered ({test_name})")
                    else:
                        gaps.append(f"FLAG: Letter requests {test_name} - NOT ORDERED IN SYSTEM")
                        gaps.append(f"VERIFY: Check diagnostics system for {test_name} booking")
                
                elif action_type == 'past':
                    # Test was ALREADY DONE - check if results recorded
                    actions_required.append(f"VERIFY: {test_name} results from letter recorded in clinical notes (Y/N)")
                    # Don't flag as gap - this is documentation, not an order
    
    # ============================================
    # CODE 30 - FIRST DEFINITIVE TREATMENT
    # ============================================
    elif rtt_code == "30":
        actions_required.append("CHECK: Treatment date recorded in PAS (Y/N)")
        actions_required.append("CHECK: Procedure/treatment type documented (Y/N)")
        actions_required.append("CHECK: Clock stop date = treatment date (Y/N)")
        actions_required.append("CHECK: Pathway status = Closed (Y/N)")
        actions_required.append("CHECK: RTT code 30 recorded (Y/N)")
        
        if pas_summary.get('treatment_started') == 'Y':
            actions_in_pas.append("✅ Treatment started - Code 30 recorded")
        else:
            gaps.append("FLAG: Letter says treatment performed - NOT RECORDED IN SYSTEM")
            gaps.append("VERIFY: Check treatment records and update clock stop date")
        
        # Post-treatment follow-up
        if any(phrase in letter_lower for phrase in ['post-op', 'follow-up', 'review', 'check wound']):
            actions_required.append("CHECK: Post-treatment follow-up booked (Y/N)")
            actions_required.append("CHECK: Follow-up appointment date recorded (Y/N)")
    
    # ============================================
    # CODE 33 - DNA (DID NOT ATTEND)
    # ============================================
    elif rtt_code == "33":
        actions_required.append("CHECK: DNA recorded in PAS (Y/N)")
        actions_required.append("CHECK: DNA date = appointment date (Y/N)")
        actions_required.append("CHECK: RTT code 33 applied (Y/N)")
        actions_required.append("CHECK: Rebooking arranged (Y/N)")
        actions_required.append("CHECK: Rebook date within 2 weeks (Y/N)")
        actions_required.append("CHECK: DNA letter sent to patient (Y/N)")
        
        gaps.append("VERIFY: DNA recorded with correct date")
        gaps.append("VERIFY: New appointment booked within trust policy")
        gaps.append("FLAG: Ensure GP informed of DNA")
    
    # ============================================
    # CODE 34 - DISCHARGE / NO TREATMENT
    # ============================================
    elif rtt_code == "34":
        actions_required.append("CHECK: Discharge recorded in PAS (Y/N)")
        actions_required.append("CHECK: Discharge date = letter date (Y/N)")
        actions_required.append("CHECK: Clock stop date set (Y/N)")
        actions_required.append("CHECK: Pathway status = Closed (Y/N)")
        actions_required.append("CHECK: RTT code 34 recorded (Y/N)")
        actions_required.append("CHECK: Discharge letter sent to GP (Y/N)")
        
        gaps.append("VERIFY: Discharge properly recorded and pathway closed")
    
    # ============================================
    # CODE 31/32 - ACTIVE MONITORING
    # ============================================
    elif rtt_code in ["31", "32"]:
        actions_required.append("CHECK: Active Monitoring pathway created (Y/N)")
        actions_required.append("CHECK: AM start date recorded (Y/N)")
        actions_required.append(f"CHECK: RTT code {rtt_code} recorded (Y/N)")
        actions_required.append("CHECK: Clock status = Paused (Y/N)")
        actions_required.append("CHECK: Review date set for AM monitoring (Y/N)")
        
        if pas_summary.get('am_recorded') == 'Y':
            actions_in_pas.append("✅ Active Monitoring recorded")
        else:
            gaps.append("FLAG: Letter indicates Active Monitoring - NOT RECORDED IN SYSTEM")
            gaps.append("VERIFY: Check clock is paused and AM pathway exists")
    
    # ============================================
    # STANDARD CHECKS FOR ALL LETTER TYPES
    # ============================================
    
    # FOLLOW-UP APPOINTMENT CHECKS (with past/future logic)
    if 'follow' in letter_lower or 'review' in letter_lower or 'appointment' in letter_lower:
        # Check if this is PAST (already booked) or FUTURE (needs to be booked)
        appt_action = is_past_action(letter_lower, 'follow')
        
        if appt_action == 'future':
            # Appointment needs to be BOOKED
            actions_required.append("CHECK: Follow-up appointment booked (Y/N)")
            actions_required.append("CHECK: Follow-up date recorded (Y/N)")
            
            if pas_summary.get('followup_booked') == 'Y':
                actions_in_pas.append("✅ Follow-up appointment booked")
            else:
                gaps.append("FLAG: Letter requests follow-up appointment - NOT BOOKED")
                gaps.append("VERIFY: Check appointment diary for follow-up")
        
        elif appt_action == 'past':
            # Appointment already happened - verify it's recorded
            actions_required.append("VERIFY: Follow-up appointment attendance recorded (Y/N)")
    
    # GP LETTER CHECKS (for all codes except Code 10 which has it in Section 10)
    # With past/future logic
    if rtt_code != "10" and any(phrase in letter_lower for phrase in ['gp', 'copy to gp', 'inform gp', 'gp letter']):
        # Check if GP letter already sent or needs to be sent
        gp_action = is_past_action(letter_lower, 'gp')
        
        if gp_action == 'future' or gp_action == 'unclear':
            # GP letter needs to be SENT
            actions_required.append("CHECK: GP letter sent (Y/N)")
            actions_required.append("CHECK: GP letter date recorded (Y/N)")
            
            if pas_summary.get('gp_informed') == 'Y':
                actions_in_pas.append("✅ GP letter sent")
            else:
                gaps.append("FLAG: Letter says inform GP - GP letter NOT SENT")
                gaps.append("VERIFY: Check correspondence log for GP letter")
        
        elif gp_action == 'past':
            # GP letter already sent - verify recorded
            actions_required.append("VERIFY: GP letter recorded in correspondence log (Y/N)")
    
    # ============================================
    # PAS UPDATES REQUIRED (Based on gaps found)
    # ============================================
    pas_updates = [f"MANDATORY: Record RTT code {rtt_code} in PAS"]
    
    # Generate specific PAS update instructions based on gaps
    for gap in gaps:
        gap_lower = gap.lower()
        
        # Referral/pathway creation
        if 'referral' in gap_lower and 'logged' in gap_lower:
            pas_updates.append("ACTION: Log referral in referral register with all mandatory fields")
        elif 'pathway' in gap_lower and 'duplicate' in gap_lower:
            pas_updates.append("ACTION: Search PAS for duplicate pathways - same patient/specialty")
        elif 'pathway number' in gap_lower:
            pas_updates.append("ACTION: Assign unique pathway number and record in PAS")
        
        # Patient demographics
        elif 'patient name' in gap_lower or 'nhs number' in gap_lower or 'dob' in gap_lower:
            pas_updates.append("ACTION: Verify and correct patient demographics in PAS")
        
        # Partial Booking List
        elif 'pbl' in gap_lower or 'partial booking' in gap_lower:
            pas_updates.append("ACTION: Add patient to Partial Booking List (PBL) awaiting first appointment")
        
        # Appointments
        elif 'first appointment' in gap_lower or 'first appt' in gap_lower:
            pas_updates.append("ACTION: Book first outpatient appointment (2ww urgent / 6wk routine)")
        elif 'follow-up' in gap_lower or 'follow up' in gap_lower:
            pas_updates.append("ACTION: Book follow-up appointment as per letter instructions")
        
        # Waiting list
        elif 'waiting list' in gap_lower or 'surgical list' in gap_lower:
            pas_updates.append("ACTION: Add patient to surgical waiting list with procedure and specialty")
        elif 'tci' in gap_lower:
            pas_updates.append("ACTION: Set TCI (To Come In) date on waiting list entry")
        
        # Diagnostics
        elif any(test in gap_lower for test in ['ecg', 'angiogram', 'mri', 'ct', 'ultrasound', 'echo', 'x-ray']):
            pas_updates.append("ACTION: Order requested diagnostic test in diagnostics system")
        
        # Clock management
        elif 'clock start' in gap_lower:
            pas_updates.append("ACTION: Set clock start date = referral date")
        elif 'clock stop' in gap_lower or 'clock status' in gap_lower:
            pas_updates.append("ACTION: Update clock status and set stop date if applicable")
        
        # Correspondence
        elif 'gp letter' in gap_lower or 'gp informed' in gap_lower:
            pas_updates.append("ACTION: Send GP letter and record in correspondence log")
        elif 'acknowledgment' in gap_lower:
            pas_updates.append("ACTION: Send acknowledgment letter to referring GP/Consultant")
        
        # Priority/urgency
        elif 'urgent' in gap_lower or '2ww' in gap_lower:
            pas_updates.append("ACTION: Set URGENT/2WW priority flag in system")
        
        # Treatment
        elif 'treatment' in gap_lower and 'recorded' in gap_lower:
            pas_updates.append("ACTION: Record treatment date and type, set clock stop date")
        
        # Active Monitoring
        elif 'active monitoring' in gap_lower or 'am pathway' in gap_lower:
            pas_updates.append("ACTION: Create AM pathway and set clock status to PAUSED")
        
        # DNA
        elif 'dna' in gap_lower:
            pas_updates.append("ACTION: Record DNA, rebook within trust policy, inform GP")
    
    priority = "High" if len(gaps) >= 2 else ("Medium" if gaps else "Low")
    
    training_feedback = f"RTT code {rtt_code} is correct for this outcome. "
    if gaps:
        training_feedback += f"{len(gaps)} action(s) incomplete: complete all letter instructions to maintain pathway integrity."
    else:
        training_feedback += "All required actions completed. Well done."
    
    # NHS STANDARD COMMENT LINE FORMAT
    # Format: CS [DATE] ([CODE]) [INITIALS] AS PER CL DATED [LETTER_DATE] [ACTION]. F/U STATUS
    
    validation_date = datetime.now().strftime('%d/%m/%Y')
    validator_initials = pas_summary.get('validator_initials', 'VLD')
    
    # Try to extract letter date from letter text
    letter_date = validation_date  # Default to today if not found
    import re
    date_patterns = [
        r'Date[:\s]+(\d{1,2})[/\s-]+(\d{1,2})[/\s-]+(\d{4})',
        r'Dated[:\s]+(\d{1,2})[/\s-]+(\d{1,2})[/\s-]+(\d{4})',
        r'(\d{1,2})[/\s-]+(\d{1,2})[/\s-]+(\d{4})'
    ]
    
    for pattern in date_patterns:
        match = re.search(pattern, letter_text, re.IGNORECASE)
        if match:
            try:
                day = match.group(1).zfill(2)
                month = match.group(2).zfill(2)
                year = match.group(3)
                letter_date = f"{day}/{month}/{year}"
                break
            except:
                pass
    
    # Extract follow-up information
    followup_booked = pas_summary.get('followup_booked', 'N')
    followup_date_raw = pas_summary.get('followup_date')
    
    followup_status = ""
    if followup_date_raw:
        # Convert date object to string if needed
        if hasattr(followup_date_raw, 'strftime'):
            followup_date = followup_date_raw.strftime('%d/%m/%Y')
        else:
            followup_date = str(followup_date_raw)
        
        if followup_booked == 'Y':
            followup_status = f". F/U APPT BOOKED FOR {followup_date}"
        else:
            followup_status = ". F/U APPT REQUIRED BOOKING"
    elif any(phrase in letter_lower for phrase in ['follow-up', 'follow up', 'review']):
        if followup_booked == 'Y':
            followup_status = ". F/U APPT BOOKED"
        else:
            followup_status = ". F/U APPT REQUIRED BOOKING"
    
    # Build comment based on RTT code
    # CLOCK STOPPED CODES: 30, 31, 32, 33, 34, 35, 36
    clock_stopped_codes = ["30", "31", "32", "33", "34", "35", "36"]
    
    if rtt_code in clock_stopped_codes:
        # CLOCK STOP FORMAT (T21 style): CS (DATE OF CLOCK STOP)(RTT CODE) [INITIALS] REASON FOR CLOCK STOP
        stop_date = letter_date  # Use letter date as clock stop date
        
        if rtt_code == "30":
            # First Definitive Treatment
            if followup_status:
                comment_line = f"CS ({stop_date})({rtt_code}) {validator_initials} PATIENT RCVD MEDICATION/TREATMENT{followup_status}"
            else:
                comment_line = f"CS ({stop_date})({rtt_code}) {validator_initials} PATIENT RCVD MEDICATION/TREATMENT"
        
        elif rtt_code == "34":
            # Discharge
            comment_line = f"CS ({stop_date})({rtt_code}) {validator_initials} PATIENT DISCHARGED - NO TREATMENT REQUIRED"
        
        elif rtt_code == "35":
            # Patient declined
            comment_line = f"CS ({stop_date})({rtt_code}) {validator_initials} PATIENT DECLINED TREATMENT"
        
        elif rtt_code == "33":
            # DNA
            comment_line = f"{validation_date} T21 - DNA RECORDED. REBOOK REQUIRED"
        
        elif rtt_code in ["31", "32"]:
            # Active Monitoring
            am_type = "PATIENT" if rtt_code == "31" else "CLINICIAN"
            comment_line = f"{validation_date} T21 - AM ({am_type} INITIATED). CLOCK PAUSED{followup_status}"
        
        elif rtt_code == "36":
            # Further treatment not clinically appropriate
            comment_line = f"CS ({stop_date})({rtt_code}) {validator_initials} FURTHER TREATMENT NOT APPROPRIATE"
    
    else:
        # CLOCK CONTINUES CODES: 10, 11, 12, 20, 21, 90, 91, 92, 98
        # Format: [VALIDATION_DATE] T21 - [SUMMARY]
        
        # Extract summary from letter
        letter_summary = ""
        diagnostics_ordered = pas_summary.get('diagnostics_ordered', 'N')
        diagnostics_date_raw = pas_summary.get('diagnostics_date')
        waiting_list = pas_summary.get('waiting_list', 'N')
        
        if rtt_code == "10":
            # Referral - awaiting first OPA
            comment_line = f"{validation_date} T21 - AWAITING 1ST OPA"
        
        elif rtt_code == "20":
            # Decision to treat - T21 style: [DATE] T21 - [ACTION]
            
            # Check for diagnostics in letter
            diagnostic_mentioned = False
            diagnostic_type = ""
            if any(test in letter_lower for test in ['mri', 'ct', 'scan', 'ultrasound', 'x-ray', 'ecg', 'echo']):
                diagnostic_mentioned = True
                if 'mri' in letter_lower:
                    diagnostic_type = "MRI SCAN"
                elif 'ct' in letter_lower or 'ct scan' in letter_lower:
                    diagnostic_type = "CT SCAN"
                elif 'ultrasound' in letter_lower:
                    diagnostic_type = "ULTRASOUND"
                elif 'x-ray' in letter_lower or 'xray' in letter_lower:
                    diagnostic_type = "X-RAY"
                elif 'ecg' in letter_lower:
                    diagnostic_type = "ECG"
                elif 'echo' in letter_lower:
                    diagnostic_type = "ECHOCARDIOGRAM"
            
            # Check for surgery/procedure in letter
            surgery_mentioned = any(word in letter_lower for word in ['surgery', 'operation', 'procedure', 'list for', 'waiting list'])
            
            # Build T21 style comment based on what letter mentions
            if diagnostic_mentioned:
                # Check if diagnostic is PAST (done) or FUTURE (to be done)
                is_done = any(phrase in letter_lower for phrase in ['was performed', 'has been done', 'underwent', 'results from'])
                
                if is_done:
                    # Diagnostic already done - check if results received
                    results_received = any(phrase in letter_lower for phrase in ['results', 'showed', 'demonstrated', 'normal', 'abnormal'])
                    if results_received:
                        # Results in letter
                        comment_line = f"{validation_date} T21 - DXG [{diagnostic_type}] {letter_date}"
                    else:
                        # Done but awaiting results
                        comment_line = f"{validation_date} T21 - AWAITING RESULTS [{diagnostic_type}]"
                else:
                    # Diagnostic to be done
                    if diagnostics_ordered == 'Y':
                        if diagnostics_date_raw:
                            if hasattr(diagnostics_date_raw, 'strftime'):
                                diag_date = diagnostics_date_raw.strftime('%d/%m/%Y')
                            else:
                                diag_date = str(diagnostics_date_raw)
                            # DSG = Diagnostic booked
                            comment_line = f"{validation_date} T21 - DSG [{diagnostic_type}] {diag_date}"
                        else:
                            comment_line = f"{validation_date} T21 - DSG [{diagnostic_type}]"
                    else:
                        # Awaiting diagnostic booking
                        comment_line = f"{validation_date} T21 - AWAITING DSG [{diagnostic_type}]"
            
            elif surgery_mentioned:
                # Surgery/waiting list - check if TCI date set
                if waiting_list == 'Y':
                    # Check if TCI date in PAS
                    if followup_date_raw:  # Using followup_date as TCI date
                        if hasattr(followup_date_raw, 'strftime'):
                            tci_date = followup_date_raw.strftime('%d/%m/%Y')
                        else:
                            tci_date = str(followup_date_raw)
                        # 1CL = TCI/surgery date
                        comment_line = f"{validation_date} T21 - 1CL {tci_date}"
                    else:
                        # On waiting list but no TCI date
                        comment_line = f"{validation_date} T21 - AWAITING 1CL"
                else:
                    # Not on waiting list yet
                    comment_line = f"{validation_date} T21 - AWAITING WAITING LIST ENTRY"
            
            else:
                # Generic decision to treat - check if follow-up mentioned
                if followup_booked == 'Y' and followup_date_raw:
                    if hasattr(followup_date_raw, 'strftime'):
                        fu_date = followup_date_raw.strftime('%d/%m/%Y')
                    else:
                        fu_date = str(followup_date_raw)
                    comment_line = f"{validation_date} T21 - F/U APPT {fu_date}"
                elif any(phrase in letter_lower for phrase in ['follow-up', 'follow up', 'review']):
                    comment_line = f"{validation_date} T21 - AWAITING F/U APPT"
                else:
                    comment_line = f"{validation_date} T21 - CLINIC OUTCOME REVIEWED"
        
        elif rtt_code == "11":
            # Return from AM - T21 style
            comment_line = f"{validation_date} T21 - RETURNED FROM AM. CLOCK RESTARTED"
        
        elif rtt_code == "12":
            # Return from DNA - T21 style
            comment_line = f"{validation_date} T21 - PATIENT ATTENDED AFTER DNA"
        
        elif rtt_code == "21":
            # Inter-provider transfer - T21 style
            comment_line = f"{validation_date} T21 - IPT TO [RECEIVING PROVIDER]"
        
        elif rtt_code in ["90", "91", "92", "98"]:
            # Post-treatment codes - T21 style
            if followup_booked == 'Y' and followup_date_raw:
                if hasattr(followup_date_raw, 'strftime'):
                    fu_date = followup_date_raw.strftime('%d/%m/%Y')
                else:
                    fu_date = str(followup_date_raw)
                comment_line = f"{validation_date} T21 - POST-TX F/U {fu_date}"
            else:
                comment_line = f"{validation_date} T21 - AWAITING POST-TX F/U"
        
        else:
            # Generic - T21 style
            comment_line = f"{validation_date} T21 - CLINIC OUTCOME REVIEWED"
    
    # VALIDATION SUMMARY - For Excel Reporting
    total_actions = len(actions_required)
    completed_actions = len(actions_in_pas)
    missing_actions = len(gaps)
    compliance_rate = f"{(completed_actions / total_actions * 100):.0f}%" if total_actions > 0 else "N/A"
    
    # Overall validation status
    if missing_actions == 0:
        validation_status = "PASS - All actions completed"
        excel_flag = "GREEN"
    elif missing_actions <= 2:
        validation_status = f"PARTIAL - {missing_actions} action(s) outstanding"
        excel_flag = "AMBER"
    else:
        validation_status = f"FAIL - {missing_actions} critical gaps found"
        excel_flag = "RED"
    
    return {
        "RTT_Code": rtt_code,
        "RTT_Action": rtt_action,
        "Clock_Status": clock_status,
        "Explanation": explanation,
        
        # VALIDATION CHECKLIST (for Excel tracker)
        "Validation_Summary": {
            "Overall_Status": validation_status,
            "Excel_Flag_Color": excel_flag,
            "Compliance_Rate": compliance_rate,
            "Total_Actions_Required": total_actions,
            "Actions_Completed": completed_actions,
            "Actions_Outstanding": missing_actions
        },
        
        "Action_Compliance": {
            "Actions_Required": actions_required,
            "Actions_Reported_In_PAS": actions_in_pas,
            "Gaps": gaps,
            "Priority": priority
        },
        
        "PAS_Update": pas_updates,
        "Training_Feedback": training_feedback,
        "Confidence_Level": "High",
        "Policy_Reference": "NHS England RTT Guidance v17",
        "Standardised_Comment_Line": comment_line,
        
        # EXCEL REPORTING FIELDS (Matches Excel Tracker Structure)
        "Excel_Report": generate_excel_report(rtt_code, validation_date, validator_initials, 
                                             pas_summary, completed_actions, missing_actions, 
                                             gaps, excel_flag)
    }


def generate_excel_report(rtt_code, validation_date, validator_initials, pas_summary, 
                          completed_actions, missing_actions, gaps, excel_flag):
    """Generate Excel tracker report matching exact Excel structure"""
    
    excel_clock_status = pas_summary.get('clock_status', 'Unclear')
    excel_outcome = pas_summary.get('outcome', '(Blank)')
    
    # Generate Validation Comments (Summary style: CODE + DATE + SUMMARY + ACTIONS DONE + NEXT ACTIONS)
    validation_comment = f"{validation_date} "
    
    # Add letter summary
    if rtt_code == "10":
        validation_comment += "REFERRAL RECEIVED. "
    elif rtt_code == "20":
        validation_comment += "CLINIC OUTCOME LETTER REVIEWED. "
    elif rtt_code == "30":
        validation_comment += "FDT COMPLETED. "
    elif rtt_code in ["31", "32"]:
        validation_comment += "AM STARTED. "
    elif rtt_code == "33":
        validation_comment += "DNA RECORDED. "
    elif rtt_code == "34":
        validation_comment += "DISCHARGED. "
    else:
        validation_comment += "LETTER VALIDATED. "
    
    # Add what's been checked/done
    if completed_actions > 0:
        validation_comment += f"{completed_actions} ACTIONS VERIFIED IN PAS. "
    
    # Add what's missing/needs to be done
    if missing_actions > 0:
        validation_comment += f"{missing_actions} OUTSTANDING. "
        # Add key gaps
        key_gaps = []
        for gap in gaps[:3]:  # First 3 gaps only for brevity
            if "waiting list" in gap.lower():
                key_gaps.append("WL")
            elif "pbl" in gap.lower() or "partial booking" in gap.lower():
                key_gaps.append("PBL")
            elif "appointment" in gap.lower() and "first" in gap.lower():
                key_gaps.append("OPA")
            elif "gp" in gap.lower():
                key_gaps.append("GP LTR")
            elif any(test in gap.lower() for test in ['ecg', 'angiogram', 'scan', 'mri']):
                key_gaps.append("DIAGNOSTICS")
        if key_gaps:
            validation_comment += "REQUIRED: " + ", ".join(key_gaps) + ". "
    else:
        validation_comment += "ALL COMPLETE. "
    
    # Add outcome/next step
    if excel_outcome and excel_outcome != "(Blank)":
        validation_comment += f"{excel_outcome}."
    
    return {
        "Validator_Name": validator_initials,
        "Clock_Status": excel_clock_status,
        "Outcome": excel_outcome,
        "Validation_Date": validation_date,
        "Validation_Comments": validation_comment.strip(),
        "RTT_Code": rtt_code
    }


def validate_timeline(events: List[Dict]) -> Dict:
    """
    Timeline Auditor (T21 RTT Data Quality Auditor v1.1)
    """
    critical_issues = []
    moderate_issues = []
    duplicate_issues = []
    recode_suggestions = []
    
    # Track code usage
    code_counts = {}
    dates = []
    
    for event in events:
        code = event.get('code', '')
        date = parse_date(event.get('date', ''))
        
        if date:
            dates.append(date)
        
        if code in code_counts:
            code_counts[code] += 1
        else:
            code_counts[code] = 1
    
    # Check for duplicate unique codes
    for code in ['10', '30', '34', '35', '36']:
        if code_counts.get(code, 0) > 1:
            duplicate_issues.append(f"Code {code} appears {code_counts[code]} times - should appear ONCE only")
            critical_issues.append(f"Duplicate code {code} invalidates pathway")
    
    # Check chronology
    if dates and dates != sorted(dates):
        critical_issues.append("Events not in chronological order")
    
    # Check for specific issues
    has_code_10 = '10' in code_counts
    has_code_11 = '11' in code_counts
    has_code_12 = '12' in code_counts
    has_am_start = '31' in code_counts or '32' in code_counts
    has_code_91 = '91' in code_counts
    
    # Check for pathway start (10, 11, or 12)
    has_start = has_code_10 or has_code_11 or has_code_12
    if not has_start:
        critical_issues.append("No pathway start code found (10, 11, or 12 required)")
    
    # Check code 11 logic (must follow AM)
    if has_code_11:
        # Look for prior AM start (31/32)
        found_am_before_11 = False
        for event in events:
            if event.get('code') in ['31', '32']:
                found_am_before_11 = True
            if event.get('code') == '11' and not found_am_before_11:
                critical_issues.append("Code 11 used without prior Active Monitoring (31/32)")
                recode_suggestions.append("Code 11 requires prior code 31 or 32. Add AM start or change to code 10/20")
                break
    
    if has_code_91 and not has_am_start:
        critical_issues.append("Code 91 used without prior code 31 or 32 (AM start)")
        recode_suggestions.append("Recode 91 to 20 (if routine) or add missing AM start code 31/32")
    
    # Check for code 20 after code 30
    found_30 = False
    for i, event in enumerate(events):
        if event.get('code') == '30':
            found_30 = True
        if found_30 and event.get('code') == '20':
            moderate_issues.append(f"Code 20 used after code 30 on {event.get('date')} - should be code 90")
            recode_suggestions.append(f"{event.get('date')}: Code 20 → Code 90 (FDT occurred previously)")
    
    # Calculate weeks
    clock_start = dates[0] if dates else None
    clock_stop = None
    
    for event in events:
        if event.get('code') in ['30', '34', '35', '36']:
            clock_stop = parse_date(event.get('date'))
            break
    
    if clock_start and clock_stop:
        weeks_total = calculate_weeks(clock_start, clock_stop)
    elif clock_start:
        weeks_total = calculate_weeks(clock_start, datetime.now())
    else:
        weeks_total = 0
    
    breach_flag = get_breach_flag(weeks_total)
    
    # Overall status
    if critical_issues:
        overall_status = "Fail"
    elif moderate_issues:
        overall_status = "Warning"
    else:
        overall_status = "Pass"
    
    # Training feedback
    if critical_issues:
        feedback = f"Critical errors found: {len(critical_issues)} issue(s) must be fixed immediately. Pathway is invalid."
    elif moderate_issues:
        feedback = f"Minor issues detected: {len(moderate_issues)} coding improvements recommended."
    else:
        feedback = "Pathway correctly coded and sequenced. Compliant with RTT rules."
    
    # Comment line
    if clock_stop:
        comment_line = f"CS{clock_stop.strftime('%d/%m/%Y')}/30 – PATHWAY CLOSED {weeks_total}WKS. "
    else:
        comment_line = f"RTT ACTIVE – {weeks_total}WKS ELAPSED. "
    
    if overall_status == "Fail":
        comment_line += "CRITICAL ERRORS - RECODE REQUIRED."
    elif overall_status == "Warning":
        comment_line += "MINOR ISSUES - REVIEW RECOMMENDED."
    else:
        comment_line += "COMPLIANT."
    
    return {
        "Overall_Status": overall_status,
        "Clock_Start_Date": clock_start.strftime('%d/%m/%Y') if clock_start else "",
        "Clock_Stop_Date": clock_stop.strftime('%d/%m/%Y') if clock_stop else "",
        "Weeks_Total": str(weeks_total),
        "Breach_Flag": breach_flag,
        "Duplicate_Code_Issues": duplicate_issues,
        "Critical_Issues": critical_issues,
        "Moderate_Issues": moderate_issues,
        "Recommended_Recode_Suggestions": recode_suggestions,
        "What_To_Change_In_PAS": recode_suggestions + [issue for issue in critical_issues],
        "Training_Feedback": feedback,
        "Confidence_Level": "High",
        "Policy_Reference": "NHS England RTT v17",
        "Standardised_Comment_Line": comment_line
    }


def validate_nhs_number(nhs_number: str) -> bool:
    """Validate NHS number using modulus 11 check digit algorithm"""
    if not nhs_number or len(nhs_number) != 10 or not nhs_number.isdigit():
        return False
    
    # Modulus 11 algorithm
    total = 0
    for i in range(9):
        total += int(nhs_number[i]) * (10 - i)
    
    remainder = total % 11
    check_digit = 11 - remainder
    
    if check_digit == 11:
        check_digit = 0
    
    # Check digit must not be 10
    if check_digit == 10:
        return False
    
    return int(nhs_number[9]) == check_digit


def validate_patient_registration(data: Dict) -> Dict:
    """
    Patient Registration Validator (T21 v1.0)
    Validates patient registration details and document readiness
    """
    issues = []
    pas_updates = []
    
    # Validate NHS Number
    nhs_number = data.get('nhs_number', '').replace(' ', '')
    if not nhs_number:
        issues.append("NHS number is missing (mandatory field)")
    elif not validate_nhs_number(nhs_number):
        issues.append(f"NHS number '{nhs_number}' is invalid (failed checksum or format)")
    
    # Validate DOB
    dob = parse_date(data.get('dob', ''))
    if not dob:
        issues.append("Date of Birth is missing (mandatory field)")
    elif dob > datetime.now():
        issues.append("Date of Birth is in the future (invalid)")
    elif dob < datetime(1900, 1, 1):
        issues.append("Date of Birth is before 1900 (check for data entry error)")
    
    # Check age consistency
    if dob:
        age = (datetime.now() - dob).days // 365
        provided_age = data.get('age', '')
        if provided_age and abs(age - int(provided_age)) > 1:
            issues.append(f"Age mismatch: DOB suggests {age} years but {provided_age} recorded")
    
    # Validate name
    if not data.get('patient_name', '').strip():
        issues.append("Patient name is missing (mandatory field)")
    
    # Validate referral details
    if not data.get('referral_source', '').strip():
        issues.append("Referral source is missing (mandatory field)")
    
    referral_date = parse_date(data.get('referral_date', ''))
    if not referral_date:
        issues.append("Referral date is missing (mandatory field)")
    elif referral_date > datetime.now():
        issues.append("Referral date is in the future (invalid)")
    
    if not data.get('specialty', '').strip():
        issues.append("Specialty is missing (mandatory field)")
    
    # Document naming convention check
    documents = data.get('documents', '')
    if documents:
        doc_list = [d.strip() for d in documents.split(',')]
        for doc in doc_list:
            # Check for reasonable naming (SURNAME_FORENAME_DDMMYY_DOCTYPE pattern)
            if '_' not in doc and len(doc) > 0:
                pas_updates.append(f"Document '{doc}' does not follow naming convention (SURNAME_FORENAME_DDMMYY_DOCTYPE)")
    
    # Check for potential duplicates
    if data.get('check_duplicate') == 'Y':
        # In real system, would query database
        pas_updates.append("Check for duplicate pathways with same NHS number and specialty")
    
    # RTT start reminder
    if data.get('referral_accepted') == 'Y':
        pas_updates.append("Reminder: Start RTT clock (code 10) at first clinical activity")
        if 'diagnostic' in data.get('referral_type', '').lower() and 'consultant' not in data.get('referral_type', '').lower():
            pas_updates.append("Note: If diagnostic-only referral (non-consultant-led), use code 92 (non-RTT)")
    
    # Determine result
    if len(issues) >= 3:
        result = "Fail"
    elif issues:
        result = "Warning"
    else:
        result = "Pass"
    
    # Training feedback
    if result == "Pass":
        feedback = "Registration data complete and valid. Ready to start RTT pathway."
    elif result == "Warning":
        feedback = f"{len(issues)} issue(s) found. Correct these before proceeding to avoid data quality problems."
    else:
        feedback = f"Registration incomplete: {len(issues)} critical issues. Cannot start pathway until resolved."
    
    # Comment line
    if result == "Pass":
        comment_line = f"NEW REG/{data.get('referral_date', '')} – {data.get('referral_source', 'GP')} → {data.get('specialty', 'UNK')}. CODE 10 AT FIRST CARE."
    else:
        comment_line = f"REG INCOMPLETE – {len(issues)} ISSUES. RESOLVE BEFORE RTT START."
    
    return {
        "Validation_Result": result,
        "Data_Issues": issues,
        "PAS_Update": pas_updates if pas_updates else ["No PAS updates required"],
        "Training_Feedback": feedback,
        "Confidence_Level": "High",
        "Standardised_Comment_Line": comment_line
    }


def validate_appointments(data: Dict) -> Dict:
    """
    Appointment & Booking Checker (T21 v1.0)
    Reviews booking history and ensures correct RTT impact
    """
    issues = []
    pas_updates = []
    rtt_impact = "No change"
    
    # Parse dates
    referral_date = parse_date(data.get('referral_date', ''))
    first_appt_date = parse_date(data.get('first_appt_date', ''))
    
    # Check first appointment timing
    if referral_date and first_appt_date:
        days_to_first = (first_appt_date - referral_date).days
        if days_to_first > 21:
            issues.append(f"First appointment {days_to_first} days after referral (>3 weeks - check capacity)")
        if days_to_first < 0:
            issues.append("First appointment date is BEFORE referral date (data error)")
    
    # Check DNAs
    dna_text = data.get('dnas_cancellations', '').lower()
    if 'dna' in dna_text or 'did not attend' in dna_text:
        if 'first' in dna_text and 'care' in dna_text:
            pas_updates.append("Record DNA first care (code 33)")
            pas_updates.append("Rebook within trust policy timeframe (typically 2 weeks)")
            rtt_impact = "Continue (20) or DNA (33)"
        else:
            pas_updates.append("Rebook appointment - check if patient or hospital initiated")
    
    # Check cancellations
    if 'cancel' in dna_text:
        if any(word in dna_text for word in ['hospital', 'trust', 'clinic', 'provider']):
            issues.append("Hospital-initiated cancellation - clock does NOT pause (continue code 20)")
            pas_updates.append("Rebook immediately - provider cancellations do not pause RTT clock")
        elif any(word in dna_text for word in ['patient', 'personal', 'unavailable']):
            pas_updates.append("Patient-initiated cancellation - clock CAN pause (document dates)")
            rtt_impact = "Pause"
    
    # Check follow-ups
    followup_text = data.get('followup_appointments', '')
    if followup_text:
        # Check if within instructed window (extract from notes if mentioned)
        import re
        window_match = re.search(r'(\d+)\s*(week|month)', data.get('notes', '').lower())
        if window_match:
            required_weeks = int(window_match.group(1))
            if 'month' in window_match.group(2):
                required_weeks *= 4
            pas_updates.append(f"Verify follow-up booked within {required_weeks}-week window")
    
    # Check waiting list / TCI
    if data.get('planned_surgery', '').strip():
        wl_text = data.get('planned_surgery', '').lower()
        if 'tci' in wl_text or 'date' in wl_text:
            pas_updates.append("Verify TCI date on waiting list entry")
        else:
            issues.append("Surgery planned but no TCI date set - patient is waiting")
        
        if data.get('treatment_started') == 'Y':
            rtt_impact = "Stop (30)"
            pas_updates.append("Record first treatment (code 30) with treatment date")
        else:
            rtt_impact = "Continue (20)"
    
    # Check Active Monitoring
    am_status = data.get('am_status', '')
    if am_status:
        if '31' in am_status or '32' in am_status:
            pas_updates.append(f"Verify code {am_status[:2]} recorded with AM start date")
            pas_updates.append("Subsequent AM appointments should use code 91")
            rtt_impact = "AM (31/32 start or 91 during)"
        elif '91' in am_status:
            # Check if 31/32 exists earlier
            if data.get('am_start_date', ''):
                rtt_impact = "AM (91)"
            else:
                issues.append("Code 91 used but no AM start (31/32) recorded - invalid")
                pas_updates.append("Add missing code 31 or 32 for AM start OR recode 91 to 20")
    
    # Determine result
    confidence = "High" if referral_date and first_appt_date else "Medium"
    
    # Training feedback
    if issues:
        feedback = f"{len(issues)} issue(s) detected in booking history. Review and correct to maintain pathway integrity."
    else:
        feedback = "Booking history appears correct. Appointments scheduled appropriately."
    
    # Comment line
    if rtt_impact.startswith("Stop"):
        comment_line = f"APPTS COMPLETE/{datetime.now().strftime('%d/%m/%Y')} – RTT STOP {rtt_impact}."
    elif "Pause" in rtt_impact:
        comment_line = f"APPTS/{datetime.now().strftime('%d/%m/%Y')} – CLOCK PAUSED. PATIENT-INITIATED DELAY."
    elif "AM" in rtt_impact:
        comment_line = f"APPTS/{datetime.now().strftime('%d/%m/%Y')} – ACTIVE MONITORING. CODE {rtt_impact}."
    else:
        comment_line = f"APPTS/{datetime.now().strftime('%d/%m/%Y')} – PATHWAY CONTINUES. CODE 20."
    
    return {
        "Issues": issues if issues else ["No issues found"],
        "RTT_Impact": rtt_impact,
        "PAS_Update": pas_updates if pas_updates else ["No updates required"],
        "Training_Feedback": feedback,
        "Confidence_Level": confidence,
        "Standardised_Comment_Line": comment_line
    }


def generate_comment_line(data: Dict) -> Dict:
    """
    Comment Line Generator (T21 v1.0)
    Generates standardized PAS comment lines in T21 style
    """
    event = data.get('event', '').lower()
    key_date = data.get('key_date', datetime.now().strftime('%d/%m/%Y'))
    rtt_code = data.get('rtt_code', '')
    procedure = data.get('procedure', '').upper()
    next_action = data.get('next_action', '')
    gp_letter = data.get('gp_letter', 'N')
    
    # Generate comment based on event type
    if 'treatment' in event or 'fdt' in event or event == '30':
        comment = f"CS{key_date}/30 – FDT STARTED"
        if procedure:
            comment += f" ({procedure})"
        comment += ". PATHWAY CLOSED."
        if gp_letter == 'Y':
            comment += " GP LETTER SENT."
    
    elif 'active monitoring' in event or 'am start' in event or rtt_code in ['31', '32']:
        code = rtt_code if rtt_code in ['31', '32'] else '32'
        comment = f"AM{code}/{key_date} – "
        if next_action:
            # Extract review period
            import re
            match = re.search(r'(\d+)\s*(week|month|w|m)', next_action.lower())
            if match:
                period = match.group(1) + ('W' if 'w' in match.group(2) else 'M')
                comment += f"UNDER REVIEW {period}. "
            else:
                comment += "UNDER REVIEW. "
        else:
            comment += "UNDER REVIEW. "
        
        # Add follow-up info
        if 'fu' in next_action.lower() or 'follow' in next_action.lower():
            match = re.search(r'(\d{2}/\d{2}/\d{4})', next_action)
            if match:
                comment += f"FU BOOKED {match.group(1)}."
            else:
                comment += "FU REQUIRED."
        else:
            comment += "CONTINUE AM."
    
    elif 'dna' in event or rtt_code == '33':
        comment = f"DNA33/{key_date} – "
        if 'first care' in event:
            comment += "FIRST CARE DNA. "
        else:
            comment += "DNA. "
        comment += "REBOOK 2W."
        if gp_letter == 'Y':
            comment += " GP COPY SENT."
        else:
            comment += " GP COPY PENDING."
    
    elif 'wl' in event or 'tci' in event or 'waiting list' in event:
        comment = f"WL/TCI"
        if key_date:
            comment += f" {key_date}"
        comment += " – "
        if next_action and any(char.isdigit() for char in next_action):
            comment += f"TCI SET. "
        else:
            comment += "AWAITING DATE. "
        comment += "CONTINUE 20."
    
    elif 'discharge' in event or rtt_code == '34':
        comment = f"DISCH{key_date}/34 – "
        if 'no treatment' in event or 'not required' in event:
            comment += "NO TREATMENT REQUIRED. "
        else:
            comment += "DISCHARGED. "
        comment += "PATHWAY CLOSED."
        if gp_letter == 'Y':
            comment += " GP LETTER SENT."
    
    elif 'decision to treat' in event or 'dtt' in event:
        comment = f"DTT{key_date}/20 – LISTED FOR "
        if procedure:
            comment += procedure
        else:
            comment += "TREATMENT"
        comment += ". "
        if next_action:
            comment += next_action.upper()
        else:
            comment += "WL ENTRY REQUIRED."
    
    else:
        # Generic comment
        comment = f"RTT{key_date}"
        if rtt_code:
            comment += f"/{rtt_code}"
        comment += " – "
        if procedure:
            comment += f"{procedure}. "
        if next_action:
            comment += next_action.upper()
        else:
            comment += "CONTINUE."
    
    return {
        "Standardised_Comment_Line": comment
    }


# ============================================================================
# AI-ENHANCED FUNCTIONS (NEW!)
# ============================================================================

def validate_clinic_letter_ai_enhanced(letter_text: str, pas_summary: Dict, use_ai: bool = False) -> Dict:
    """
    AI-Enhanced Clinic Letter Interpreter
    
    Combines traditional keyword-based validation with optional AI NLP
    
    Args:
        letter_text: The clinic letter text
        pas_summary: PAS data summary
        use_ai: If True, uses AI NLP for enhanced accuracy (requires OpenAI API key)
    
    Returns:
        Enhanced validation results with AI insights
    """
    # Always run traditional validation (fast, reliable)
    traditional_result = validate_clinic_letter(letter_text, pas_summary)
    
    # If AI is available and requested, enhance with NLP
    if use_ai and NLP_AVAILABLE:
        try:
            nlp_reader = NLPLetterReader()
            ai_result = nlp_reader.read_letter(letter_text)
            
            # Merge AI insights with traditional results
            traditional_result['ai_enhanced'] = True
            traditional_result['ai_confidence'] = ai_result.get('confidence', 0)
            traditional_result['ai_extracted_data'] = ai_result.get('extracted_data', {})
            traditional_result['ai_suggestions'] = ai_result.get('suggestions', [])
            
            # If AI detects different code, flag for review
            if ai_result.get('rtt_code') != traditional_result.get('rtt_code'):
                traditional_result['code_conflict'] = {
                    'traditional': traditional_result.get('rtt_code'),
                    'ai_suggested': ai_result.get('rtt_code'),
                    'review_required': True
                }
        except Exception as e:
            traditional_result['ai_error'] = str(e)
            traditional_result['ai_enhanced'] = False
    else:
        traditional_result['ai_enhanced'] = False
        traditional_result['ai_available'] = NLP_AVAILABLE
    
    return traditional_result


def transcribe_audio_letter(audio_file_path: str) -> Dict:
    """
    Transcribe doctor's audio dictation to text
    
    Args:
        audio_file_path: Path to audio file (mp3, wav, m4a, etc.)
    
    Returns:
        {
            'success': bool,
            'text': str (transcribed text),
            'duration': float (seconds),
            'confidence': float,
            'error': str (if failed)
        }
    """
    if not AUDIO_AVAILABLE:
        return {
            'success': False,
            'error': 'Audio transcription not available. Install OpenAI Whisper.'
        }
    
    try:
        service = AudioTranscriptionService()
        result = service.transcribe_audio(audio_file_path)
        return {
            'success': True,
            'text': result.get('text', ''),
            'duration': result.get('duration', 0),
            'confidence': result.get('confidence', 0),
            'efficiency': result.get('efficiency', '')
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


def ocr_handwritten_letter(image_path: str) -> Dict:
    """
    Extract text from handwritten clinic letter
    
    Args:
        image_path: Path to image file (jpg, png, pdf, etc.)
    
    Returns:
        {
            'success': bool,
            'text': str (extracted text),
            'confidence': float,
            'error': str (if failed)
        }
    """
    if not OCR_AVAILABLE:
        return {
            'success': False,
            'error': 'OCR not available. Install OpenAI Vision API.'
        }
    
    try:
        service = HandwritingOCRService()
        result = service.extract_text_from_image(image_path)
        return {
            'success': True,
            'text': result.get('text', ''),
            'confidence': result.get('confidence', 0),
            'processing_time': result.get('processing_time', 0)
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


def auto_fix_pas_errors(validation_result: Dict, pas_data: Dict) -> Dict:
    """
    Automatically fix detected errors in PAS
    
    Args:
        validation_result: Result from validate_clinic_letter()
        pas_data: Current PAS data
    
    Returns:
        {
            'success': bool,
            'fixes_applied': int,
            'fixes': List[Dict],
            'updated_pas_data': Dict,
            'confidence': float
        }
    """
    if not AUTOFIX_AVAILABLE:
        return {
            'success': False,
            'error': 'Auto-fix not available.'
        }
    
    try:
        engine = AutoFixEngine()
        result = engine.fix_errors(validation_result, pas_data)
        return result
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


def validate_bulk_letters(letters: List[Dict], use_ai: bool = False) -> Dict:
    """
    Validate multiple clinic letters at once (ULTRA-FAST!)
    
    Args:
        letters: List of {'text': str, 'pas_summary': Dict}
        use_ai: Use AI enhancement (slower but more accurate)
    
    Returns:
        {
            'total_letters': int,
            'validation_time': float,
            'results': List[Dict],
            'errors_found': int,
            'auto_fixed': int,
            'efficiency': str
        }
    """
    if not BATCH_AVAILABLE:
        # Fallback to sequential processing
        import time
        start_time = time.time()
        results = []
        
        for letter in letters:
            result = validate_clinic_letter_ai_enhanced(
                letter.get('text', ''),
                letter.get('pas_summary', {}),
                use_ai=use_ai
            )
            results.append(result)
        
        end_time = time.time()
        
        return {
            'total_letters': len(letters),
            'validation_time': end_time - start_time,
            'results': results,
            'errors_found': sum(1 for r in results if r.get('gaps')),
            'efficiency': f"Processed {len(letters)} letters in {end_time - start_time:.2f}s"
        }
    
    try:
        engine = BatchValidationEngine()
        result = engine.validate_batch(letters, use_ai=use_ai)
        return result
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


# ============================================================================
# FEATURE AVAILABILITY CHECK
# ============================================================================

def get_ai_features_status() -> Dict:
    """
    Check which AI features are available
    
    Returns:
        {
            'nlp': bool,
            'audio_transcription': bool,
            'ocr': bool,
            'auto_fix': bool,
            'batch_processing': bool,
            'all_available': bool
        }
    """
    return {
        'nlp': NLP_AVAILABLE,
        'audio_transcription': AUDIO_AVAILABLE,
        'ocr': OCR_AVAILABLE,
        'auto_fix': AUTOFIX_AVAILABLE,
        'batch_processing': BATCH_AVAILABLE,
        'all_available': all([NLP_AVAILABLE, AUDIO_AVAILABLE, OCR_AVAILABLE, AUTOFIX_AVAILABLE, BATCH_AVAILABLE])
    }
