"""
T21 CLINIC LETTER INTERPRETER - EDUCATIONAL VERSION
Teaches HOW to interpret clinic letters step-by-step

SHOWS:
1. How to READ the letter (interpretation guide)
2. Which RTT code to use and WHY
3. NHS commenting style (exact format to copy)
4. Next actions required
5. Step-by-step teaching explanations

This is the TEACHING tool - shows you HOW to interpret!
"""

import streamlit as st
import json
from datetime import datetime
import io
import os
from openai import OpenAI

def extract_text_from_file(uploaded_file):
    """Extract text from uploaded file"""
    
    file_type = uploaded_file.name.split('.')[-1].lower()
    
    try:
        if file_type == 'txt':
            text = uploaded_file.read().decode('utf-8')
            return True, text
        
        elif file_type == 'pdf':
            try:
                import PyPDF2
                pdf_reader = PyPDF2.PdfReader(uploaded_file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()
                return True, text
            except Exception as e:
                return False, f"PDF extraction error: {str(e)}"
        
        elif file_type in ['docx', 'doc']:
            try:
                import docx
                doc = docx.Document(uploaded_file)
                text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
                return True, text
            except Exception as e:
                return False, f"DOCX extraction error: {str(e)}"
        
        else:
            return False, f"Unsupported file type: {file_type}"
    
    except Exception as e:
        return False, f"File processing error: {str(e)}"


def ai_educational_interpretation(letter_text):
    """
    AI provides EDUCATIONAL interpretation
    Shows HOW to interpret the letter step-by-step
    """
    
    try:
        api_key = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
        
        if not api_key:
            return basic_educational_interpretation(letter_text)
        
        client = OpenAI(api_key=api_key)
        
        prompt = f"""
        You are a T21 Services NHS RTT validation trainer. Analyze this clinical letter and provide EDUCATIONAL interpretation.
        
        CRITICAL: Return ONLY the scenarios that apply to THIS specific letter. Do NOT return all possible scenarios.
        
        TEACH the user HOW to interpret THIS letter step-by-step using OFFICIAL T21 COMMENTING STYLES.
        
        T21 OFFICIAL COMMENT FORMATS (ENHANCED WITH FULL DETAILS):
        
        CLOCK CONTINUES: [DATE] T21 - [DETAILED ACTION WITH CONTEXT]
        
        REFERRAL Examples with FULL DETAILS (Validator must CHECK PBL and appointment status):
        - REF REC'D [REF_DATE] FOR [CONDITION] - PT NOT ON PBL - AWAITING 1ST OPA [SPECIALTY]
        - REF REC'D [REF_DATE] FOR [CONDITION] - PT ON PBL - AWAITING 1ST OPA [SPECIALTY]
        - REF REC'D [REF_DATE] FOR [CONDITION] - 1ST OPA [DATE] [SPECIALTY] (appointment booked)
        - REF REC'D [REF_DATE] FOR [CONDITION] - 1ST OPA ATTENDED [DATE] [SPECIALTY]
        
        DIAGNOSTIC Examples (Validator must CHECK test status):
        - AWAITING DSG [TEST NAME] FOR [CONDITION] (test NOT booked yet)
        - DSG [TEST NAME] [DATE] FOR [CONDITION] (test BOOKED but not done yet - check date!)
        - DXG [TEST NAME] [DATE] FOR [CONDITION] - AWAITING RESULTS (test DONE, waiting for results)
        - DXG [TEST NAME] [DATE] FOR [CONDITION] - RESULTS: [OUTCOME] (test DONE, results received)
        
        SURGERY Examples (Validator must CHECK waiting list and TCI status):
        - REF FOR [PROCEDURE] FOR [CONDITION] - PT NOT ON WAITING LIST - REQUIRES WL ENTRY
        - PT ON WAITING LIST FOR [PROCEDURE] FOR [CONDITION] - AWAITING 1CL
        - 1CL [DATE] [PROCEDURE] FOR [CONDITION] (TCI date set)
        - SURGERY COMPLETED [DATE] [PROCEDURE] FOR [CONDITION]
        
        FOLLOW-UP Examples (Validator must CHECK booking and attendance):
        - F/U APPT REQUIRED POST [TREATMENT/EVENT] FOR [CONDITION] - NOT BOOKED
        - F/U APPT [DATE] POST [TREATMENT/EVENT] FOR [CONDITION] (booked but not done)
        - F/U APPT ATTENDED [DATE] POST [TREATMENT/EVENT] FOR [CONDITION]
        
        CLOCK STOPS: CS ([STOP_DATE])([CODE]) [INITIALS] DETAILED REASON WITH CONTEXT
        Examples with FULL DETAILS:
        - CS (23/04/2025)(30) JDS PT RCVD [TREATMENT NAME] FOR [CONDITION]. F/U APPT [DATE] BOOKED
        - CS (23/04/2025)(30) JDS PT RCVD [TREATMENT NAME] FOR [CONDITION]. F/U APPT REQUIRED IN [WEEKS]
        - CS (15/09/2025)(34) MOD PT DISCHARGED - [DIAGNOSIS] - NO FURTHER TX REQUIRED
        - CS (15/09/2025)(34) MOD PT DISCHARGED BACK TO GP - [CONDITION] RESOLVED
        
        CLINICAL LETTER:
        {letter_text}
        
        Provide JSON with TEACHING explanations using T21 official formats:
        
        {{
            "step1_identify_letter_type": {{
                "letter_type": "Referral/Clinic Outcome/Results/Discharge",
                "how_you_know": "Explain the KEY PHRASES that identify this type",
                "teaching_point": "What to look for in similar letters"
            }},
            "step2_extract_key_info": {{
                "patient_name": "name",
                "nhs_number": "number",
                "letter_date": "date",
                "clinic_date": "date if mentioned",
                "consultant": "name",
                "specialty": "specialty",
                "teaching": "Explain WHERE to find this info in letters"
            }},
            "step3_understand_content": {{
                "what_happened": "Explain what clinically happened",
                "diagnosis": "diagnosis if any",
                "treatment_given": "treatment if any",
                "plan_stated": "what the plan is",
                "teaching": "How to identify PAST vs FUTURE actions"
            }},
            "step4_determine_rtt_code": {{
                "suggested_code": "RTT code number",
                "code_name": "Code name (e.g., First Definitive Treatment)",
                "why_this_code": "DETAILED explanation of why this code applies",
                "clock_action": "START/STOP/PAUSE/CONTINUE",
                "teaching": "How to recognize this scenario in future letters"
            }},
            "step5_nhs_comment_format": {{
                "comment_format": "Use T21 ENHANCED format with FULL DETAILS from letter",
                "format_if_clock_continues": "[DATE] T21 - [DETAILED ACTION WITH CONTEXT]",
                "format_if_clock_stops": "CS ([STOP_DATE])([CODE]) [INITIALS] DETAILED REASON WITH CONTEXT",
                "comment_line": "T21 enhanced format with condition, treatment, dates, etc.",
                "comment_breakdown": "Include ALL relevant details: referral date, condition, treatment name, specialty, etc.",
                "critical_point": "MUST include: What (action), When (dates), Why (condition/diagnosis), Where (specialty)",
                
                "referral_scenarios": {{
                    "not_on_pbl": "{{today_date}} T21 - REF REC'D {{ref_date}} FOR {{condition}} - PT NOT ON PBL - AWAITING 1ST OPA {{specialty}}",
                    "on_pbl_no_apt": "{{today_date}} T21 - REF REC'D {{ref_date}} FOR {{condition}} - PT ON PBL - AWAITING 1ST OPA {{specialty}}",
                    "apt_booked": "{{today_date}} T21 - REF REC'D {{ref_date}} FOR {{condition}} - 1ST OPA {{apt_date}} {{specialty}}",
                    "apt_attended": "{{today_date}} T21 - REF REC'D {{ref_date}} FOR {{condition}} - 1ST OPA ATTENDED {{apt_date}} {{specialty}}",
                    "validator_must_check": "Check: Is PT on PBL? Is appointment booked? Has appointment happened? Comment what you FIND!",
                    "example": "18/10/2025 T21 - REF REC'D 01/10/2025 FOR CHEST PAIN - PT ON PBL - AWAITING 1ST OPA CARDIOLOGY"
                }} (ONLY include if letter is a REFERRAL),
                
                "diagnostic_scenarios": {{
                    "awaiting_not_booked": "{{today_date}} T21 - AWAITING DSG [{{test_name}}] FOR {{condition}}",
                    "booked_not_done": "{{today_date}} T21 - DSG [{{test_name}}] {{test_date}} FOR {{condition}}",
                    "done_awaiting_results": "{{today_date}} T21 - DXG [{{test_name}}] {{test_date}} FOR {{condition}} - AWAITING RESULTS",
                    "done_results_received": "{{today_date}} T21 - DXG [{{test_name}}] {{test_date}} FOR {{condition}} - RESULTS: {{outcome}}",
                    "validator_must_check": "Check: Is test booked? Has test date passed? Are results available? Comment based on what you FIND!",
                    "example": "Check date and status, then use: AWAITING DSG (not booked) | DSG [date] (booked but not done) | DXG [date] AWAITING RESULTS (done, no results) | DXG [date] RESULTS: [outcome] (results received)"
                }} (ONLY include if letter mentions DIAGNOSTIC tests),
                
                "treatment_scenarios": {{
                    "basic": "CS ({{tx_date}})(30) {{init}} PT RCVD {{treatment_name}} FOR {{condition}}",
                    "with_followup_booked": "CS ({{tx_date}})(30) {{init}} PT RCVD {{treatment_name}} FOR {{condition}}. F/U APT {{fu_date}} BOOKED",
                    "with_followup_weeks": "CS ({{tx_date}})(30) {{init}} PT RCVD {{treatment_name}} FOR {{condition}}. F/U APPT REQUIRED IN {{weeks}} WEEKS",
                    "example": "CS (10/10/2025)(30) TSO PT RCVD ANTIBIOTICS FOR CHEST INFECTION. F/U APPT 15/11/2025 BOOKED"
                }} (ONLY include if letter mentions TREATMENT given),
                
                "surgery_scenarios": {{
                    "not_on_wl": "{{today_date}} T21 - REF FOR {{procedure}} FOR {{condition}} - PT NOT ON WAITING LIST - REQUIRES WL ENTRY",
                    "on_wl_no_tci": "{{today_date}} T21 - PT ON WAITING LIST FOR {{procedure}} FOR {{condition}} - AWAITING 1CL",
                    "tci_set": "{{today_date}} T21 - 1CL {{surgery_date}} {{procedure}} FOR {{condition}}",
                    "surgery_done": "{{today_date}} T21 - SURGERY COMPLETED {{surgery_date}} {{procedure}} FOR {{condition}}",
                    "validator_must_check": "Check: Is PT on waiting list? Is TCI date set? Has surgery happened? Comment what you FIND!",
                    "example": "18/10/2025 T21 - PT ON WAITING LIST FOR KNEE ARTHROSCOPY FOR MENISCAL TEAR - AWAITING 1CL"
                }} (ONLY include if letter mentions SURGERY/procedure),
                
                "followup_scenarios": {{
                    "needed_not_booked": "{{today_date}} T21 - F/U APPT REQUIRED POST {{treatment_event}} FOR {{condition}} - NOT BOOKED",
                    "booked_not_done": "{{today_date}} T21 - F/U APPT {{apt_date}} POST {{treatment_event}} FOR {{condition}}",
                    "attended": "{{today_date}} T21 - F/U APPT ATTENDED {{apt_date}} POST {{treatment_event}} FOR {{condition}}",
                    "validator_must_check": "Check: Is F/U booked? Has F/U date passed? Was F/U attended? Comment what you FIND!",
                    "example": "18/10/2025 T21 - F/U APPT 15/11/2025 POST TREATMENT FOR CHEST INFECTION"
                }} (ONLY include if letter mentions FOLLOW-UP needed),
                
                "discharge_scenarios": {{
                    "basic": "CS ({{discharge_date}})(34) {{init}} PT DISCHARGED - {{diagnosis}} - NO FURTHER TX REQUIRED",
                    "to_gp": "CS ({{discharge_date}})(34) {{init}} PT DISCHARGED BACK TO GP - {{condition}} RESOLVED",
                    "example": "CS (15/09/2025)(34) TSO PT DISCHARGED - HYPERTENSION CONTROLLED - NO FURTHER TX REQUIRED"
                }} (ONLY include if letter is DISCHARGE),
                
                "teaching": "ALWAYS include FULL DETAILS: referral dates, condition/diagnosis, treatment names, test results, specialty. Make comments informative!"
            }},
            "step6_next_actions": {{
                "actions_required": [
                    "1. CHECK relevant systems based on letter content",
                    "2. For REFERRALS: Check PBL/appointment system - is 1st OPA booked?",
                    "3. For TREATMENT: Check if follow-up appointment booked (if letter mentions review)",
                    "4. For DIAGNOSTICS: Check if test booked/done",
                    "5. For SURGERY: Check if TCI date set",
                    "6. Update RTT code in PAS",
                    "7. Add T21 format comment based on what you FOUND"
                ],
                "check_workflow": {{
                    "referral": "Check PBL → If no appointment: 'AWAITING 1ST OPA' | If booked: '1ST OPA {{date}}'",
                    "treatment": "Check appointments → If follow-up booked: 'F/U APPT BOOKED' | If not: 'F/U APPT REQUIRED'",
                    "diagnostic": "Check diagnostic system → If booked: 'DSG [TEST] {{date}}' | If not: 'AWAITING DSG [TEST]'",
                    "surgery": "Check waiting list → If TCI set: '1CL {{date}}' | If not: 'AWAITING 1CL'"
                }},
                "critical_point": "ALWAYS CHECK systems BEFORE commenting. Use T21 official format showing what you FOUND!",
                "teaching": "T21 comment must reflect REALITY (what you found) not assumptions. Check first, comment second!"
            }},
            "step7_common_mistakes": {{
                "mistakes_to_avoid": ["Common errors for this letter type"],
                "why_mistakes_happen": "Explanation",
                "how_to_avoid": "Tips to avoid errors"
            }},
            "interpretation_confidence": "High/Medium/Low",
            "learning_summary": "Key takeaways from this letter"
        }}
        
        Be EDUCATIONAL - explain WHY, not just WHAT.
        
        CRITICAL INSTRUCTION: Only return scenario sections that are RELEVANT to this letter.
        Example: If it's a REFERRAL letter, return referral_scenarios. If it mentions tests, also return diagnostic_scenarios.
        Do NOT return surgery_scenarios if the letter doesn't mention surgery.
        Do NOT return discharge_scenarios if it's not a discharge letter.
        """
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an NHS RTT validation trainer. Teach users HOW to interpret clinical letters step-by-step with detailed explanations."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=3000
        )
        
        result = json.loads(response.choices[0].message.content)
        return result
        
    except Exception as e:
        st.warning(f"AI interpretation unavailable: {e}")
        return basic_educational_interpretation(letter_text)


def basic_educational_interpretation(letter_text):
    """Fallback basic interpretation - returns ONLY relevant scenarios"""
    
    letter_lower = letter_text.lower()
    
    # Detect letter type and what it contains
    is_referral = any(word in letter_lower for word in ['refer', 'referral', 'i am writing to refer'])
    is_discharge = any(word in letter_lower for word in ['discharg', 'no further', 'no treatment required'])
    is_treatment = any(word in letter_lower for word in ['treatment', 'medication prescribed', 'procedure completed'])
    has_tests = any(word in letter_lower for word in ['x-ray', 'mri', 'ct scan', 'ultrasound', 'blood test', 'investigation'])
    has_surgery = any(word in letter_lower for word in ['surgery', 'operation', 'procedure'])
    has_followup = any(word in letter_lower for word in ['follow-up', 'follow up', 'review appointment', 'see again'])
    
    # Determine primary letter type
    if is_referral:
        letter_type = "Referral Letter"
        suggested_code = "10"
        code_name = "Referral (Clock Start)"
        clock_action = "START"
        t21_format = f"{datetime.now().strftime('%d/%m/%Y')} T21 - REF REC'D [REF_DATE] FOR [CONDITION] - AWAITING 1ST OPA [SPECIALTY]"
    elif is_discharge:
        letter_type = "Discharge Letter"
        suggested_code = "34"
        code_name = "Discharge (Clock Stop)"
        clock_action = "STOP"
        t21_format = "CS ([DISCHARGE_DATE])(34) [INITIALS] PT DISCHARGED - [DIAGNOSIS] - NO FURTHER TX REQUIRED"
    elif is_treatment:
        letter_type = "Treatment Letter"
        suggested_code = "30"
        code_name = "First Definitive Treatment (Clock Stop)"
        clock_action = "STOP"
        t21_format = "CS ([TREATMENT_DATE])(30) [INITIALS] PT RCVD [TREATMENT_NAME] FOR [CONDITION]"
    else:
        letter_type = "Clinic Outcome Letter"
        suggested_code = "20"
        code_name = "Decision to Treat (Clock Continues)"
        clock_action = "CONTINUE"
        t21_format = "[DATE] T21 - [ACTION BASED ON LETTER]"
    
    # Build result with ONLY relevant scenarios
    result = {
        "step1_identify_letter_type": {
            "letter_type": letter_type,
            "how_you_know": "Based on key phrases in the letter",
            "teaching_point": "Look for referral/discharge/treatment keywords"
        },
        "step2_extract_key_info": {
            "patient_name": "Check letter header",
            "nhs_number": "Usually in header or first paragraph",
            "letter_date": "Top of letter",
            "teaching": "Always verify patient demographics first"
        },
        "step3_understand_content": {
            "what_happened": "Analyze letter content",
            "plan_stated": "Review what the letter says will happen next",
            "teaching": "Identify PAST actions (done) vs FUTURE actions (to do)"
        },
        "step4_determine_rtt_code": {
            "suggested_code": suggested_code,
            "code_name": code_name,
            "clock_action": clock_action,
            "why_this_code": f"This appears to be a {letter_type}",
            "teaching": "Match letter content to RTT code definitions"
        },
        "step5_nhs_comment_format": {
            "comment_format": "T21 ENHANCED FORMAT WITH FULL DETAILS",
            "format_clock_continues": "[DATE] T21 - [DETAILED ACTION WITH CONTEXT]",
            "format_clock_stops": "CS ([DATE])([CODE]) [INITIALS] DETAILED REASON WITH CONTEXT",
            "comment_line": t21_format,
            "comment_breakdown": f"Use T21 enhanced format. Clock {clock_action}s. Include ALL details: dates, conditions, treatments",
            "critical_point": "CHECK systems FIRST. Include FULL DETAILS: referral date, condition, treatment name, specialty, test results!",
            "teaching": "T21 enhanced formats include ALL relevant details from letter. Make comments informative and clear!"
        },
        "step6_next_actions": {
            "actions_required": [],
            "teaching": "Check relevant systems based on letter content"
        },
        "interpretation_confidence": "Medium"
    }
    
    # Add ONLY relevant scenario sections
    if is_referral:
        result["step5_nhs_comment_format"]["referral_scenarios"] = {
            "not_on_pbl": f"{datetime.now().strftime('%d/%m/%Y')} T21 - REF REC'D [REF_DATE] FOR [CONDITION] - PT NOT ON PBL - AWAITING 1ST OPA [SPECIALTY]",
            "on_pbl_no_apt": f"{datetime.now().strftime('%d/%m/%Y')} T21 - REF REC'D [REF_DATE] FOR [CONDITION] - PT ON PBL - AWAITING 1ST OPA [SPECIALTY]",
            "apt_booked": f"{datetime.now().strftime('%d/%m/%Y')} T21 - REF REC'D [REF_DATE] FOR [CONDITION] - 1ST OPA [DATE] [SPECIALTY]",
            "apt_attended": f"{datetime.now().strftime('%d/%m/%Y')} T21 - REF REC'D [REF_DATE] FOR [CONDITION] - 1ST OPA ATTENDED [DATE] [SPECIALTY]",
            "validator_must_check": "Validator must CHECK: Is PT on PBL? Is appointment booked? Has appointment happened?",
            "example": "18/10/2025 T21 - REF REC'D 01/10/2025 FOR CHEST PAIN - PT ON PBL - AWAITING 1ST OPA CARDIOLOGY"
        }
        result["step6_next_actions"]["actions_required"].append("Check if patient is on Partial Booking List (PBL)")
        result["step6_next_actions"]["actions_required"].append("Check if 1st OPA appointment is booked")
        result["step6_next_actions"]["pbl_check_critical"] = "ALWAYS check PBL for referrals"
    
    if has_tests:
        result["step5_nhs_comment_format"]["diagnostic_scenarios"] = {
            "awaiting_not_booked": f"{datetime.now().strftime('%d/%m/%Y')} T21 - AWAITING DSG [TEST_NAME] FOR [CONDITION]",
            "booked_not_done": f"{datetime.now().strftime('%d/%m/%Y')} T21 - DSG [TEST_NAME] [TEST_DATE] FOR [CONDITION]",
            "done_awaiting_results": f"{datetime.now().strftime('%d/%m/%Y')} T21 - DXG [TEST_NAME] [TEST_DATE] FOR [CONDITION] - AWAITING RESULTS",
            "done_results_received": f"{datetime.now().strftime('%d/%m/%Y')} T21 - DXG [TEST_NAME] [TEST_DATE] FOR [CONDITION] - RESULTS: [OUTCOME]",
            "validator_must_check": "Validator must CHECK: Is test booked? Has test date passed? Are results available?",
            "example": "Check system then comment: Not booked → AWAITING DSG | Booked not done → DSG [date] | Done no results → DXG AWAITING RESULTS | Results in → DXG RESULTS: [outcome]"
        }
        result["step6_next_actions"]["actions_required"].append("Check if diagnostic test is booked/completed")
    
    if is_treatment:
        result["step5_nhs_comment_format"]["treatment_scenarios"] = {
            "basic": "CS ([TX_DATE])(30) [INIT] PT RCVD [TREATMENT_NAME] FOR [CONDITION]",
            "with_followup_booked": "CS ([TX_DATE])(30) [INIT] PT RCVD [TREATMENT_NAME] FOR [CONDITION]. F/U APPT [DATE] BOOKED",
            "with_followup_weeks": "CS ([TX_DATE])(30) [INIT] PT RCVD [TREATMENT_NAME] FOR [CONDITION]. F/U APPT REQUIRED IN [WEEKS] WEEKS",
            "example": "CS (10/10/2025)(30) TSO PT RCVD ANTIBIOTICS FOR CHEST INFECTION. F/U APPT 15/11/2025 BOOKED"
        }
        result["step6_next_actions"]["actions_required"].append("Check if follow-up appointment is booked (if needed)")
    
    if has_surgery:
        result["step5_nhs_comment_format"]["surgery_scenarios"] = {
            "not_on_wl": f"{datetime.now().strftime('%d/%m/%Y')} T21 - REF FOR [PROCEDURE] FOR [CONDITION] - PT NOT ON WAITING LIST - REQUIRES WL ENTRY",
            "on_wl_no_tci": f"{datetime.now().strftime('%d/%m/%Y')} T21 - PT ON WAITING LIST FOR [PROCEDURE] FOR [CONDITION] - AWAITING 1CL",
            "tci_set": f"{datetime.now().strftime('%d/%m/%Y')} T21 - 1CL [SURGERY_DATE] [PROCEDURE] FOR [CONDITION]",
            "surgery_done": f"{datetime.now().strftime('%d/%m/%Y')} T21 - SURGERY COMPLETED [SURGERY_DATE] [PROCEDURE] FOR [CONDITION]",
            "validator_must_check": "Validator must CHECK: Is PT on waiting list? Is TCI date set? Has surgery happened?",
            "example": "18/10/2025 T21 - PT ON WAITING LIST FOR KNEE ARTHROSCOPY FOR MENISCAL TEAR - AWAITING 1CL"
        }
        result["step6_next_actions"]["actions_required"].append("Check if patient is on surgical waiting list")
        result["step6_next_actions"]["actions_required"].append("Check if TCI (To Come In) date is set")
    
    if has_followup:
        result["step5_nhs_comment_format"]["followup_scenarios"] = {
            "needed_not_booked": f"{datetime.now().strftime('%d/%m/%Y')} T21 - F/U APPT REQUIRED POST [TREATMENT/EVENT] FOR [CONDITION] - NOT BOOKED",
            "booked_not_done": f"{datetime.now().strftime('%d/%m/%Y')} T21 - F/U APPT [DATE] POST [TREATMENT/EVENT] FOR [CONDITION]",
            "attended": f"{datetime.now().strftime('%d/%m/%Y')} T21 - F/U APPT ATTENDED [DATE] POST [TREATMENT/EVENT] FOR [CONDITION]",
            "validator_must_check": "Validator must CHECK: Is F/U booked? Has F/U date passed? Was F/U attended?",
            "example": "18/10/2025 T21 - F/U APPT 15/11/2025 POST TREATMENT FOR CHEST INFECTION"
        }
        result["step6_next_actions"]["actions_required"].append("Check if follow-up appointment is booked")
    
    if is_discharge:
        result["step5_nhs_comment_format"]["discharge_scenarios"] = {
            "basic": "CS ([DISCHARGE_DATE])(34) [INIT] PT DISCHARGED - [DIAGNOSIS] - NO FURTHER TX REQUIRED",
            "to_gp": "CS ([DISCHARGE_DATE])(34) [INIT] PT DISCHARGED BACK TO GP - [CONDITION] RESOLVED",
            "example": "CS (15/09/2025)(34) TSO PT DISCHARGED - HYPERTENSION CONTROLLED - NO FURTHER TX REQUIRED"
        }
        result["step6_next_actions"]["actions_required"].append("Verify pathway is closed in PAS")
    
    # Always add these
    result["step6_next_actions"]["actions_required"].append("Update RTT code in PAS")
    result["step6_next_actions"]["actions_required"].append("Add T21 validation comment with today's date")
    
    return result


def render_clinic_letter_interpreter():
    """Main clinic letter interpreter with Teaching and Validation modes"""
    
    st.title("📝 Clinic Letter Interpreter")
    
    # MODE SELECTION
    col1, col2 = st.columns([3, 2])
    
    with col1:
        mode = st.radio(
            "**Select Mode:**",
            ["🎓 Teaching Mode (Show all scenarios)", "⚡ Validation Mode (Give me the comment!)"],
            horizontal=True,
            help="Teaching: Learn all options | Validation: Get quick answer for real work"
        )
    
    with col2:
        if mode == "🎓 Teaching Mode (Show all scenarios)":
            st.info("📚 **Learning Mode Active**")
        else:
            st.success("⚡ **Fast Validation Active**")
    
    # Store mode in session state
    is_teaching_mode = "Teaching" in mode
    
    if is_teaching_mode:
        st.caption("Learn HOW to interpret clinic letters step-by-step")
        st.info("""
        **🎓 This Tool TEACHES You:**
        1. How to READ and understand clinic letters
        2. Which RTT code to use and WHY
        3. NHS commenting format (exact text to write)
        4. Next actions required
        5. Common mistakes to avoid
        
        Perfect for training and learning!
        """)
    else:
        st.caption("Fast validation for working NHS staff - Get the comment in seconds!")
        st.success("""
        **⚡ Validation Mode:**
        1. Upload letter → Get instant analysis
        2. Shows what to CHECK in systems (PBL, appointments, etc.)
        3. Gives you ONE specific comment to use
        4. Flags discrepancies automatically
        
        **30X faster than manual validation!**
        """)
    
    # Step 1: Upload letter
    st.markdown("---")
    st.markdown("### 📄 Step 1: Provide Clinical Letter")
    
    input_method = st.radio(
        "Choose input method:",
        ["📎 Upload File (PDF/DOCX/TXT)", "📝 Paste Text"],
        horizontal=True
    )
    
    letter_text = None
    interpretation = None
    
    if input_method == "📎 Upload File (PDF/DOCX/TXT)":
        uploaded_file = st.file_uploader(
            "Upload clinical letter",
            type=['pdf', 'docx', 'doc', 'txt']
        )
        
        if uploaded_file:
            st.success(f"✅ File uploaded: {uploaded_file.name}")
            
            with st.spinner("📄 Extracting text..."):
                success, result = extract_text_from_file(uploaded_file)
            
            if success:
                letter_text = result
                st.success(f"✅ Text extracted! ({len(letter_text)} characters)")
                
                with st.expander("📄 View Letter Text"):
                    st.text_area("Letter Content", letter_text, height=300)
            else:
                st.error(f"❌ {result}")
    
    else:
        letter_text = st.text_area(
            "Paste clinical letter:",
            height=300,
            placeholder="Paste the full clinical letter here..."
        )
        
        if letter_text:
            st.success(f"✅ Letter provided ({len(letter_text)} characters)")
    
    # Interpret button (text changes based on mode)
    if letter_text:
        button_text = "🎓 Interpret & Teach Me" if is_teaching_mode else "⚡ Analyze Letter (Fast Validation)"
        spinner_text = "🤖 AI analyzing and preparing teaching explanation..." if is_teaching_mode else "⚡ Fast analysis in progress..."
        
        if st.button(button_text, type="primary", use_container_width=True):
            with st.spinner(spinner_text):
                interpretation = ai_educational_interpretation(letter_text)
                st.session_state['interpretation'] = interpretation
                st.session_state['is_teaching_mode'] = is_teaching_mode  # Store mode
            
            success_msg = "✅ Educational interpretation complete!" if is_teaching_mode else "✅ Fast validation analysis complete!"
            st.success(success_msg)
            st.rerun()
    
    # Show interpretation
    if 'interpretation' in st.session_state:
        interpretation = st.session_state['interpretation']
        stored_mode = st.session_state.get('is_teaching_mode', True)
        
        st.markdown("---")
        
        # DIFFERENT DISPLAY BASED ON MODE
        if stored_mode:
            # TEACHING MODE - Show all scenarios
            st.markdown("## 🎓 STEP-BY-STEP INTERPRETATION GUIDE")
        else:
            # ========================================
            # VALIDATION MODE - DIFFERENT WORKFLOW
            # ========================================
            st.markdown("## ⚡ VALIDATION WORKFLOW")
            
            step2 = interpretation.get('step2_extract_key_info', {})
            step3 = interpretation.get('step3_understand_content', {})
            step4 = interpretation.get('step4_determine_rtt_code', {})
            step5 = interpretation.get('step5_nhs_comment_format', {})
            
            # Quick Summary
            st.success(f"""
            **Letter Type:** {interpretation.get('step1_identify_letter_type', {}).get('letter_type', 'Unknown')}
            **Patient:** {step2.get('patient_name', 'Not extracted')}
            **NHS Number:** {step2.get('nhs_number', 'Not extracted')}
            **Specialty:** {step2.get('specialty', 'Not extracted')}
            **RTT Code:** {step4.get('suggested_code', '?')} - {step4.get('code_name', 'Unknown')}
            **Clock:** {step4.get('clock_action', 'CONTINUE')}
            """)
            
            # SYSTEM CHECKS REQUIRED
            st.markdown("---")
            st.markdown("### 🔍 STEP 1: VERIFY IN SYSTEMS")
            st.error("""
            **🚨 CRITICAL: Check systems FIRST before writing comment!**
            
            You MUST verify the information across multiple systems.
            Do NOT just copy what the letter says!
            """)
            
            # Determine what type of letter to show relevant checks
            letter_type = interpretation.get('step1_identify_letter_type', {}).get('letter_type', '').lower()
            
            with st.expander("📋 System Verification Checklist", expanded=True):
                st.markdown("**Check these systems and record what you FIND:**")
                
                # PAS Check
                st.markdown("**1. PAS System:**")
                pas_check = st.radio(
                    "Patient details match?",
                    ["✅ All match", "❌ Mismatch found", "⚠️ Not checked yet"],
                    key="pas_check",
                    horizontal=True
                )
                if pas_check == "❌ Mismatch found":
                    st.text_input("Describe mismatch:", key="pas_mismatch")
                
                # PBL Check (if referral/waiting)
                if 'referral' in letter_type or 'waiting' in step3.get('plan_stated', '').lower():
                    st.markdown("**2. Partial Booking List (PBL):**")
                    pbl_status = st.radio(
                        "Is patient on PBL?",
                        ["✅ ON PBL", "❌ NOT on PBL", "⚠️ Not checked yet"],
                        key="pbl_check",
                        horizontal=True
                    )
                
                # Appointment Check
                st.markdown("**3. Appointments System:**")
                apt_status = st.radio(
                    "Appointment status:",
                    ["✅ Booked", "✅ Attended", "❌ NOT booked", "⚠️ Not checked yet"],
                    key="apt_check",
                    horizontal=True
                )
                if apt_status == "✅ Booked" or apt_status == "✅ Attended":
                    apt_date = st.date_input("Appointment date:", key="apt_date")
                
                # Referral Check
                if 'referral' in letter_type:
                    st.markdown("**4. Referral System:**")
                    ref_check = st.radio(
                        "Referral exists in system?",
                        ["✅ Yes", "❌ No", "⚠️ Not checked yet"],
                        key="ref_check",
                        horizontal=True
                    )
                    if ref_check == "✅ Yes":
                        ref_date = st.date_input("Referral date in system:", key="ref_date")
            
            # GENERATE COMMENT BASED ON FINDINGS
            st.markdown("---")
            st.markdown("### 💬 STEP 2: YOUR COMMENT")
            
            if st.button("✅ Generate Comment Based on My Checks", type="primary"):
                # Build comment based on what user selected
                today = datetime.now().strftime('%d/%m/%Y')
                
                # Get values from checks
                pbl_val = st.session_state.get('pbl_check', '')
                apt_val = st.session_state.get('apt_check', '')
                pas_val = st.session_state.get('pas_check', '')
                
                # Generate appropriate comment
                if 'referral' in letter_type:
                    specialty = step2.get('specialty', '[SPECIALTY]')
                    ref_date_val = st.session_state.get('ref_date', 'REF_DATE')
                    condition = step3.get('diagnosis', '') or step3.get('what_happened', '')[:50]
                    
                    if 'ON PBL' in pbl_val and 'NOT booked' in apt_val:
                        generated_comment = f"{today} T21 - REF REC'D {ref_date_val} FOR {condition} - PT ON PBL - AWAITING 1ST OPA {specialty}"
                    elif 'NOT on PBL' in pbl_val:
                        generated_comment = f"{today} T21 - REF REC'D {ref_date_val} FOR {condition} - PT NOT ON PBL - AWAITING 1ST OPA {specialty}"
                    elif 'Booked' in apt_val:
                        apt_date_val = st.session_state.get('apt_date', 'APT_DATE')
                        generated_comment = f"{today} T21 - REF REC'D {ref_date_val} FOR {condition} - 1ST OPA {apt_date_val} {specialty}"
                    elif 'Attended' in apt_val:
                        apt_date_val = st.session_state.get('apt_date', 'APT_DATE')
                        generated_comment = f"{today} T21 - REF REC'D {ref_date_val} FOR {condition} - 1ST OPA ATTENDED {apt_date_val} {specialty}"
                    else:
                        generated_comment = f"{today} T21 - REF REC'D [DATE] - AWAITING 1ST OPA {specialty}"
                else:
                    # Use suggested comment from interpretation
                    generated_comment = step5.get('comment_line', f"{today} T21 - [ACTION]")
                
                st.session_state['generated_comment'] = generated_comment
            
            # Show generated comment with copy button
            if 'generated_comment' in st.session_state:
                st.markdown("**✅ Your Comment (Ready to Use):**")
                comment = st.session_state['generated_comment']
                
                st.code(comment, language=None)
                
                col1, col2 = st.columns([1, 3])
                with col1:
                    if st.button("📋 Copy Comment"):
                        st.success("✅ Select the text above and press Ctrl+C to copy!")
                
                # Check for discrepancies
                if st.session_state.get('pas_check', '') == "❌ Mismatch found":
                    st.error("""
                    🚨 **DISCREPANCY DETECTED!**
                    
                    PAS data doesn't match letter. Investigate before finalizing comment.
                    You may need to flag this for correction.
                    """)
                
                # Show what was checked
                with st.expander("📊 Verification Summary", expanded=False):
                    st.markdown("**Your Checks:**")
                    st.write(f"- PAS: {st.session_state.get('pas_check', 'Not checked')}")
                    st.write(f"- PBL: {st.session_state.get('pbl_check', 'Not applicable')}")
                    st.write(f"- Appointments: {st.session_state.get('apt_check', 'Not checked')}")
                    st.write(f"- Referral: {st.session_state.get('ref_check', 'Not applicable')}")
                    
                    st.info("💡 Your comment reflects what you FOUND in systems, not just what letter says!")
            
            st.markdown("---")
            st.success("""
            ⚡ **Validation Complete!**
            
            You've:
            1. ✅ Verified information across systems
            2. ✅ Generated comment based on REALITY
            3. ✅ Ready to paste into PAS
            
            **This is professional validation work!** 👏
            """)
            
            # End of validation mode - don't show teaching content
            st.stop()
        
        # ========================================
        # TEACHING MODE CONTENT BELOW
        # ========================================
        # Step 1: Identify Letter Type
        st.markdown("### 📋 Step 1: Identify Letter Type")
        
        step1 = interpretation.get('step1_identify_letter_type', {})
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.info(f"**Letter Type:**\n\n{step1.get('letter_type', 'Unknown')}")
        
        with col2:
            st.markdown("**How I Know:**")
            st.write(step1.get('how_you_know', 'Based on content analysis'))
            
            st.markdown("**🎯 Teaching Point:**")
            st.success(step1.get('teaching_point', 'Look for key identifying phrases'))
        
        # Step 2: Extract Key Info
        st.markdown("---")
        st.markdown("### 👤 Step 2: Extract Key Information")
        
        step2 = interpretation.get('step2_extract_key_info', {})
        
        col_a, col_b = st.columns(2)
        
        with col_a:
            st.markdown("**Patient Details:**")
            st.write(f"• Name: {step2.get('patient_name', 'Not extracted')}")
            st.write(f"• NHS Number: {step2.get('nhs_number', 'Not extracted')}")
            st.write(f"• Specialty: {step2.get('specialty', 'Not extracted')}")
        
        with col_b:
            st.markdown("**Letter Details:**")
            st.write(f"• Letter Date: {step2.get('letter_date', 'Not extracted')}")
            st.write(f"• Clinic Date: {step2.get('clinic_date', 'Not specified')}")
            st.write(f"• Consultant: {step2.get('consultant', 'Not extracted')}")
        
        st.info(f"**🎯 Teaching:** {step2.get('teaching', 'Always verify patient demographics first')}")
        
        # Step 3: Understand Content
        st.markdown("---")
        st.markdown("### 📖 Step 3: Understand Letter Content")
        
        step3 = interpretation.get('step3_understand_content', {})
        
        st.markdown("**What Happened:**")
        st.write(step3.get('what_happened', 'Analyze clinical content'))
        
        if step3.get('diagnosis'):
            st.markdown("**Diagnosis:**")
            st.write(step3.get('diagnosis'))
        
        if step3.get('treatment_given'):
            st.markdown("**Treatment Given:**")
            st.write(step3.get('treatment_given'))
        
        st.markdown("**Plan:**")
        st.write(step3.get('plan_stated', 'Review stated plan'))
        
        st.info(f"**🎯 Teaching:** {step3.get('teaching', 'Distinguish between past actions (done) and future actions (to do)')}")
        
        # Step 4: RTT Code - THE IMPORTANT PART!
        st.markdown("---")
        st.markdown("### 🎯 Step 4: Determine RTT Code")
        
        step4 = interpretation.get('step4_determine_rtt_code', {})
        
        # Big prominent code display
        col_code, col_clock = st.columns(2)
        
        with col_code:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        padding: 20px; border-radius: 10px; text-align: center;">
                <h2 style="color: white; margin: 0;">RTT Code: {step4.get('suggested_code', '?')}</h2>
                <p style="color: white; margin: 5px 0 0 0;">{step4.get('code_name', 'Unknown')}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col_clock:
            clock_action = step4.get('clock_action', 'CONTINUE')
            clock_colors = {
                'START': '#4caf50',
                'STOP': '#f44336',
                'PAUSE': '#ff9800',
                'CONTINUE': '#2196f3'
            }
            color = clock_colors.get(clock_action, '#2196f3')
            
            st.markdown(f"""
            <div style="background-color: {color}; 
                        padding: 20px; border-radius: 10px; text-align: center;">
                <h2 style="color: white; margin: 0;">Clock: {clock_action}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("**Why This Code:**")
        st.success(step4.get('why_this_code', 'Code determination explanation'))
        
        st.info(f"**🎯 Teaching:** {step4.get('teaching', 'Learn to recognize this scenario in future letters')}")
        
        # Step 5: NHS Comment Format - CRITICAL!
        st.markdown("---")
        st.markdown("### 💬 Step 5: NHS Comment Format")
        
        step5 = interpretation.get('step5_nhs_comment_format', {})
        
        st.markdown("**EXACT Comment to Write in PAS:**")
        
        comment_line = step5.get('comment_line', '[DATE] [INITIALS] - CLINIC OUTCOME REVIEWED')
        
        st.code(comment_line, language=None)
        
        if st.button("📋 Copy Comment to Clipboard"):
            st.success("✅ Comment copied! (Use Ctrl+C to copy from the box above)")
        
        st.markdown("**Comment Breakdown:**")
        st.write(step5.get('comment_breakdown', 'Explanation of comment structure'))
        
        # Show T21 format types
        if step5.get('format_clock_continues') or step5.get('format_clock_stops'):
            st.markdown("**📋 T21 OFFICIAL FORMATS:**")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Clock CONTINUES:**")
                st.code(step5.get('format_clock_continues', '[DATE] T21 - [ACTION]'), language=None)
            with col2:
                st.markdown("**Clock STOPS:**")
                st.code(step5.get('format_clock_stops', 'CS ([DATE])([CODE]) [INIT] REASON'), language=None)
        
        # Show critical point
        if step5.get('critical_point'):
            st.error(f"🚨 **CRITICAL:** {step5.get('critical_point')}")
        
        # Show DETAILED examples for all scenarios
        if step5.get('referral_scenarios'):
            st.markdown("**📌 REFERRAL Examples - Validator Must CHECK PBL & Appointment Status:**")
            ref_ex = step5.get('referral_scenarios', {})
            
            if ref_ex.get('validator_must_check'):
                st.warning(f"**⚠️ {ref_ex.get('validator_must_check')}**")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**1️⃣ PT NOT on PBL:**")
                st.code(ref_ex.get('not_on_pbl', 'Example'), language=None)
                st.markdown("**2️⃣ PT ON PBL - no appointment:**")
                st.code(ref_ex.get('on_pbl_no_apt', 'Example'), language=None)
            with col2:
                st.markdown("**3️⃣ Appointment booked:**")
                st.code(ref_ex.get('apt_booked', 'Example'), language=None)
                st.markdown("**4️⃣ Appointment attended:**")
                st.code(ref_ex.get('apt_attended', 'Example'), language=None)
            
            if ref_ex.get('example'):
                st.info(f"**💡 Example:** {ref_ex.get('example')}")
        
        # Show diagnostic examples
        if step5.get('diagnostic_scenarios'):
            st.markdown("**🔬 DIAGNOSTIC Examples - Validator Must CHECK Date & Status:**")
            diag_ex = step5.get('diagnostic_scenarios', {})
            
            if diag_ex.get('validator_must_check'):
                st.warning(f"**⚠️ {diag_ex.get('validator_must_check')}**")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**1️⃣ Test NOT booked yet:**")
                st.code(diag_ex.get('awaiting_not_booked', 'Example'), language=None)
                st.markdown("**2️⃣ Test BOOKED but not done:**")
                st.code(diag_ex.get('booked_not_done', 'Example'), language=None)
            with col2:
                st.markdown("**3️⃣ Test DONE - awaiting results:**")
                st.code(diag_ex.get('done_awaiting_results', 'Example'), language=None)
                st.markdown("**4️⃣ Test DONE - results received:**")
                st.code(diag_ex.get('done_results_received', 'Example'), language=None)
            
            if diag_ex.get('example'):
                st.info(f"**💡 Workflow:** {diag_ex.get('example')}")
        
        # Show treatment examples
        if step5.get('treatment_scenarios'):
            st.markdown("**💊 TREATMENT Examples (Clock Stops - Enhanced):**")
            treat_ex = step5.get('treatment_scenarios', {})
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown("**No follow-up:**")
                st.code(treat_ex.get('basic', 'Example'), language=None)
            with col2:
                st.markdown("**Follow-up BOOKED:**")
                st.code(treat_ex.get('with_followup_booked', 'Example'), language=None)
            with col3:
                st.markdown("**Follow-up in X weeks:**")
                st.code(treat_ex.get('with_followup_weeks', 'Example'), language=None)
            if treat_ex.get('example'):
                st.info(f"**💡 Example:** {treat_ex.get('example')}")
        
        # Show surgery examples
        if step5.get('surgery_scenarios'):
            st.markdown("**🏥 SURGERY Examples - Validator Must CHECK Waiting List & TCI Status:**")
            surg_ex = step5.get('surgery_scenarios', {})
            
            if surg_ex.get('validator_must_check'):
                st.warning(f"**⚠️ {surg_ex.get('validator_must_check')}**")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**1️⃣ PT NOT on waiting list:**")
                st.code(surg_ex.get('not_on_wl', 'Example'), language=None)
                st.markdown("**2️⃣ PT ON waiting list - no TCI:**")
                st.code(surg_ex.get('on_wl_no_tci', 'Example'), language=None)
            with col2:
                st.markdown("**3️⃣ TCI date set:**")
                st.code(surg_ex.get('tci_set', 'Example'), language=None)
                st.markdown("**4️⃣ Surgery completed:**")
                st.code(surg_ex.get('surgery_done', 'Example'), language=None)
            
            if surg_ex.get('example'):
                st.info(f"**💡 Example:** {surg_ex.get('example')}")
        
        # Show follow-up examples
        if step5.get('followup_scenarios'):
            st.markdown("**📅 FOLLOW-UP Examples - Validator Must CHECK Booking & Attendance:**")
            fu_ex = step5.get('followup_scenarios', {})
            
            if fu_ex.get('validator_must_check'):
                st.warning(f"**⚠️ {fu_ex.get('validator_must_check')}**")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown("**F/U needed - NOT booked:**")
                st.code(fu_ex.get('needed_not_booked', 'Example'), language=None)
            with col2:
                st.markdown("**F/U booked - not done:**")
                st.code(fu_ex.get('booked_not_done', 'Example'), language=None)
            with col3:
                st.markdown("**F/U attended:**")
                st.code(fu_ex.get('attended', 'Example'), language=None)
            
            if fu_ex.get('example'):
                st.info(f"**💡 Example:** {fu_ex.get('example')}")
        
        # Show discharge examples
        if step5.get('discharge_scenarios'):
            st.markdown("**📋 DISCHARGE Examples (Clock Stops - Enhanced):**")
            disch_ex = step5.get('discharge_scenarios', {})
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Discharged - no further treatment:**")
                st.code(disch_ex.get('basic', 'Example'), language=None)
            with col2:
                st.markdown("**Discharged back to GP:**")
                st.code(disch_ex.get('to_gp', 'Example'), language=None)
            if disch_ex.get('example'):
                st.info(f"**💡 Example:** {disch_ex.get('example')}")
        
        if step5.get('format_rules'):
            st.markdown("**Format Rules:**")
            st.write(step5.get('format_rules'))
        
        st.info(f"**🎯 Teaching:** {step5.get('teaching', 'NHS comments follow standardized formats for consistency')}")
        
        # Step 6: Next Actions
        st.markdown("---")
        st.markdown("### ✅ Step 6: Next Actions Required")
        
        step6 = interpretation.get('step6_next_actions', {})
        
        # Show PBL check as CRITICAL
        if step6.get('pbl_check_critical'):
            st.error(f"🚨 **CRITICAL:** {step6.get('pbl_check_critical')}")
        
        st.markdown("**Actions to Complete:**")
        
        actions = step6.get('actions_required', [])
        for idx, action in enumerate(actions, 1):
            # Highlight PBL-related actions
            if 'PBL' in action or 'Partial Booking' in action or 'waiting list' in action:
                st.checkbox(f"**{idx}. 🔴 {action}**", key=f"action_{idx}")
            else:
                st.checkbox(f"**{idx}.** {action}", key=f"action_{idx}")
        
        if step6.get('priority_order'):
            st.markdown("**Priority Order:**")
            st.warning(step6.get('priority_order'))
        
        if step6.get('pas_updates_needed'):
            st.markdown("**PAS Updates Needed:**")
            for update in step6.get('pas_updates_needed', []):
                st.write(f"• {update}")
        
        st.info(f"**🎯 Teaching:** {step6.get('teaching', 'Always verify PAS matches letter content')}")
        
        # Step 7: Common Mistakes
        if 'step7_common_mistakes' in interpretation:
            st.markdown("---")
            st.markdown("### ⚠️ Step 7: Common Mistakes to Avoid")
            
            step7 = interpretation.get('step7_common_mistakes', {})
            
            mistakes = step7.get('mistakes_to_avoid', [])
            if mistakes:
                for mistake in mistakes:
                    st.error(f"❌ {mistake}")
            
            if step7.get('how_to_avoid'):
                st.markdown("**How to Avoid:**")
                st.success(step7.get('how_to_avoid'))
        
        # Learning Summary
        st.markdown("---")
        st.markdown("### 📚 Learning Summary")
        
        confidence = interpretation.get('interpretation_confidence', 'Medium')
        confidence_colors = {'High': '#4caf50', 'Medium': '#ff9800', 'Low': '#f44336'}
        confidence_color = confidence_colors.get(confidence, '#ff9800')
        
        st.markdown(f"""
        <div style="border-left: 5px solid {confidence_color}; padding: 15px; background-color: #f5f5f5;">
            <strong>Interpretation Confidence: {confidence}</strong>
        </div>
        """, unsafe_allow_html=True)
        
        if interpretation.get('learning_summary'):
            st.info(f"**Key Takeaways:** {interpretation.get('learning_summary')}")
        
        # Download option
        st.markdown("---")
        if st.button("📥 Download Interpretation Guide", type="primary"):
            report = generate_interpretation_report(interpretation, letter_text)
            
            st.download_button(
                label="💾 Download as TXT",
                data=report,
                file_name=f"letter_interpretation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )


def generate_interpretation_report(interpretation, letter_text):
    """Generate downloadable interpretation report"""
    
    step4 = interpretation.get('step4_determine_rtt_code', {})
    step5 = interpretation.get('step5_nhs_comment_format', {})
    
    report = f"""
    T21 CLINIC LETTER INTERPRETATION GUIDE
    {'='*60}
    
    Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    
    LETTER TYPE:
    {'='*60}
    {interpretation.get('step1_identify_letter_type', {}).get('letter_type', 'Unknown')}
    
    RTT CODE DETERMINATION:
    {'='*60}
    Suggested Code: {step4.get('suggested_code', '?')}
    Code Name: {step4.get('code_name', 'Unknown')}
    Clock Action: {step4.get('clock_action', 'CONTINUE')}
    
    Why This Code:
    {step4.get('why_this_code', 'Not specified')}
    
    NHS COMMENT FORMAT:
    {'='*60}
    {step5.get('comment_line', 'Not generated')}
    
    Comment Breakdown:
    {step5.get('comment_breakdown', 'Not provided')}
    
    NEXT ACTIONS:
    {'='*60}
    """
    
    actions = interpretation.get('step6_next_actions', {}).get('actions_required', [])
    for idx, action in enumerate(actions, 1):
        report += f"\n{idx}. {action}"
    
    report += f"""
    
    {'='*60}
    T21 Services Limited | www.t21services.co.uk
    NHS RTT Validation Training Platform
    {'='*60}
    """
    
    return report


# Export
__all__ = ['render_clinic_letter_interpreter']
