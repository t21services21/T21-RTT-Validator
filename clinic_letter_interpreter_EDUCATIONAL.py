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
        
        TEACH the user HOW to interpret this letter step-by-step using OFFICIAL T21 COMMENTING STYLES.
        
        T21 OFFICIAL COMMENT FORMATS:
        
        CLOCK CONTINUES: [DATE] T21 - [ACTION]
        Examples:
        - AWAITING 1ST OPA (referral, no appointment yet)
        - 1ST OPA [DATE] (first appointment booked)
        - AWAITING DSG [TEST NAME] (diagnostic test to be booked)
        - DSG [TEST NAME] [DATE] (diagnostic booked)
        - DXG [TEST NAME] [DATE] (diagnostic done)
        - AWAITING 1CL (waiting for surgery TCI date)
        - 1CL [DATE] (surgery date set)
        - AWAITING F/U APPT (follow-up needed)
        - F/U APPT [DATE] (follow-up booked)
        
        CLOCK STOPS: CS ([STOP_DATE])([CODE]) [INITIALS] REASON
        Examples:
        - CS (23/04/2025)(30) JDS PATIENT RCVD MEDICATION/TREATMENT. F/U APPT BOOKED
        - CS (15/09/2025)(34) MOD PATIENT DISCHARGED - NO TREATMENT REQUIRED
        
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
                "comment_format": "Use T21 OFFICIAL format based on clock action",
                "format_if_clock_continues": "[DATE] T21 - [ACTION]",
                "format_if_clock_stops": "CS ([STOP_DATE])([CODE]) [INITIALS] REASON",
                "comment_line": "T21 format based on letter content",
                "comment_breakdown": "Choose correct T21 format: Clock continues OR Clock stops",
                "critical_point": "MUST CHECK systems (PBL, appointments, diagnostics) and use correct T21 format based on what you FIND",
                
                "referral_scenarios": {{
                    "if_no_appointment": "{{today_date}} T21 - AWAITING 1ST OPA",
                    "if_appointment_booked": "{{today_date}} T21 - 1ST OPA {{appointment_date}}"
                }},
                
                "treatment_scenarios": {{
                    "treatment_no_followup": "CS ({{treatment_date}})(30) {{initials}} PATIENT RCVD MEDICATION/TREATMENT",
                    "treatment_with_followup_not_booked": "CS ({{treatment_date}})(30) {{initials}} PATIENT RCVD MEDICATION/TREATMENT. F/U APPT REQUIRED",
                    "treatment_with_followup_booked": "CS ({{treatment_date}})(30) {{initials}} PATIENT RCVD MEDICATION/TREATMENT. F/U APPT BOOKED"
                }},
                
                "discharge_scenarios": {{
                    "discharge": "CS ({{discharge_date}})(34) {{initials}} PATIENT DISCHARGED - NO TREATMENT REQUIRED"
                }},
                
                "teaching": "Use OFFICIAL T21 format. Check systems first, then choose correct format based on what you FIND!"
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
    """Fallback basic interpretation"""
    
    letter_lower = letter_text.lower()
    
    # Detect letter type
    if any(word in letter_lower for word in ['refer', 'referral', 'i am writing to refer']):
        letter_type = "Referral Letter"
        suggested_code = "10"
        code_name = "Referral (Clock Start)"
        clock_action = "START"
        t21_format = "[DATE] T21 - AWAITING 1ST OPA"
    elif any(word in letter_lower for word in ['discharg', 'no further', 'no treatment required']):
        letter_type = "Discharge Letter"
        suggested_code = "34"
        code_name = "Discharge (Clock Stop)"
        clock_action = "STOP"
        t21_format = "CS ([DISCHARGE_DATE])(34) [INITIALS] PATIENT DISCHARGED - NO TREATMENT REQUIRED"
    elif any(word in letter_lower for word in ['treatment', 'medication prescribed', 'procedure completed']):
        letter_type = "Treatment Letter"
        suggested_code = "30"
        code_name = "First Definitive Treatment (Clock Stop)"
        clock_action = "STOP"
        t21_format = "CS ([TREATMENT_DATE])(30) [INITIALS] PATIENT RCVD MEDICATION/TREATMENT"
    else:
        letter_type = "Clinic Outcome Letter"
        suggested_code = "20"
        code_name = "Decision to Treat (Clock Continues)"
        clock_action = "CONTINUE"
        t21_format = "[DATE] T21 - [ACTION BASED ON LETTER]"
    
    return {
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
            "teaching": "Identify PAST actions (done) vs FUTURE actions (to do)"
        },
        "step4_determine_rtt_code": {
            "suggested_code": suggested_code,
            "code_name": code_name,
            "why_this_code": f"This appears to be a {letter_type}",
            "teaching": "Match letter content to RTT code definitions"
        },
        "step5_nhs_comment_format": {
            "comment_format": "T21 OFFICIAL FORMAT",
            "format_clock_continues": "[DATE] T21 - [ACTION]",
            "format_clock_stops": "CS ([DATE])([CODE]) [INITIALS] REASON",
            "comment_line": t21_format,
            "comment_breakdown": f"Use T21 official format. Clock {clock_action}s → Use appropriate format",
            "referral_examples": {
                "if_no_appointment": f"{datetime.now().strftime('%d/%m/%Y')} T21 - AWAITING 1ST OPA",
                "if_appointment_booked": f"{datetime.now().strftime('%d/%m/%Y')} T21 - 1ST OPA [DATE]"
            },
            "treatment_examples": {
                "no_followup": f"CS ([TREATMENT_DATE])(30) [INIT] PATIENT RCVD MEDICATION/TREATMENT",
                "followup_booked": f"CS ([TREATMENT_DATE])(30) [INIT] PATIENT RCVD MEDICATION/TREATMENT. F/U APPT BOOKED",
                "followup_not_booked": f"CS ([TREATMENT_DATE])(30) [INIT] PATIENT RCVD MEDICATION/TREATMENT. F/U APPT REQUIRED"
            },
            "critical_point": "CHECK systems FIRST (PBL, appointments, etc.) then use correct T21 format based on what you FIND!",
            "teaching": "T21 official formats must be used. Choose format based on clock action and what you discovered when checking!"
        },
        "step6_next_actions": {
            "actions_required": [
                "Check if patient is on Partial Booking List (PBL)",
                "If letter says 'patient to be added to waiting list' - verify they ARE on PBL",
                "If NOT on PBL - escalate to booking team",
                "Update RTT code in PAS",
                "Add validation comment with today's date"
            ],
            "pbl_check_critical": "ALWAYS check PBL when letter mentions waiting list",
            "teaching": "PBL verification is FIRST priority - prevents patients being lost!"
        },
        "interpretation_confidence": "Medium"
    }


def render_clinic_letter_interpreter():
    """Main EDUCATIONAL clinic letter interpreter"""
    
    st.title("📝 Clinic Letter Interpreter - TEACHING MODE")
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
    
    # Interpret button
    if letter_text:
        if st.button("🎓 Interpret & Teach Me", type="primary", use_container_width=True):
            with st.spinner("🤖 AI analyzing and preparing teaching explanation..."):
                interpretation = ai_educational_interpretation(letter_text)
                st.session_state['interpretation'] = interpretation
            
            st.success("✅ Educational interpretation complete!")
            st.rerun()
    
    # Show interpretation
    if 'interpretation' in st.session_state:
        interpretation = st.session_state['interpretation']
        
        st.markdown("---")
        st.markdown("## 🎓 STEP-BY-STEP INTERPRETATION GUIDE")
        
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
        
        # Show critical point
        if step5.get('critical_point'):
            st.error(f"🚨 **CRITICAL:** {step5.get('critical_point')}")
        
        # Show PBL examples
        if step5.get('example_if_on_pbl') or step5.get('example_if_not_on_pbl'):
            st.markdown("**📋 PBL Check Workflow:**")
            st.info("**Step 1:** Go to PBL/Outpatient Waiting List system\n**Step 2:** Search for this patient\n**Step 3:** Is patient on the list?\n**Step 4:** Comment what you FOUND (see examples below)")
            st.markdown("**Comment Examples Based on What You FIND:**")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**If patient IS on PBL:**")
                st.code(step5.get('example_if_on_pbl', 'Check example'), language=None)
            with col2:
                st.markdown("**If patient NOT on PBL:**")
                st.code(step5.get('example_if_not_on_pbl', 'Check example'), language=None)
        
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
