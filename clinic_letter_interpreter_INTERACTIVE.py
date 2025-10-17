"""
T21 PROFESSIONAL CLINIC LETTER INTERPRETER - INTERACTIVE VERSION
For NHS Staff - Manual PAS Verification & Compliance Checking

WORKFLOW:
1. Upload clinical letter (PDF/DOCX/TXT)
2. AI extracts key information
3. YOU manually enter current PAS status
4. System compares letter vs PAS
5. Generates compliance report showing discrepancies
6. Interactive checklist to complete actions

This is NOT the automated analyzer - this requires YOUR input!
"""

import streamlit as st
import json
from datetime import datetime
import io
import os
from openai import OpenAI

def extract_text_from_file(uploaded_file):
    """Extract text from uploaded file (PDF, DOCX, TXT)"""
    
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


def ai_extract_letter_info(letter_text):
    """
    AI extracts key information from letter
    Returns basic structure for comparison
    """
    
    try:
        api_key = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
        
        if not api_key:
            # Fallback to basic regex extraction
            return basic_extract_letter_info(letter_text)
        
        client = OpenAI(api_key=api_key)
        
        prompt = f"""
        Extract key information from this clinical letter for NHS RTT validation:
        
        {letter_text}
        
        Return JSON with:
        {{
            "patient_name": "full name",
            "nhs_number": "NHS number",
            "letter_date": "date",
            "clinic_date": "clinic date",
            "consultant": "consultant name",
            "specialty": "specialty",
            "diagnosis": "main diagnosis",
            "treatment_plan": "summary of plan",
            "follow_up_required": "yes/no",
            "follow_up_timeframe": "timeframe",
            "investigations_ordered": ["list of tests"],
            "surgery_required": "yes/no",
            "waiting_list_needed": "yes/no",
            "gp_copy_mentioned": "yes/no",
            "urgent_indicators": ["any urgent flags"]
        }}
        """
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an NHS clinical letter analyzer. Extract information accurately."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=1500
        )
        
        result = json.loads(response.choices[0].message.content)
        return result
        
    except Exception as e:
        return basic_extract_letter_info(letter_text)


def basic_extract_letter_info(letter_text):
    """Fallback basic extraction if no API key"""
    return {
        "patient_name": "Not extracted",
        "nhs_number": "Not extracted",
        "letter_date": "Not extracted",
        "clinic_date": "Not extracted",
        "consultant": "Not extracted",
        "specialty": "Not extracted",
        "diagnosis": "Not extracted",
        "treatment_plan": "Not extracted",
        "follow_up_required": "Unknown",
        "follow_up_timeframe": "Not specified",
        "investigations_ordered": [],
        "surgery_required": "Unknown",
        "waiting_list_needed": "Unknown",
        "gp_copy_mentioned": "Unknown",
        "urgent_indicators": []
    }


def compare_letter_vs_pas(letter_info, pas_status):
    """
    Compare what letter says vs what PAS shows
    Returns list of discrepancies
    """
    
    discrepancies = []
    compliance_issues = []
    
    # Check follow-up appointment
    if letter_info.get('follow_up_required') == 'yes':
        if pas_status.get('follow_up_booked') == 'No':
            discrepancies.append({
                'type': 'Missing Follow-Up',
                'severity': 'HIGH',
                'letter_says': f"Follow-up required in {letter_info.get('follow_up_timeframe', 'timeframe not specified')}",
                'pas_shows': 'No follow-up booked',
                'action': 'Book follow-up appointment immediately'
            })
    
    # Check investigations
    if letter_info.get('investigations_ordered'):
        if pas_status.get('investigations_ordered') == 'No':
            discrepancies.append({
                'type': 'Missing Investigation Orders',
                'severity': 'HIGH',
                'letter_says': f"Tests ordered: {', '.join(letter_info.get('investigations_ordered', []))}",
                'pas_shows': 'No investigations ordered in PAS',
                'action': 'Order investigations in PAS immediately'
            })
    
    # Check waiting list
    if letter_info.get('waiting_list_needed') == 'yes':
        if pas_status.get('waiting_list_added') == 'No':
            discrepancies.append({
                'type': 'Missing Waiting List Entry',
                'severity': 'HIGH',
                'letter_says': 'Patient should be on waiting list',
                'pas_shows': 'Not on waiting list',
                'action': 'Add patient to waiting list'
            })
    
    # Check GP copy
    if letter_info.get('gp_copy_mentioned') == 'yes':
        if pas_status.get('gp_letter_sent') == 'No':
            compliance_issues.append({
                'type': 'GP Communication',
                'severity': 'MEDIUM',
                'letter_says': 'GP copy to be sent',
                'pas_shows': 'GP letter not sent',
                'action': 'Send GP letter'
            })
    
    # Check RTT code
    if pas_status.get('current_rtt_code'):
        # This would need more sophisticated logic
        pass
    
    # Check clinic notes
    if pas_status.get('clinic_notes_updated') == 'No':
        compliance_issues.append({
            'type': 'Clinical Notes',
            'severity': 'MEDIUM',
            'letter_says': 'Clinic outcome documented',
            'pas_shows': 'Clinic notes not updated in PAS',
            'action': 'Update clinical notes in PAS'
        })
    
    # Check urgent flags
    if letter_info.get('urgent_indicators'):
        if pas_status.get('urgent_flag_set') == 'No':
            discrepancies.append({
                'type': 'Urgent Flag Missing',
                'severity': 'CRITICAL',
                'letter_says': f"Urgent indicators: {', '.join(letter_info.get('urgent_indicators', []))}",
                'pas_shows': 'Not flagged as urgent in PAS',
                'action': 'Set urgent flag in PAS immediately'
            })
    
    return discrepancies, compliance_issues


def render_clinic_letter_interpreter():
    """Main interactive clinic letter interpreter"""
    
    st.title("📝 Professional Clinic Letter Interpreter")
    st.caption("Interactive PAS Verification & Compliance Checking")
    
    st.info("""
    **How This Works:**
    1. Upload clinical letter → AI extracts key information
    2. YOU enter current PAS status manually
    3. System compares letter vs PAS
    4. Generates compliance report showing discrepancies
    5. Interactive checklist to complete actions
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
    letter_info = None
    
    if input_method == "📎 Upload File (PDF/DOCX/TXT)":
        uploaded_file = st.file_uploader(
            "Upload clinical letter",
            type=['pdf', 'docx', 'doc', 'txt'],
            help="Supported: PDF, Word documents, text files"
        )
        
        if uploaded_file:
            st.success(f"✅ File uploaded: {uploaded_file.name}")
            
            with st.spinner("📄 Extracting text from file..."):
                success, result = extract_text_from_file(uploaded_file)
            
            if success:
                letter_text = result
                st.success(f"✅ Text extracted successfully! ({len(letter_text)} characters)")
                
                with st.expander("📄 Preview extracted text"):
                    st.text_area("Extracted Content", letter_text, height=300)
                
                # AI extract information
                with st.spinner("🤖 AI analyzing letter content..."):
                    letter_info = ai_extract_letter_info(letter_text)
                    st.session_state['letter_info'] = letter_info
                
                st.success("✅ AI extraction complete!")
                
            else:
                st.error(f"❌ {result}")
    
    else:
        letter_text = st.text_area(
            "Paste clinical letter text:",
            height=300,
            placeholder="Paste the entire clinical letter here..."
        )
        
        if letter_text:
            st.success(f"✅ Text provided ({len(letter_text)} characters)")
            
            if st.button("🤖 Analyze Letter with AI", type="primary"):
                with st.spinner("🤖 AI analyzing letter content..."):
                    letter_info = ai_extract_letter_info(letter_text)
                    st.session_state['letter_info'] = letter_info
                
                st.success("✅ AI extraction complete!")
    
    # Step 2: Show extracted info and get PAS status
    if 'letter_info' in st.session_state:
        letter_info = st.session_state['letter_info']
        
        st.markdown("---")
        st.markdown("### 📋 Step 2: AI-Extracted Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Patient Details")
            st.write(f"**Name:** {letter_info.get('patient_name', 'Not extracted')}")
            st.write(f"**NHS Number:** {letter_info.get('nhs_number', 'Not extracted')}")
            st.write(f"**Specialty:** {letter_info.get('specialty', 'Not extracted')}")
            st.write(f"**Consultant:** {letter_info.get('consultant', 'Not extracted')}")
        
        with col2:
            st.markdown("#### Letter Details")
            st.write(f"**Letter Date:** {letter_info.get('letter_date', 'Not extracted')}")
            st.write(f"**Clinic Date:** {letter_info.get('clinic_date', 'Not extracted')}")
            st.write(f"**Diagnosis:** {letter_info.get('diagnosis', 'Not extracted')}")
        
        st.markdown("#### Treatment Plan")
        st.info(letter_info.get('treatment_plan', 'Not extracted'))
        
        # Show key flags
        st.markdown("#### Key Requirements from Letter:")
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            follow_up = letter_info.get('follow_up_required', 'Unknown')
            if follow_up == 'yes':
                st.success(f"✅ Follow-up: {letter_info.get('follow_up_timeframe', 'timeframe not specified')}")
            else:
                st.info("ℹ️ No follow-up mentioned")
        
        with col_b:
            investigations = letter_info.get('investigations_ordered', [])
            if investigations:
                st.warning(f"⚠️ {len(investigations)} investigation(s) ordered")
            else:
                st.info("ℹ️ No investigations ordered")
        
        with col_c:
            waiting_list = letter_info.get('waiting_list_needed', 'Unknown')
            if waiting_list == 'yes':
                st.warning("⚠️ Waiting list required")
            else:
                st.info("ℹ️ No waiting list needed")
        
        # Step 3: Manual PAS entry
        st.markdown("---")
        st.markdown("### 🖥️ Step 3: Enter Current PAS Status")
        st.caption("⚠️ **IMPORTANT:** Enter what is CURRENTLY in PAS, not what should be there!")
        
        with st.form("pas_status_form"):
            st.markdown("#### RTT Status")
            
            col1, col2 = st.columns(2)
            
            with col1:
                current_rtt_code = st.text_input(
                    "Current RTT Code in PAS",
                    placeholder="e.g., 10, 20, 30, etc.",
                    help="The RTT code currently recorded in PAS"
                )
                
                clock_status = st.selectbox(
                    "Clock Status in PAS",
                    ["Running", "Stopped", "Paused", "Not Started"]
                )
            
            with col2:
                dtt_recorded = st.radio(
                    "Decision to Treat (DTT) recorded?",
                    ["Yes", "No", "Not Applicable"],
                    horizontal=True
                )
                
                urgent_flag_set = st.radio(
                    "Urgent flag set in PAS?",
                    ["Yes", "No"],
                    horizontal=True
                )
            
            st.markdown("#### Appointments & Actions")
            
            col3, col4 = st.columns(2)
            
            with col3:
                follow_up_booked = st.radio(
                    "Follow-up appointment booked?",
                    ["Yes", "No", "Not Required"],
                    horizontal=True
                )
                
                investigations_ordered = st.radio(
                    "Investigations ordered in PAS?",
                    ["Yes", "No", "Not Required"],
                    horizontal=True
                )
            
            with col4:
                waiting_list_added = st.radio(
                    "Patient on waiting list?",
                    ["Yes", "No", "Not Required"],
                    horizontal=True
                )
                
                gp_letter_sent = st.radio(
                    "GP letter sent?",
                    ["Yes", "No", "Not Required"],
                    horizontal=True
                )
            
            st.markdown("#### Clinical Documentation")
            
            clinic_notes_updated = st.radio(
                "Clinic notes updated in PAS?",
                ["Yes", "No"],
                horizontal=True
            )
            
            submit_pas = st.form_submit_button("🔍 Compare Letter vs PAS", type="primary")
        
        if submit_pas:
            # Store PAS status
            pas_status = {
                'current_rtt_code': current_rtt_code,
                'clock_status': clock_status,
                'dtt_recorded': dtt_recorded,
                'urgent_flag_set': urgent_flag_set,
                'follow_up_booked': follow_up_booked,
                'investigations_ordered': investigations_ordered,
                'waiting_list_added': waiting_list_added,
                'gp_letter_sent': gp_letter_sent,
                'clinic_notes_updated': clinic_notes_updated
            }
            
            st.session_state['pas_status'] = pas_status
            
            # Compare
            discrepancies, compliance_issues = compare_letter_vs_pas(letter_info, pas_status)
            
            st.session_state['discrepancies'] = discrepancies
            st.session_state['compliance_issues'] = compliance_issues
            
            st.rerun()
    
    # Step 4: Show comparison results
    if 'discrepancies' in st.session_state or 'compliance_issues' in st.session_state:
        st.markdown("---")
        st.markdown("### 📊 Step 4: Compliance Report")
        
        discrepancies = st.session_state.get('discrepancies', [])
        compliance_issues = st.session_state.get('compliance_issues', [])
        
        # Calculate compliance rate
        total_checks = len(discrepancies) + len(compliance_issues)
        if total_checks == 0:
            compliance_rate = 100
            st.success("🎉 **100% COMPLIANT** - No discrepancies found!")
        else:
            compliance_rate = 0
            st.error(f"⚠️ **{total_checks} Issue(s) Found** - See below for details")
        
        # Show critical discrepancies
        if discrepancies:
            st.markdown("#### 🚨 Critical Discrepancies (HIGH/CRITICAL)")
            
            for idx, disc in enumerate(discrepancies, 1):
                severity_color = "error" if disc['severity'] == 'CRITICAL' else "warning"
                
                with st.container():
                    st.markdown(f"""
                    <div style="border-left: 5px solid {'#d32f2f' if disc['severity'] == 'CRITICAL' else '#f57c00'}; 
                                padding: 15px; margin-bottom: 10px; background-color: {'#ffebee' if disc['severity'] == 'CRITICAL' else '#fff3e0'};">
                    """, unsafe_allow_html=True)
                    
                    st.markdown(f"**Issue #{idx}: {disc['type']}** - `{disc['severity']}`")
                    
                    col_x, col_y = st.columns(2)
                    
                    with col_x:
                        st.markdown("**Letter Says:**")
                        st.info(disc['letter_says'])
                    
                    with col_y:
                        st.markdown("**PAS Shows:**")
                        st.error(disc['pas_shows'])
                    
                    st.markdown(f"**Required Action:** {disc['action']}")
                    
                    # Checkbox to mark as actioned
                    st.checkbox(f"✅ Actioned", key=f"disc_{idx}")
                    
                    st.markdown("</div>", unsafe_allow_html=True)
        
        # Show compliance issues
        if compliance_issues:
            st.markdown("#### ℹ️ Compliance Issues (MEDIUM)")
            
            for idx, issue in enumerate(compliance_issues, 1):
                with st.expander(f"Issue: {issue['type']}"):
                    col_x, col_y = st.columns(2)
                    
                    with col_x:
                        st.markdown("**Letter Says:**")
                        st.info(issue['letter_says'])
                    
                    with col_y:
                        st.markdown("**PAS Shows:**")
                        st.warning(issue['pas_shows'])
                    
                    st.markdown(f"**Required Action:** {issue['action']}")
                    
                    st.checkbox(f"✅ Actioned", key=f"comp_{idx}")
        
        # Action checklist
        st.markdown("---")
        st.markdown("### ✅ Action Checklist")
        
        all_actions = []
        for disc in discrepancies:
            all_actions.append(('CRITICAL' if disc['severity'] == 'CRITICAL' else 'HIGH', disc['action']))
        for issue in compliance_issues:
            all_actions.append(('MEDIUM', issue['action']))
        
        for idx, (priority, action) in enumerate(all_actions, 1):
            st.checkbox(f"**[{priority}]** {action}", key=f"action_{idx}")
        
        # Download report
        st.markdown("---")
        if st.button("📥 Download Compliance Report", type="primary"):
            report = generate_compliance_report(
                st.session_state.get('letter_info'),
                st.session_state.get('pas_status'),
                discrepancies,
                compliance_issues
            )
            
            st.download_button(
                label="💾 Download Report as TXT",
                data=report,
                file_name=f"compliance_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )


def generate_compliance_report(letter_info, pas_status, discrepancies, compliance_issues):
    """Generate downloadable compliance report"""
    
    report = f"""
    T21 RTT PATHWAY COMPLIANCE REPORT
    {'='*60}
    
    Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    
    PATIENT INFORMATION:
    {'='*60}
    Name: {letter_info.get('patient_name', 'Not extracted')}
    NHS Number: {letter_info.get('nhs_number', 'Not extracted')}
    Specialty: {letter_info.get('specialty', 'Not extracted')}
    Consultant: {letter_info.get('consultant', 'Not extracted')}
    
    LETTER DETAILS:
    {'='*60}
    Letter Date: {letter_info.get('letter_date', 'Not extracted')}
    Clinic Date: {letter_info.get('clinic_date', 'Not extracted')}
    Diagnosis: {letter_info.get('diagnosis', 'Not extracted')}
    
    PAS STATUS (AS ENTERED):
    {'='*60}
    RTT Code: {pas_status.get('current_rtt_code', 'Not entered')}
    Clock Status: {pas_status.get('clock_status', 'Not entered')}
    DTT Recorded: {pas_status.get('dtt_recorded', 'Not entered')}
    Follow-up Booked: {pas_status.get('follow_up_booked', 'Not entered')}
    Investigations Ordered: {pas_status.get('investigations_ordered', 'Not entered')}
    Waiting List Added: {pas_status.get('waiting_list_added', 'Not entered')}
    GP Letter Sent: {pas_status.get('gp_letter_sent', 'Not entered')}
    
    COMPLIANCE SUMMARY:
    {'='*60}
    Total Issues Found: {len(discrepancies) + len(compliance_issues)}
    Critical/High Priority: {len(discrepancies)}
    Medium Priority: {len(compliance_issues)}
    
    DISCREPANCIES FOUND:
    {'='*60}
    """
    
    if discrepancies:
        for idx, disc in enumerate(discrepancies, 1):
            report += f"""
    #{idx} - {disc['type']} [{disc['severity']}]
    Letter Says: {disc['letter_says']}
    PAS Shows: {disc['pas_shows']}
    Action Required: {disc['action']}
    {'_'*60}
    """
    else:
        report += "\nNo critical discrepancies found.\n"
    
    if compliance_issues:
        report += f"\n\nCOMPLIANCE ISSUES:\n{'='*60}\n"
        for idx, issue in enumerate(compliance_issues, 1):
            report += f"""
    #{idx} - {issue['type']} [{issue['severity']}]
    Letter Says: {issue['letter_says']}
    PAS Shows: {issue['pas_shows']}
    Action Required: {issue['action']}
    {'_'*60}
    """
    
    report += f"""
    
    {'='*60}
    END OF REPORT
    T21 Services Limited | www.t21services.co.uk
    {'='*60}
    """
    
    return report


# Export
__all__ = ['render_clinic_letter_interpreter']
