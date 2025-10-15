"""
T21 PROFESSIONAL CLINIC LETTER INTERPRETER
For NHS Staff, Graduates, and Healthcare Professionals

Features:
- Upload PDF, DOCX, TXT files or paste text
- Extract patient information automatically
- Validate against PAS system
- Generate compliance reports
- Export results to Excel
- RTT code suggestions
- Action tracking
- Professional reporting
"""

import streamlit as st
import json
from datetime import datetime
import io
import base64

def extract_text_from_file(uploaded_file):
    """Extract text from uploaded file (PDF, DOCX, TXT)"""
    
    file_type = uploaded_file.name.split('.')[-1].lower()
    
    try:
        if file_type == 'txt':
            # Simple text file
            text = uploaded_file.read().decode('utf-8')
            return True, text
        
        elif file_type == 'pdf':
            # PDF extraction
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
            # Word document extraction
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


def analyze_letter_content(letter_text):
    """
    Analyze letter content and extract key information
    """
    
    letter_lower = letter_text.lower()
    
    analysis = {
        'patient_info_found': False,
        'clinical_findings': False,
        'treatment_plan': False,
        'follow_up_required': False,
        'urgent_indicators': False,
        'rtt_implications': [],
        'action_items': [],
        'validation_warnings': []
    }
    
    # Check for patient information
    if any(keyword in letter_lower for keyword in ['patient', 'nhs', 'dob', 'date of birth']):
        analysis['patient_info_found'] = True
    
    # Check for clinical findings
    if any(keyword in letter_lower for keyword in ['diagnosis', 'assessment', 'examination', 'findings']):
        analysis['clinical_findings'] = True
    
    # Check for treatment plan
    if any(keyword in letter_lower for keyword in ['plan', 'treatment', 'procedure', 'surgery', 'intervention']):
        analysis['treatment_plan'] = True
    
    # Check for follow-up
    if any(keyword in letter_lower for keyword in ['follow', 'review', 'appointment', 'see again']):
        analysis['follow_up_required'] = True
        analysis['action_items'].append("Schedule follow-up appointment")
    
    # Check for urgent indicators
    urgent_keywords = ['urgent', 'emergency', '2ww', 'two week', 'cancer', 'suspected cancer', 'immediate']
    if any(keyword in letter_lower for keyword in urgent_keywords):
        analysis['urgent_indicators'] = True
        analysis['validation_warnings'].append("⚠️ URGENT CASE - Priority handling required")
    
    # RTT implications
    if 'discharge' in letter_lower:
        analysis['rtt_implications'].append("RTT clock may stop (Code 33 - Discharged)")
        analysis['action_items'].append("Update RTT status to Code 33")
    
    if any(word in letter_lower for word in ['surgery', 'operation', 'theatre', 'procedure']):
        analysis['rtt_implications'].append("Treatment likely started (Code 30)")
        analysis['action_items'].append("Check if waiting list entry required")
    
    if 'decision to treat' in letter_lower or 'dtt' in letter_lower:
        analysis['rtt_implications'].append("Decision To Treat recorded (Code 10)")
        analysis['action_items'].append("Verify DTT date in PAS")
    
    if any(word in letter_lower for word in ['active monitoring', 'watchful waiting', 'surveillance']):
        analysis['rtt_implications'].append("Active Monitoring pathway (Code 11)")
        analysis['action_items'].append("Confirm Active Monitoring recorded in PAS")
    
    # Check for diagnostic tests
    if any(word in letter_lower for word in ['mri', 'ct', 'scan', 'x-ray', 'ultrasound', 'blood test', 'biopsy']):
        analysis['action_items'].append("Verify diagnostic tests ordered in PAS")
    
    # Check for GP notification
    if any(phrase in letter_lower for phrase in ['gp', 'general practitioner', 'copy to gp']):
        analysis['action_items'].append("Confirm GP letter sent")
    
    return analysis


def render_clinic_letter_interpreter():
    """Main UI for Professional Clinic Letter Interpreter"""
    
    st.title("📝 Professional Clinic Letter Interpreter")
    st.markdown("""
    **For NHS Staff, Graduates & Healthcare Professionals**
    
    ✅ Upload PDF, DOCX, or TXT files  
    ✅ Or paste letter text directly  
    ✅ Automatic information extraction  
    ✅ RTT code validation  
    ✅ PAS compliance checking  
    ✅ Professional reporting  
    """)
    
    st.markdown("---")
    
    # Input method selection
    st.subheader("📄 Step 1: Provide Clinical Letter")
    
    input_method = st.radio(
        "Choose input method:",
        ["📎 Upload File (PDF/DOCX/TXT)", "📝 Paste Text"],
        horizontal=True
    )
    
    letter_text = None
    
    if input_method == "📎 Upload File (PDF/DOCX/TXT)":
        uploaded_file = st.file_uploader(
            "Upload clinical letter",
            type=['pdf', 'docx', 'doc', 'txt'],
            help="Supported formats: PDF, Word (DOCX/DOC), Text (TXT)"
        )
        
        if uploaded_file:
            with st.spinner("📄 Extracting text from file..."):
                success, result = extract_text_from_file(uploaded_file)
                
                if success:
                    letter_text = result
                    st.success(f"✅ File uploaded: {uploaded_file.name}")
                    st.success(f"✅ Text extracted successfully! ({len(letter_text)} characters)")
                    
                    # Show preview
                    with st.expander("📄 Preview extracted text"):
                        st.text_area("Extracted text", letter_text, height=200, disabled=True)
                else:
                    st.error(f"❌ {result}")
    
    else:  # Paste text
        letter_text = st.text_area(
            "Paste clinical letter here:",
            height=300,
            placeholder="""Example:

ENT Review - Ms Smith, NHS: 123 456 7890

Assessment: Patient reviewed for chronic rhinosinusitis. 
Symptoms persistent despite medical management.

Plan: Patient agrees to proceed with functional endoscopic sinus surgery (FESS).
Consented for procedure. Please add to surgical waiting list.

Follow-up: Post-op review in 6 weeks.

Copy to GP.
Dr. Jones, Consultant ENT Surgeon
15/10/2025"""
        )
    
    if letter_text and letter_text.strip():
        
        st.markdown("---")
        st.subheader("💻 Step 2: PAS System Verification")
        
        st.markdown("**Verify current PAS entries:**")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**RTT Information:**")
            current_rtt_code = st.selectbox(
                "Current RTT Code",
                ["Not Set", "10", "11", "12", "20", "21", "30", "31", "32", "33", "34", "35", "36", "90", "91", "92", "98"]
            )
            clock_status = st.selectbox(
                "Clock Status",
                ["Running", "Stopped", "Paused", "Not Started"]
            )
        
        with col2:
            st.markdown("**Appointments:**")
            followup_booked = st.selectbox("Follow-up booked?", ["No", "Yes"])
            diagnostics_ordered = st.selectbox("Diagnostics ordered?", ["No", "Yes"])
            waiting_list_added = st.selectbox("On waiting list?", ["No", "Yes"])
        
        with col3:
            st.markdown("**Communication:**")
            gp_notified = st.selectbox("GP notified?", ["No", "Yes"])
            patient_informed = st.selectbox("Patient informed?", ["No", "Yes"])
            notes_updated = st.selectbox("Clinical notes updated?", ["No", "Yes"])
        
        st.markdown("**Additional Information:**")
        validator_name = st.text_input("Your name/initials", placeholder="e.g., JDS, A.Smith")
        additional_notes = st.text_area("Additional notes", placeholder="Any other relevant information...")
        
        st.markdown("---")
        
        # ANALYZE BUTTON
        if st.button("🔍 Analyze & Interpret Letter", type="primary", use_container_width=True):
            
            with st.spinner("🔍 Analyzing clinical letter..."):
                
                # Analyze letter content
                analysis = analyze_letter_content(letter_text)
                
                st.success("✅ Analysis Complete!")
                
                # URGENT WARNING
                if analysis['urgent_indicators']:
                    st.error("🚨 **URGENT CASE DETECTED** - Priority handling required!")
                
                st.markdown("---")
                
                # ANALYSIS RESULTS
                st.subheader("📊 Letter Analysis Results")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    status = "✅" if analysis['patient_info_found'] else "❌"
                    st.metric("Patient Info", status)
                
                with col2:
                    status = "✅" if analysis['clinical_findings'] else "❌"
                    st.metric("Clinical Findings", status)
                
                with col3:
                    status = "✅" if analysis['treatment_plan'] else "❌"
                    st.metric("Treatment Plan", status)
                
                with col4:
                    status = "✅" if analysis['follow_up_required'] else "❌"
                    st.metric("Follow-up", status)
                
                st.markdown("---")
                
                # RTT IMPLICATIONS
                if analysis['rtt_implications']:
                    st.subheader("⏰ RTT Pathway Implications")
                    for implication in analysis['rtt_implications']:
                        st.info(f"📌 {implication}")
                
                # ACTION ITEMS
                if analysis['action_items']:
                    st.subheader("✅ Required Actions")
                    for i, action in enumerate(analysis['action_items'], 1):
                        st.checkbox(f"{i}. {action}", key=f"action_{i}")
                
                # VALIDATION WARNINGS
                if analysis['validation_warnings']:
                    st.subheader("⚠️ Validation Warnings")
                    for warning in analysis['validation_warnings']:
                        st.warning(warning)
                
                st.markdown("---")
                
                # COMPLIANCE CHECK
                st.subheader("🎯 PAS Compliance Check")
                
                compliance_issues = []
                
                if analysis['follow_up_required'] and followup_booked == "No":
                    compliance_issues.append("❌ Follow-up required but not booked in PAS")
                
                if 'diagnostic' in analysis['action_items'] and diagnostics_ordered == "No":
                    compliance_issues.append("❌ Diagnostics mentioned but not ordered in PAS")
                
                if 'waiting list' in ' '.join(analysis['action_items']).lower() and waiting_list_added == "No":
                    compliance_issues.append("❌ Waiting list entry required but not added")
                
                if 'gp' in ' '.join(analysis['action_items']).lower() and gp_notified == "No":
                    compliance_issues.append("❌ GP notification required but not sent")
                
                if compliance_issues:
                    st.error("**PAS Compliance Issues Found:**")
                    for issue in compliance_issues:
                        st.write(issue)
                    
                    compliance_rate = max(0, 100 - (len(compliance_issues) * 25))
                    st.metric("Compliance Rate", f"{compliance_rate}%")
                else:
                    st.success("✅ **No compliance issues found** - PAS entries match clinical letter")
                    st.metric("Compliance Rate", "100%")
                
                st.markdown("---")
                
                # REPORT GENERATION
                st.subheader("📄 Professional Report")
                
                report = f"""
# CLINIC LETTER INTERPRETATION REPORT

**Date:** {datetime.now().strftime('%d/%m/%Y %H:%M')}
**Validated by:** {validator_name if validator_name else 'Not specified'}

## LETTER ANALYSIS

- Patient Information: {'✅ Found' if analysis['patient_info_found'] else '❌ Missing'}
- Clinical Findings: {'✅ Documented' if analysis['clinical_findings'] else '❌ Not found'}
- Treatment Plan: {'✅ Present' if analysis['treatment_plan'] else '❌ Absent'}
- Follow-up Required: {'✅ Yes' if analysis['follow_up_required'] else '❌ No'}
- Urgent Indicators: {'🚨 YES - URGENT' if analysis['urgent_indicators'] else '✅ No'}

## RTT IMPLICATIONS

{chr(10).join(['- ' + imp for imp in analysis['rtt_implications']]) if analysis['rtt_implications'] else '- No specific RTT implications identified'}

## REQUIRED ACTIONS

{chr(10).join(['- ' + action for action in analysis['action_items']]) if analysis['action_items'] else '- No specific actions required'}

## PAS VERIFICATION

- Current RTT Code: {current_rtt_code}
- Clock Status: {clock_status}
- Follow-up Booked: {followup_booked}
- Diagnostics Ordered: {diagnostics_ordered}
- Waiting List Added: {waiting_list_added}
- GP Notified: {gp_notified}
- Patient Informed: {patient_informed}
- Clinical Notes Updated: {notes_updated}

## COMPLIANCE STATUS

{chr(10).join(['- ' + issue for issue in compliance_issues]) if compliance_issues else '✅ All PAS entries comply with clinical letter'}

## ADDITIONAL NOTES

{additional_notes if additional_notes else 'None'}

---

*Report generated by T21 Professional Clinic Letter Interpreter*
*T21 Services Limited | Company No: 13091053*
"""
                
                st.text_area("Report (copy this)", report, height=400)
                
                # Download button
                st.download_button(
                    label="📥 Download Report (TXT)",
                    data=report,
                    file_name=f"clinic_letter_report_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                    mime="text/plain"
                )
    
    else:
        st.info("👆 Please upload a file or paste clinical letter text to begin analysis")


if __name__ == "__main__":
    render_clinic_letter_interpreter()
