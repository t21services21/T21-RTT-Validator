"""
T21 RTT Pathway Intelligence Application
NHS Referral To Treatment (RTT) Simulation and Validation System
T21 Services UK
"""

import streamlit as st
import json
from datetime import datetime
from rtt_validator import (validate_pathway, validate_clinic_letter, validate_timeline, 
                          validate_patient_registration, validate_appointments, generate_comment_line)

# Page configuration
st.set_page_config(
    page_title="T21 RTT Pathway Intelligence",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #005EB8;
        font-weight: bold;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #425563;
        text-align: center;
        margin-bottom: 2rem;
    }
    .json-output {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #005EB8;
    }
    .breach-flag {
        padding: 0.5rem;
        border-radius: 0.25rem;
        font-weight: bold;
        text-align: center;
    }
    .breach-none {
        background-color: #d4edda;
        color: #155724;
    }
    .breach-18 {
        background-color: #fff3cd;
        color: #856404;
    }
    .breach-26 {
        background-color: #f8d7da;
        color: #721c24;
    }
    .breach-52 {
        background-color: #721c24;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">🏥 T21 RTT Pathway Intelligence (v1.2)</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">NHS Referral To Treatment Simulation & Validation System | T21 Services UK</div>', unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("🧭 Validation Tools")
tool = st.sidebar.radio(
    "Select Tool:",
    [
        "📊 Pathway Validator",
        "📝 Clinic Letter Interpreter",
        "📅 Timeline Auditor",
        "👤 Patient Registration Validator",
        "📆 Appointment & Booking Checker",
        "💬 Comment Line Generator",
        "ℹ️ About RTT Rules"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("**T21 Services UK**")
st.sidebar.markdown("*Training & Simulation Environment*")
st.sidebar.markdown("No real patient data")


# ============================================
# TOOL 1: PATHWAY VALIDATOR
# ============================================
if tool == "📊 Pathway Validator":
    st.header("RTT Pathway Validator")
    st.markdown("Validate a complete RTT pathway from referral to treatment (0-52 weeks)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📋 Pathway Details")
        specialty = st.text_input("Specialty", value="ENT")
        referral_source = st.selectbox("Referral Source", ["GP", "Consultant", "A&E", "Dentist", "Optician", "Other"])
        referral_date = st.date_input("Referral Received Date", value=datetime(2025, 1, 2))
        first_appt_date = st.date_input("First Appointment Date", value=datetime(2025, 1, 10))
        
        st.subheader("📅 Key Dates")
        diagnostics_date = st.date_input("Diagnostics Date (if any)", value=datetime(2025, 1, 25))
        decision_date = st.date_input("Decision To Treat Date (if any)", value=datetime(2025, 2, 1))
        tci_date = st.date_input("Planned Admission/TCI Date (if any)", value=datetime(2025, 2, 12))
        treatment_date = st.date_input("First Treatment Date (if completed)", value=datetime(2025, 2, 20))
    
    with col2:
        st.subheader("⏸️ Delays & Status")
        delays_pauses = st.text_area("Known Delays/Pauses", 
                                      placeholder="e.g., Patient requested 4-week delay for personal reasons")
        
        active_monitoring = st.selectbox("Active Monitoring", 
                                         ["None", "31_patient", "32_clinician"])
        
        am_start_date = st.date_input("AM Start Date (if applicable)", value=None)
        
        transfer_out = st.selectbox("Transfer Out", ["N", "Y"])
        
        cancellations_dna = st.text_area("Cancellations/DNAs", 
                                         placeholder="e.g., Hospital cancelled 1st appointment")
        
        current_rtt_event = st.selectbox("Current RTT Event Code", 
                                         ["10", "11", "12", "20", "21", "30", "31", "32", "33", "34", "35", "36", "90", "91", "92", "98"])
        
        notes = st.text_area("Additional Notes", placeholder="Any extra context...")
    
    if st.button("🔍 Validate Pathway", type="primary"):
        # Prepare data
        data = {
            'specialty': specialty,
            'referral_source': referral_source,
            'referral_date': referral_date.strftime('%d/%m/%Y'),
            'first_appt_date': first_appt_date.strftime('%d/%m/%Y'),
            'diagnostics_date': diagnostics_date.strftime('%d/%m/%Y') if diagnostics_date else '',
            'decision_date': decision_date.strftime('%d/%m/%Y') if decision_date else '',
            'tci_date': tci_date.strftime('%d/%m/%Y') if tci_date else '',
            'treatment_date': treatment_date.strftime('%d/%m/%Y') if treatment_date else '',
            'delays_pauses': delays_pauses,
            'active_monitoring': active_monitoring,
            'am_start_date': am_start_date.strftime('%d/%m/%Y') if am_start_date else '',
            'transfer_out': transfer_out,
            'cancellations_dna': cancellations_dna,
            'current_rtt_event': current_rtt_event,
            'notes': notes
        }
        
        # Validate
        result = validate_pathway(data)
        
        # Display results
        st.success("✅ Validation Complete")
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Clock Status", result['RTT_Clock_Status'])
        with col2:
            st.metric("Weeks Elapsed", result['Weeks_Elapsed'])
        with col3:
            st.metric("RTT Code", result['RTT_Code'])
        with col4:
            st.metric("Confidence", result['Confidence_Level'])
        
        # Breach flag
        breach_class = "breach-none"
        if "52" in result['Breach_Flag']:
            breach_class = "breach-52"
        elif "26" in result['Breach_Flag']:
            breach_class = "breach-26"
        elif "18" in result['Breach_Flag']:
            breach_class = "breach-18"
        
        st.markdown(f'<div class="breach-flag {breach_class}">🚨 {result["Breach_Flag"]}</div>', 
                   unsafe_allow_html=True)
        
        # Explanation
        st.subheader("📖 Explanation")
        st.info(result['Explanation'])
        
        # Recommended action
        st.subheader("✅ Recommended Action")
        st.success(f"**{result['Recommended_Action']}**")
        
        # PAS Updates
        st.subheader("🔧 What To Change In PAS")
        for update in result['What_To_Change_In_PAS']:
            st.markdown(f"- {update}")
        
        # Comment line
        st.subheader("💬 Standardised Comment Line")
        st.code(result['Standardised_Comment_Line'], language=None)
        
        # Full JSON
        with st.expander("📄 View Full JSON Output"):
            st.json(result)


# ============================================
# TOOL 2: CLINIC LETTER INTERPRETER
# ============================================
elif tool == "📝 Clinic Letter Interpreter":
    st.header("Clinic Letter Interpreter")
    st.markdown("Interpret clinic letters and verify action compliance in PAS")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📨 Clinic Letter / Outcome Text")
        letter_text = st.text_area("Paste clinic letter here:", 
                                    height=300,
                                    placeholder="Example:\n\nENT Review: Patient assessed for deviated septum.\nPlan: Proceed to septoplasty – patient consented.\nPlease book on surgical waiting list (ENT – Septoplasty).\nFollow-up in 6 weeks pre-op clinic to confirm fitness.\nCopy to GP.")
    
    with col2:
        st.subheader("💻 Current PAS Summary")
        st.markdown("**What has already been recorded in PAS:**")
        
        validator_initials = st.text_input("Validator Initials (2-3 letters)", 
                                          value="VLD", 
                                          max_chars=3,
                                          help="Your initials for the comment line (e.g., JDS, AKM)")
        
        # Excel Tracker Fields
        st.markdown("**Excel Tracker Fields:**")
        
        clock_status = st.selectbox("Clock Status (for Excel)", 
                                   ["Previously Stopped", "Hospital to Review", "Unclear", "No", "Yes"],
                                   help="Previously Stopped = Another validator stopped it before | Yes = You're stopping it now")
        
        outcome = st.selectbox("Outcome (for Excel)",
                              ["(Blank)", "Awaiting OPD Appt", "Awaiting results", "Awaiting TC date", 
                               "CL Required", "Discharged", "Further Information Required", "OPD Appt (Booked)"],
                              help="Next action required based on letter")
        
        st.markdown("---")
        st.markdown("**PAS System Checks:**")
        
        followup_booked = st.selectbox("Follow-up appointment booked?", ["N", "Y"])
        followup_date = st.date_input("Follow-up date (if booked)", value=None)
        
        diagnostics_ordered = st.selectbox("Diagnostics ordered?", ["N", "Y"])
        diagnostics_date = st.date_input("Diagnostics date (if ordered)", value=None)
        
        waiting_list = st.selectbox("Added to waiting list?", ["N", "Y"])
        wl_type = st.text_input("Waiting list type", placeholder="e.g., ENT surgical list")
        
        gp_informed = st.selectbox("GP letter sent?", ["N", "Y"])
        
        am_recorded = st.selectbox("Active Monitoring recorded?", ["N", "Y"])
        
        treatment_started = st.selectbox("Treatment started recorded (code 30)?", ["N", "Y"])
        
        other_notes = st.text_area("Other notes", placeholder="Any additional PAS entries...")
    
    if st.button("🔍 Interpret Letter", type="primary"):
        pas_summary = {
            'validator_initials': validator_initials.upper(),
            'clock_status': clock_status,
            'outcome': outcome,
            'followup_booked': followup_booked,
            'followup_date': followup_date.strftime('%d/%m/%Y') if followup_date else '',
            'diagnostics_ordered': diagnostics_ordered,
            'diagnostics_date': diagnostics_date.strftime('%d/%m/%Y') if diagnostics_date else '',
            'waiting_list': waiting_list,
            'wl_type': wl_type,
            'gp_informed': gp_informed,
            'am_recorded': am_recorded,
            'treatment_started': treatment_started,
            'other_notes': other_notes
        }
        
        result = validate_clinic_letter(letter_text, pas_summary)
        
        # VALIDATION STATUS BANNER
        val_summary = result['Validation_Summary']
        if val_summary['Excel_Flag_Color'] == "GREEN":
            st.success(f"✅ {val_summary['Overall_Status']}")
        elif val_summary['Excel_Flag_Color'] == "AMBER":
            st.warning(f"⚠️ {val_summary['Overall_Status']}")
        else:
            st.error(f"❌ {val_summary['Overall_Status']}")
        
        # VALIDATION METRICS (for Excel reporting)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("RTT Code", result['RTT_Code'])
        with col2:
            st.metric("Clock Status", result['Clock_Status'])
        with col3:
            st.metric("Compliance Rate", val_summary['Compliance_Rate'])
        with col4:
            flag_color = val_summary['Excel_Flag_Color']
            st.metric("Excel Flag", flag_color, delta_color="off")
        
        # EXCEL REPORTING SECTION (Matches Excel Tracker Columns)
        st.subheader("📊 Excel Tracker Report")
        excel_data = result['Excel_Report']
        
        excel_output = f"""
**Copy to Excel Tracker (Exact Column Order):**

Validator Name: {excel_data['Validator_Name']}
Clock Status: {excel_data['Clock_Status']}
Outcome: {excel_data['Outcome']}
Validation Date: {excel_data['Validation_Date']}
Validation Comments: {excel_data['Validation_Comments']}
        """
        st.code(excel_output.strip(), language=None)
        
        # Show comment in highlighted box
        st.info(f"**Validation Comment for Excel:**\n\n{excel_data['Validation_Comments']}")
        
        # VALIDATION CHECKLIST
        st.subheader("✅ Validation Checklist")
        compliance = result['Action_Compliance']
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**📋 Actions Required (from letter):**")
            for action in compliance['Actions_Required']:
                st.markdown(f"- {action}")
        
        with col2:
            st.markdown("**✅ Actions Completed (verified in PAS):**")
            if compliance['Actions_Reported_In_PAS']:
                for action in compliance['Actions_Reported_In_PAS']:
                    st.markdown(f"- ✅ {action}")
            else:
                st.markdown("*No actions completed in PAS*")
        
        # GAPS & FLAGS
        if compliance['Gaps']:
            st.error(f"**🚩 GAPS FOUND - {compliance['Priority']} Priority ({val_summary['Actions_Outstanding']} outstanding)**")
            for i, gap in enumerate(compliance['Gaps'], 1):
                st.markdown(f"{i}. ❌ **{gap}**")
        else:
            st.success("✅ **No gaps found - All actions completed!**")
        
        # COMMENT LINE (for PAS system)
        st.subheader("💬 Standardised Comment Line (Copy to PAS)")
        st.code(result['Standardised_Comment_Line'], language=None)
        
        # Explanation
        with st.expander("📖 Code Explanation"):
            st.info(result['Explanation'])
        
        # Full JSON
        with st.expander("📄 Full JSON Output (for technical review)"):
            st.json(result)


# ============================================
# TOOL 3: TIMELINE AUDITOR
# ============================================
elif tool == "📅 Timeline Auditor":
    st.header("RTT Timeline Auditor")
    st.markdown("Audit a chronological sequence of RTT events for coding accuracy")
    
    st.subheader("📋 Enter Pathway Timeline")
    st.markdown("Add events in chronological order:")
    
    # Initialize session state for events
    if 'events' not in st.session_state:
        st.session_state.events = [
            {'date': '01/02/2025', 'description': 'Referral received', 'code': '10', 'notes': 'GP to ENT'}
        ]
    
    # Display existing events
    for i, event in enumerate(st.session_state.events):
        col1, col2, col3, col4, col5 = st.columns([2, 3, 1, 3, 1])
        with col1:
            event['date'] = st.text_input(f"Date {i+1}", value=event['date'], key=f"date_{i}")
        with col2:
            event['description'] = st.text_input(f"Description {i+1}", value=event['description'], key=f"desc_{i}")
        with col3:
            event['code'] = st.selectbox(f"Code {i+1}", 
                                        ["10", "11", "12", "20", "21", "30", "31", "32", "33", "34", "35", "36", "90", "91", "92", "98"],
                                        index=["10", "11", "12", "20", "21", "30", "31", "32", "33", "34", "35", "36", "90", "91", "92", "98"].index(event['code']),
                                        key=f"code_{i}")
        with col4:
            event['notes'] = st.text_input(f"Notes {i+1}", value=event.get('notes', ''), key=f"notes_{i}")
        with col5:
            if st.button("🗑️", key=f"del_{i}"):
                st.session_state.events.pop(i)
                st.rerun()
    
    # Add new event
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("➕ Add Event"):
            st.session_state.events.append({
                'date': datetime.now().strftime('%d/%m/%Y'),
                'description': 'New event',
                'code': '20',
                'notes': ''
            })
            st.rerun()
    
    with col2:
        if st.button("🔄 Reset Timeline"):
            st.session_state.events = [
                {'date': '01/02/2025', 'description': 'Referral received', 'code': '10', 'notes': 'GP to ENT'}
            ]
            st.rerun()
    
    st.markdown("---")
    
    if st.button("🔍 Audit Timeline", type="primary"):
        result = validate_timeline(st.session_state.events)
        
        # Overall status
        status_color = "success" if result['Overall_Status'] == "Pass" else ("warning" if result['Overall_Status'] == "Warning" else "error")
        st.markdown(f"### {result['Overall_Status']}")
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Clock Start", result['Clock_Start_Date'])
        with col2:
            st.metric("Clock Stop", result['Clock_Stop_Date'] or "Active")
        with col3:
            st.metric("Total Weeks", result['Weeks_Total'])
        with col4:
            st.metric("Breach Flag", result['Breach_Flag'])
        
        # Issues
        if result['Critical_Issues']:
            st.error("**🚨 Critical Issues:**")
            for issue in result['Critical_Issues']:
                st.markdown(f"- {issue}")
        
        if result['Moderate_Issues']:
            st.warning("**⚠️ Moderate Issues:**")
            for issue in result['Moderate_Issues']:
                st.markdown(f"- {issue}")
        
        if result['Duplicate_Code_Issues']:
            st.error("**🔄 Duplicate Code Issues:**")
            for issue in result['Duplicate_Code_Issues']:
                st.markdown(f"- {issue}")
        
        # Recode suggestions
        if result['Recommended_Recode_Suggestions']:
            st.subheader("🔧 Recode Suggestions")
            for suggestion in result['Recommended_Recode_Suggestions']:
                st.markdown(f"- {suggestion}")
        
        # Training feedback
        st.subheader("🎓 Training Feedback")
        st.info(result['Training_Feedback'])
        
        # Comment line
        st.subheader("💬 Standardised Comment Line")
        st.code(result['Standardised_Comment_Line'], language=None)
        
        # Full JSON
        with st.expander("📄 View Full JSON Output"):
            st.json(result)


# ============================================
# TOOL 4: PATIENT REGISTRATION VALIDATOR
# ============================================
elif tool == "👤 Patient Registration Validator":
    st.header("Patient Registration Validator")
    st.markdown("Validate patient registration details and document readiness before starting RTT pathway")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("👤 Patient Demographics")
        patient_name = st.text_input("Patient Name *", placeholder="SURNAME, Forename")
        nhs_number = st.text_input("NHS Number *", placeholder="1234567890 (10 digits)")
        district_number = st.text_input("District Number", placeholder="Hospital number")
        dob = st.date_input("Date of Birth *", value=None)
        age = st.number_input("Age (optional)", min_value=0, max_value=120, value=0)
        
    with col2:
        st.subheader("📋 Referral Details")
        referral_source = st.selectbox("Referral Source *", ["", "GP", "Consultant", "A&E", "Dentist", "Optician", "Other"])
        referral_date = st.date_input("Referral Date *", value=None)
        specialty = st.text_input("Specialty *", placeholder="e.g., ENT, Orthopaedics")
        referral_type = st.text_input("Referral Type", placeholder="e.g., Consultant-led, Diagnostic-only")
        
    st.subheader("📎 Documents Uploaded")
    documents = st.text_area("Document Names (comma-separated)", 
                            placeholder="SMITH_JOHN_020125_REFERRAL.pdf, SMITH_JOHN_020125_XRAY.dcm")
    
    col1, col2 = st.columns(2)
    with col1:
        referral_accepted = st.selectbox("Referral Accepted?", ["N", "Y"])
        check_duplicate = st.selectbox("Check for Duplicates?", ["N", "Y"])
    
    with col2:
        notes = st.text_area("Additional Notes", placeholder="Any special considerations...")
    
    if st.button("✅ Validate Registration", type="primary"):
        data = {
            'patient_name': patient_name,
            'nhs_number': nhs_number,
            'district_number': district_number,
            'dob': dob.strftime('%d/%m/%Y') if dob else '',
            'age': str(age) if age > 0 else '',
            'referral_source': referral_source,
            'referral_date': referral_date.strftime('%d/%m/%Y') if referral_date else '',
            'specialty': specialty,
            'referral_type': referral_type,
            'documents': documents,
            'referral_accepted': referral_accepted,
            'check_duplicate': check_duplicate,
            'notes': notes
        }
        
        result = validate_patient_registration(data)
        
        # Display result
        if result['Validation_Result'] == "Pass":
            st.success("✅ Registration Validated - PASS")
        elif result['Validation_Result'] == "Warning":
            st.warning("⚠️ Registration Validated - WARNING")
        else:
            st.error("❌ Registration Validated - FAIL")
        
        # Data issues
        if result['Data_Issues']:
            st.subheader("⚠️ Data Issues Found")
            for issue in result['Data_Issues']:
                st.markdown(f"- ❌ {issue}")
        else:
            st.success("✅ No data issues found!")
        
        # PAS updates
        st.subheader("🔧 PAS Updates Required")
        for update in result['PAS_Update']:
            st.markdown(f"- {update}")
        
        # Training feedback
        st.subheader("🎓 Training Feedback")
        st.info(result['Training_Feedback'])
        
        # Comment line
        st.subheader("💬 Standardised Comment Line")
        st.code(result['Standardised_Comment_Line'], language=None)
        
        # Full JSON
        with st.expander("📄 View Full JSON Output"):
            st.json(result)


# ============================================
# TOOL 5: APPOINTMENT & BOOKING CHECKER
# ============================================
elif tool == "📆 Appointment & Booking Checker":
    st.header("Appointment & Booking Checker")
    st.markdown("Review booking history and verify correct RTT impact")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📅 Appointment History")
        referral_date = st.date_input("Referral Date", value=datetime(2025, 1, 2))
        first_appt_date = st.date_input("First Appointment Date", value=datetime(2025, 1, 12))
        first_appt_type = st.text_input("First Appointment Type", value="New OP", placeholder="e.g., New OP, Diagnostic")
        
        followup_appointments = st.text_area("Follow-up Appointments", 
                                            placeholder="e.g., 01/02/2025 - Review OP, 15/02/2025 - Pre-op")
    
    with col2:
        st.subheader("⚠️ Issues & Status")
        dnas_cancellations = st.text_area("DNAs / Cancellations", 
                                         placeholder="e.g., Patient cancelled 1st appt - personal reasons\nHospital cancelled 2nd appt - staff shortage")
        
        planned_surgery = st.text_area("Planned Surgery / WL Details", 
                                      placeholder="e.g., Listed for septoplasty, TCI 20/02/2025")
        
        am_status = st.selectbox("Active Monitoring Status", 
                                ["None", "31 (patient-initiated)", "32 (clinician-initiated)", "91 (during AM)"])
        am_start_date = st.date_input("AM Start Date (if applicable)", value=None)
    
    treatment_started = st.selectbox("Treatment Started?", ["N", "Y"])
    notes = st.text_area("Additional Notes", placeholder="e.g., Review in 6 weeks instructed")
    
    if st.button("🔍 Check Appointments", type="primary"):
        data = {
            'referral_date': referral_date.strftime('%d/%m/%Y'),
            'first_appt_date': first_appt_date.strftime('%d/%m/%Y'),
            'first_appt_type': first_appt_type,
            'followup_appointments': followup_appointments,
            'dnas_cancellations': dnas_cancellations,
            'planned_surgery': planned_surgery,
            'am_status': am_status.split()[0] if am_status != "None" else "",
            'am_start_date': am_start_date.strftime('%d/%m/%Y') if am_start_date else '',
            'treatment_started': treatment_started,
            'notes': notes
        }
        
        result = validate_appointments(data)
        
        st.success("✅ Appointment Check Complete")
        
        # RTT Impact
        st.subheader("📊 RTT Impact")
        st.metric("RTT Impact", result['RTT_Impact'])
        
        # Issues
        if result['Issues'] != ["No issues found"]:
            st.subheader("⚠️ Issues Detected")
            for issue in result['Issues']:
                st.markdown(f"- ⚠️ {issue}")
        else:
            st.success("✅ No issues found!")
        
        # PAS updates
        st.subheader("🔧 PAS Updates Required")
        for update in result['PAS_Update']:
            st.markdown(f"- {update}")
        
        # Training feedback
        st.subheader("🎓 Training Feedback")
        st.info(result['Training_Feedback'])
        
        # Comment line
        st.subheader("💬 Standardised Comment Line")
        st.code(result['Standardised_Comment_Line'], language=None)
        
        # Full JSON
        with st.expander("📄 View Full JSON Output"):
            st.json(result)


# ============================================
# TOOL 6: COMMENT LINE GENERATOR
# ============================================
elif tool == "💬 Comment Line Generator":
    st.header("Comment Line Generator")
    st.markdown("Generate standardised T21 PAS comment lines for any RTT event")
    
    st.info("📋 Fill in the event details below to generate a professional PAS comment line")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📅 Event Details")
        event = st.selectbox("Event Type", [
            "First Treatment / FDT",
            "Active Monitoring Start",
            "DNA First Care",
            "Waiting List / TCI",
            "Discharge",
            "Decision to Treat",
            "Other / Custom"
        ])
        
        key_date = st.date_input("Key Date", value=datetime.now())
        
        rtt_code = st.selectbox("RTT Code (if known)", 
                               ["", "10", "11", "12", "20", "21", "30", "31", "32", "33", "34", "35", "36", "90", "91", "92", "98"])
    
    with col2:
        st.subheader("📝 Additional Information")
        procedure = st.text_input("Procedure / Outcome", 
                                 placeholder="e.g., Septoplasty, Hip Replacement")
        
        next_action = st.text_input("Follow-up / Next Action", 
                                   placeholder="e.g., FU booked 01/03/2025, Review in 12 weeks")
        
        gp_letter = st.selectbox("GP Letter Sent?", ["N", "Y"])
    
    st.markdown("---")
    
    if st.button("✨ Generate Comment Line", type="primary"):
        data = {
            'event': event,
            'key_date': key_date.strftime('%d/%m/%Y'),
            'rtt_code': rtt_code,
            'procedure': procedure,
            'next_action': next_action,
            'gp_letter': gp_letter
        }
        
        result = generate_comment_line(data)
        
        st.success("✅ Comment Line Generated")
        
        st.subheader("💬 Your Standardised Comment Line")
        st.code(result['Standardised_Comment_Line'], language=None)
        
        st.markdown("**Copy and paste this into PAS notes field**")
        
        # Examples
        with st.expander("📚 View Comment Line Examples"):
            st.markdown("""
            ### Example Comment Lines:
            
            **First Definitive Treatment:**
            ```
            CS20/02/2025/30 – FDT STARTED (SEPTOPLASTY). PATHWAY CLOSED. GP LETTER SENT.
            ```
            
            **Active Monitoring:**
            ```
            AM32/10/01/2025 – UNDER REVIEW 12W. FU BOOKED 10/04/2025.
            ```
            
            **DNA First Care:**
            ```
            DNA33/15/01/2025 – FIRST CARE DNA. REBOOK 2W. GP COPY PENDING.
            ```
            
            **Waiting List / TCI:**
            ```
            WL/TCI 20/02/2025 – TCI SET. CONTINUE 20.
            ```
            
            **Discharge:**
            ```
            DISCH15/01/2025/34 – NO TREATMENT REQUIRED. PATHWAY CLOSED. GP LETTER SENT.
            ```
            
            **Decision to Treat:**
            ```
            DTT01/02/2025/20 – LISTED FOR SEPTOPLASTY. WL ENTRY REQUIRED.
            ```
            """)


# ============================================
# TOOL 7: ABOUT RTT RULES
# ============================================
elif tool == "ℹ️ About RTT Rules":
    st.header("NHS RTT Rules Summary")
    
    st.markdown("""
    ## 🕒 RTT Clock Fundamentals
    
    - The RTT clock **starts** when a referral for consultant-led care is received
    - It also starts when a **decision to treat** is made without a referral
    - The clock **continues** through all stages until formally stopped
    - The standard NHS target is **18 weeks**
    
    ## ⏸️ Clock Pauses
    
    - **Patient-initiated delays (PIDs)** can pause a clock
    - **Provider-initiated cancellations** do NOT pause the clock
    - Clock pauses are temporary and resume when patient is available
    
    ## 🛑 Clock Stops
    
    The RTT clock **stops** when:
    1. First definitive treatment starts (surgery, active medication, therapeutic procedure)
    2. Clinical decision made that treatment is not required
    3. Patient declines or fails to respond to reasonable offer
    4. Patient transferred to another provider
    5. Patient dies or DNA after reasonable offer
    
    ## 🧾 RTT Event Codes
    
    | Code | Description | Impact |
    |------|-------------|--------|
    | **10** | First activity in pathway | Clock start |
    | **11** | First activity after Active Monitoring/Watchful Wait ends | Clock restart |
    | **12** | First activity following Consultant/AHP referral for NEW condition | Clock start |
    | **20** | Subsequent activity | Clock continues |
    | **21** | Tertiary referral | Transfer responsibility |
    | **30** | First definitive treatment | Clock stop |
    | **31** | Active monitoring (patient-initiated) | Clock pause |
    | **32** | Active monitoring (provider-initiated) | Clock pause |
    | **33** | DNA – first care activity | Special handling |
    | **34** | Decision not to treat | Clock stop |
    | **35** | Patient declined treatment | Clock stop |
    | **36** | Patient died | Clock stop |
    | **90** | FDT occurred previously | Post-treatment (non-RTT) |
    | **91** | Activity during active monitoring | During AM only |
    | **92** | Diagnostics only | Non-RTT |
    | **98** | Not applicable to RTT | Non-RTT |
    
    ## ⏱️ Breach Thresholds
    
    - **18 weeks**: Standard RTT target
    - **26 weeks**: Serious wait breach
    - **52 weeks**: Critical breach (requires escalation)
    
    ## 📚 Policy Reference
    
    **NHS England RTT Rules and Guidance v17.0**
    
    ---
    
    ### 🎓 Training Environment
    
    This is a **simulation and training tool** for T21 Services UK.  
    **No real patient data should be entered.**
    
    Use this tool to:
    - Practice RTT pathway validation
    - Learn correct coding sequences
    - Understand breach thresholds
    - Improve data quality
    
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    <strong>T21 RTT Pathway Intelligence v1.2</strong><br>
    T21 Services UK | NHS Training & Simulation Environment<br>
    <em>No real patient data | For training purposes only</em>
</div>
""", unsafe_allow_html=True)
