"""
POLICY & SOP GENERATOR
Generate Trust-specific RTT policies, SOPs, and procedures

🚀 COMPETITIVE ADVANTAGE: Automated policy/SOP generation (Sigma claims this, we deliver it!)
"""

import streamlit as st
from datetime import datetime
from typing import Dict
import os


def render_policy_sop_generator():
    """Main policy/SOP generator interface"""
    
    st.header("📋 Policy & SOP Generator")
    
    st.success("""
    **🚀 COMPETITIVE ADVANTAGE:**
    Generate professional RTT policies and SOPs tailored to your Trust!
    
    ✅ RTT validation policies
    ✅ Standard Operating Procedures
    ✅ Escalation workflows
    ✅ Data quality procedures
    ✅ NHS-compliant templates
    """)
    
    # Tabs for different document types
    tab1, tab2, tab3, tab4 = st.tabs([
        "📋 RTT Policy",
        "📝 SOP Generator",
        "🔄 Workflow Generator",
        "📊 Data Quality Procedure"
    ])
    
    with tab1:
        render_rtt_policy_generator()
    
    with tab2:
        render_sop_generator()
    
    with tab3:
        render_workflow_generator()
    
    with tab4:
        render_data_quality_generator()


def render_rtt_policy_generator():
    """Generate RTT validation policy"""
    
    st.subheader("📋 RTT Validation Policy Generator")
    
    with st.form("rtt_policy_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            trust_name = st.text_input("Trust Name*", placeholder="NHS Foundation Trust")
            policy_version = st.text_input("Policy Version*", value="1.0")
            author_name = st.text_input("Policy Author*", placeholder="Jane Smith, RTT Manager")
        
        with col2:
            effective_date = st.date_input("Effective Date*", value=datetime.now())
            review_date = st.date_input("Review Date*", value=datetime.now().replace(year=datetime.now().year + 1))
            department = st.text_input("Department*", value="Patient Access")
        
        st.markdown("### Policy Scope")
        scope_options = st.multiselect(
            "Select applicable areas:",
            ["Outpatient Services", "Inpatient Admissions", "Day Case Surgery", 
             "Diagnostic Services", "Cancer Services", "Emergency Admissions"],
            default=["Outpatient Services", "Inpatient Admissions"]
        )
        
        st.markdown("### Key Policy Statements")
        clock_start_rules = st.text_area(
            "Clock Start Rules",
            value="All RTT clocks start on the date the referral is received by the Trust, unless the patient is already on an active RTT pathway.",
            height=100
        )
        
        clock_stop_rules = st.text_area(
            "Clock Stop Rules",
            value="RTT clocks stop when the patient receives definitive treatment, declines treatment, or is discharged.",
            height=100
        )
        
        additional_sections = st.text_area(
            "Additional Policy Content (Optional)",
            placeholder="Add any Trust-specific policy requirements...",
            height=150
        )
        
        generate = st.form_submit_button("📄 Generate Policy Document", type="primary")
        
        if generate:
            if not trust_name or not policy_version or not author_name:
                st.error("❌ Please fill all required fields")
            else:
                policy_doc = generate_rtt_policy_document(
                    trust_name=trust_name,
                    policy_version=policy_version,
                    author=author_name,
                    effective_date=effective_date.strftime('%d/%m/%Y'),
                    review_date=review_date.strftime('%d/%m/%Y'),
                    department=department,
                    scope=scope_options,
                    clock_start_rules=clock_start_rules,
                    clock_stop_rules=clock_stop_rules,
                    additional_content=additional_sections
                )
                
                st.success("✅ Policy document generated successfully!")
                st.markdown("---")
                st.markdown("### 📄 Generated Policy Document")
                
                # Display in scrollable text area
                st.text_area("", value=policy_doc, height=400, disabled=True)
                
                # Download button
                st.download_button(
                    label="📥 Download Policy (TXT)",
                    data=policy_doc,
                    file_name=f"RTT_Validation_Policy_v{policy_version}_{datetime.now().strftime('%Y%m%d')}.txt",
                    mime="text/plain"
                )


def generate_rtt_policy_document(
    trust_name: str,
    policy_version: str,
    author: str,
    effective_date: str,
    review_date: str,
    department: str,
    scope: list,
    clock_start_rules: str,
    clock_stop_rules: str,
    additional_content: str
) -> str:
    """Generate the actual policy document"""
    
    policy = f"""
{'='*80}
RTT (REFERRAL TO TREATMENT) VALIDATION POLICY
{trust_name}
{'='*80}

DOCUMENT CONTROL
Policy Reference:    RTT-VAL-{policy_version}
Version:             {policy_version}
Effective Date:      {effective_date}
Review Date:         {review_date}
Department:          {department}
Policy Author:       {author}
Approved By:         [To be completed]
Approval Date:       [To be completed]

{'='*80}

1. PURPOSE

This policy establishes the framework for Referral to Treatment (RTT) pathway 
validation at {trust_name}. It ensures compliance with NHS England RTT 
standards and provides clear guidance for staff involved in RTT data validation.

{'='*80}

2. SCOPE

This policy applies to:
"""
    
    for item in scope:
        policy += f"\n  • {item}"
    
    policy += f"""

{'='*80}

3. DEFINITIONS

RTT Pathway: The time from referral to the start of consultant-led treatment.

18-Week Standard: At least 92% of patients should start treatment within 18 
weeks of referral.

Clock Start: The date when the RTT pathway begins for a patient.

Clock Stop: The date when the RTT pathway ends (treatment, discharge, or DNA).

Validation: The process of checking RTT data for accuracy and compliance.

{'='*80}

4. RTT CLOCK START RULES

{clock_start_rules}

Standard Clock Start Scenarios:
  • Code 01: First GP Referral
  • Code 02: First Consultant-to-Consultant Referral
  • Code 10: Follow-up Appointment

Patient must be informed of their clock start date and 18-week target.

{'='*80}

5. RTT CLOCK STOP RULES

{clock_stop_rules}

Standard Clock Stop Scenarios:
  • Code 30: Treatment - Consultant-led
  • Code 31: Patient Declined Treatment
  • Code 32: Patient DNA'd and Clock Stopped
  • Code 33: Patient DNA'd and Administratively Discharged

All clock stops require appropriate documentation in patient records.

{'='*80}

6. CLOCK PAUSE RULES

RTT clocks may be paused when:
  • Patient requests delay for non-clinical reasons (Code 91)
  • Patient is unavailable for medical reasons (Code 92)
  • Patient is awaiting treatment at another provider (Code 93)

Clock pauses require:
  • Written confirmation from patient
  • Documented rationale
  • Approval from RTT Lead

{'='*80}

7. VALIDATION PROCESS

7.1 Daily Validation
  • Review all new referrals
  • Check clock start dates
  • Verify patient demographics
  • Confirm specialty assignments

7.2 Weekly Validation
  • Review approaching breach dates
  • Check for missing appointments
  • Validate clock pause justifications
  • Audit clock stop accuracy

7.3 Monthly Validation
  • Full PTL (Patient Tracking List) review
  • Data quality audit
  • Exception reporting
  • Performance analysis

{'='*80}

8. DATA QUALITY STANDARDS

All RTT data must meet the following standards:
  • 100% of pathways have valid clock start dates
  • 100% of clock stops have appropriate codes
  • 95% of patient demographics complete
  • Zero duplicate patient records
  • All pauses justified and documented

{'='*80}

9. ESCALATION PROCEDURE

Pathway at Risk of Breach (2 weeks):
  → RTT Coordinator escalates to Booking Team
  → Daily monitoring begins

Pathway at Risk of Breach (1 week):
  → Escalate to RTT Manager
  → Emergency slot sought
  → Senior management notified

Pathway Breached:
  → Incident report filed
  → Root cause analysis initiated
  → Patient informed and apology letter sent
  → Remedial actions documented

{'='*80}

10. ROLES AND RESPONSIBILITIES

RTT Manager:
  • Overall policy compliance
  • Staff training
  • Performance reporting

RTT Coordinators:
  • Daily validation
  • Breach prevention
  • Data quality

Booking Staff:
  • Accurate appointment booking
  • Clock stop recording
  • Patient communication

Clinical Staff:
  • Timely treatment delivery
  • Documentation completion
  • Validation support

{'='*80}

11. TRAINING REQUIREMENTS

All staff involved in RTT processes must complete:
  • RTT Fundamentals training (annual)
  • Data validation training (bi-annual)
  • System-specific training (as needed)
  • Information Governance training (annual)

{'='*80}

12. MONITORING AND AUDIT

Key Performance Indicators:
  • RTT 18-week performance
  • Number of breaches
  • Clock start/stop accuracy
  • Data quality scores
  • Validation completion rates

Monthly reporting to Trust Board via Integrated Performance Report.

{'='*80}

13. ADDITIONAL TRUST-SPECIFIC REQUIREMENTS

{additional_content if additional_content else "None specified."}

{'='*80}

14. POLICY REVIEW

This policy will be reviewed annually or sooner if:
  • National RTT guidance changes
  • Trust processes change
  • Significant performance issues arise
  • System changes require updates

{'='*80}

15. REFERENCES

  • NHS England RTT Rules and Guidance
  • Data Protection Act 2018
  • NHS Constitution
  • Trust Patient Access Policy

{'='*80}

DOCUMENT APPROVAL

Policy Author:         {author}
Signature:            _____________________
Date:                 {effective_date}

Approved By:          [Name, Title]
Signature:            _____________________
Date:                 [Date]

{'='*80}

END OF POLICY DOCUMENT
Generated by T21 Services RTT Platform on {datetime.now().strftime('%d/%m/%Y %H:%M')}
{'='*80}
"""
    
    return policy


def render_sop_generator():
    """Generate Standard Operating Procedure"""
    
    st.subheader("📝 SOP Generator")
    
    st.info("Generate Standard Operating Procedures for RTT processes")
    
    with st.form("sop_form"):
        sop_title = st.text_input("SOP Title*", placeholder="RTT Clock Stop Procedure")
        process_owner = st.text_input("Process Owner*", placeholder="RTT Manager")
        
        sop_type = st.selectbox("SOP Type", [
            "Clock Start Procedure",
            "Clock Stop Procedure",
            "Booking Procedure",
            "Validation Procedure",
            "Escalation Procedure"
        ])
        
        steps = st.text_area(
            "Process Steps (one per line)*",
            placeholder="""1. Receive notification of treatment
2. Verify patient identity
3. Check RTT clock status
4. Record clock stop with appropriate code
5. Update patient record
6. Notify relevant departments""",
            height=200
        )
        
        generate = st.form_submit_button("📝 Generate SOP", type="primary")
        
        if generate:
            if not sop_title or not steps:
                st.error("❌ Please fill required fields")
            else:
                sop_doc = generate_sop_document(sop_title, process_owner, sop_type, steps)
                st.success("✅ SOP generated!")
                st.text_area("", value=sop_doc, height=400, disabled=True)
                st.download_button(
                    "📥 Download SOP",
                    data=sop_doc,
                    file_name=f"SOP_{sop_title.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.txt",
                    mime="text/plain"
                )


def generate_sop_document(title: str, owner: str, sop_type: str, steps: str) -> str:
    """Generate SOP document"""
    
    return f"""
{'='*80}
STANDARD OPERATING PROCEDURE
{title}
{'='*80}

SOP Reference:       SOP-RTT-{datetime.now().strftime('%Y%m')}
Version:             1.0
Effective Date:      {datetime.now().strftime('%d/%m/%Y')}
Process Owner:       {owner}
SOP Type:            {sop_type}

{'='*80}

PURPOSE:
This SOP defines the standard procedure for: {title}

SCOPE:
Applies to all staff involved in RTT pathway management.

{'='*80}

PROCEDURE STEPS:

{steps}

{'='*80}

QUALITY CHECKS:
✓ All steps completed as documented
✓ Accurate data entry
✓ Appropriate approvals obtained
✓ Documentation filed correctly

{'='*80}

Generated by T21 Services RTT Platform
{datetime.now().strftime('%d/%m/%Y %H:%M')}
{'='*80}
"""


def render_workflow_generator():
    """Generate workflow diagram/description"""
    st.subheader("🔄 Workflow Generator")
    st.info("Generate visual workflow descriptions for RTT processes")
    
    with st.form("workflow_form"):
        workflow_name = st.text_input("Workflow Name*", placeholder="RTT Clock Start Workflow")
        workflow_desc = st.text_area("Workflow Description", placeholder="Describe the workflow purpose...")
        
        st.markdown("### Workflow Steps")
        num_steps = st.number_input("Number of Steps", min_value=3, max_value=15, value=5)
        
        steps = []
        for i in range(int(num_steps)):
            step = st.text_input(f"Step {i+1}*", placeholder=f"Enter step {i+1} description", key=f"workflow_step_{i}")
            steps.append(step)
        
        if st.form_submit_button("🔄 Generate Workflow", type="primary"):
            if not workflow_name:
                st.error("❌ Please enter workflow name")
            elif not all(steps):
                st.error("❌ Please fill in all workflow steps")
            else:
                st.success("✅ Workflow Generated!")
                
                workflow_doc = generate_workflow_document(workflow_name, workflow_desc, steps)
                
                st.markdown("### 📄 Generated Workflow")
                st.text_area("Workflow Document", workflow_doc, height=400)
                
                st.download_button(
                    label="💾 Download Workflow",
                    data=workflow_doc,
                    file_name=f"{workflow_name.replace(' ', '_')}_workflow.txt",
                    mime="text/plain"
                )


def render_data_quality_generator():
    """Generate data quality procedure"""
    st.subheader("📊 Data Quality Procedure Generator")
    st.info("Generate data quality checks and procedures for RTT data")
    
    with st.form("dq_form"):
        trust_name = st.text_input("Trust Name*", placeholder="NHS Foundation Trust")
        dq_owner = st.text_input("Data Quality Owner*", placeholder="Information Manager")
        
        st.markdown("### Data Quality Checks")
        check_areas = st.multiselect(
            "Select data quality check areas:",
            ["NHS Number Validation", "Referral Date Accuracy", "Clock Start Validation",
             "Clock Stop Validation", "Specialty Codes", "Patient Demographics",
             "Appointment Recording", "DNA Recording", "Breach Risk Identification"],
            default=["NHS Number Validation", "Clock Start Validation", "Clock Stop Validation"]
        )
        
        frequency = st.selectbox("Check Frequency", ["Daily", "Weekly", "Monthly", "Ad-hoc"])
        
        if st.form_submit_button("📊 Generate Data Quality Procedure", type="primary"):
            if not trust_name or not dq_owner:
                st.error("❌ Please fill all required fields")
            elif not check_areas:
                st.error("❌ Please select at least one check area")
            else:
                st.success("✅ Data Quality Procedure Generated!")
                
                dq_doc = generate_data_quality_document(trust_name, dq_owner, check_areas, frequency)
                
                st.markdown("### 📄 Generated Data Quality Procedure")
                st.text_area("Data Quality Document", dq_doc, height=400)
                
                st.download_button(
                    label="💾 Download Data Quality Procedure",
                    data=dq_doc,
                    file_name=f"{trust_name.replace(' ', '_')}_DQ_Procedure.txt",
                    mime="text/plain"
                )


def generate_workflow_document(name: str, description: str, steps: list) -> str:
    """Generate workflow document"""
    
    workflow_steps = ""
    for i, step in enumerate(steps, 1):
        workflow_steps += f"""
STEP {i}: {step}
{'↓' if i < len(steps) else ''}
"""
    
    return f"""
{'='*80}
                    WORKFLOW DOCUMENT
{'='*80}

Workflow Name:       {name}
Generated Date:      {datetime.now().strftime('%d/%m/%Y')}
Version:             1.0

{'='*80}

WORKFLOW DESCRIPTION:
{description or 'Standard RTT workflow process'}

{'='*80}

WORKFLOW STEPS:
{workflow_steps}

{'='*80}

KEY DECISION POINTS:
• Verify all required information is present
• Check for any blockers or dependencies
• Ensure proper documentation at each step
• Escalate issues according to policy

{'='*80}

QUALITY CHECKS:
✓ All steps completed in sequence
✓ Accurate data entry at each stage
✓ Proper documentation maintained
✓ Escalation procedures followed where needed

{'='*80}

Generated by T21 Services RTT Platform
{datetime.now().strftime('%d/%m/%Y %H:%M')}
{'='*80}
"""


def generate_data_quality_document(trust: str, owner: str, checks: list, frequency: str) -> str:
    """Generate data quality procedure document"""
    
    check_details = ""
    for check in checks:
        check_details += f"""
• {check}
  - Frequency: {frequency}
  - Action on Failure: Review and correct data
  - Escalation: Report to Data Quality Lead
  
"""
    
    return f"""
{'='*80}
            DATA QUALITY PROCEDURE DOCUMENT
{'='*80}

Trust:               {trust}
Data Quality Owner:  {owner}
Generated Date:      {datetime.now().strftime('%d/%m/%Y')}
Version:             1.0

{'='*80}

1. PURPOSE

This procedure defines the data quality checks and processes for RTT data
to ensure accuracy, completeness, and compliance with NHS standards.

{'='*80}

2. SCOPE

Applies to all RTT data entry, validation, and reporting activities.

{'='*80}

3. DATA QUALITY CHECKS

{check_details}

{'='*80}

4. DATA QUALITY STANDARDS

Accuracy:       99% or above
Completeness:   100% required fields populated
Timeliness:     Data entered within 24 hours
Consistency:    No conflicting data entries

{'='*80}

5. MONITORING PROCESS

Frequency:      {frequency}
Method:         Automated reports + manual validation
Reporting:      Monthly Data Quality Report to Trust Board

{'='*80}

6. CORRECTIVE ACTIONS

When data quality issues identified:
1. Log the issue in DQ register
2. Investigate root cause
3. Correct the data
4. Update staff training if needed
5. Review processes to prevent recurrence

{'='*80}

7. RESPONSIBILITIES

Data Quality Owner:   {owner}
  • Overall accountability
  • Monthly reporting
  • Process improvement

Data Entry Staff:
  • Accurate data entry
  • Follow validation rules
  • Report issues

Validation Team:
  • Daily/weekly checks
  • Issue resolution
  • Training support

{'='*80}

8. ESCALATION

Minor Issues:       Report to line manager
Major Issues:       Report to Data Quality Owner within 24 hours
Critical Issues:    Immediate escalation to Director of Operations

{'='*80}

Generated by T21 Services RTT Platform
{datetime.now().strftime('%d/%m/%Y %H:%M')}
{'='*80}
"""
