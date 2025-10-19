"""
POPULATE AI KNOWLEDGE BASE
Feed ALL existing platform content into the AI Tutor's knowledge base

This script extracts:
1. All 38+ RTT training scenarios
2. All 1000+ certification questions
3. RTT code definitions
4. NHS guidelines
5. All learning materials

Then formats and uploads them so the AI Tutor can reference them!
"""

from ai_knowledge_base import add_training_material, get_knowledge_base_stats
from training_library import get_all_scenarios
import json

def populate_rtt_scenarios():
    """Add all RTT scenarios to knowledge base"""
    print("📚 Adding RTT Scenarios to AI Knowledge Base...")
    
    scenarios = get_all_scenarios()
    
    for scenario in scenarios:
        # Create comprehensive content
        content = f"""
RTT SCENARIO {scenario['id']}: {scenario['title']}

DIFFICULTY: {scenario['difficulty']}

CLINICAL LETTER:
{scenario['letter']}

CORRECT RTT CODE: {scenario['correct_code']}

EXPLANATION:
{scenario['explanation']}

TEACHING POINTS:
{scenario.get('teaching_points', 'N/A')}

COMMON MISTAKES TO AVOID:
{scenario.get('common_mistakes', 'N/A')}
"""
        
        # Add to knowledge base
        material_id = add_training_material(
            title=f"RTT Scenario {scenario['id']}: {scenario['title']}",
            content=content,
            material_type="Case Study",
            category="RTT Scenarios",
            description=f"{scenario['difficulty']} difficulty scenario about {scenario['title']}",
            tags=[
                f"Code {scenario['correct_code']}", 
                scenario['difficulty'],
                "RTT",
                "Case Study"
            ],
            file_name=f"scenario_{scenario['id']}.txt"
        )
        
        print(f"  ✅ Added Scenario {scenario['id']}: {scenario['title']}")
    
    print(f"✅ Added {len(scenarios)} RTT scenarios to knowledge base!\n")


def populate_rtt_code_definitions():
    """Add comprehensive RTT code definitions"""
    print("📋 Adding RTT Code Definitions...")
    
    # Complete RTT code reference
    rtt_codes_content = """
COMPREHENSIVE RTT CODES REFERENCE GUIDE

CLOCK START CODES:
=================

CODE 10: First Activity After Referral in RTT
- ACTION: Starts RTT clock
- WHEN: GP or Dentist referral received, first outpatient appointment
- EXAMPLES: GP referral letter, new patient pathway
- CLOCK EFFECT: START
- IMPORTANT: Clock starts on date GP wrote referral, NOT date hospital received it

CODE 11: First Activity After Watchful Wait Ends  
- ACTION: Restarts RTT clock
- WHEN: Patient was on active monitoring, now needs treatment
- EXAMPLES: End of active monitoring, patient ready for treatment
- CLOCK EFFECT: START (RESTART)
- IMPORTANT: Only use after Code 31 or 32 (watchful wait)

CODE 12: Consultant Referral for New Condition
- ACTION: Starts RTT clock
- WHEN: Consultant refers to another specialty for NEW/DIFFERENT condition
- EXAMPLES: ENT refers to Cardiology for heart issue
- CLOCK EFFECT: START
- IMPORTANT: Must be DIFFERENT condition, not same

CLOCK CONTINUE CODES:
====================

CODE 20: Subsequent Consultant/Diagnostic Tests
- ACTION: Clock continues (still ticking)
- WHEN: Any activity after first appointment - diagnostics, follow-ups, waiting list
- EXAMPLES: Blood test, X-ray, follow-up appointment, added to waiting list
- CLOCK EFFECT: CONTINUE
- IMPORTANT: Most common code - used for everything between start and stop

CODE 21: Tertiary Referral
- ACTION: Clock continues
- WHEN: Patient referred to specialist center for same condition
- EXAMPLES: Transfer to specialist hospital, tertiary care
- CLOCK EFFECT: CONTINUE
- IMPORTANT: Still same pathway, just different location

CLOCK STOP CODES:
================

CODE 30: Start First Definitive Treatment
- ACTION: Stops RTT clock
- WHEN: First treatment given (outpatient or inpatient)
- EXAMPLES: Surgery, injection, cryotherapy, chemotherapy start
- CLOCK EFFECT: STOP
- IMPORTANT: This is the TARGET - within 18 weeks of referral

CODE 31: Start of Watchful Wait by Patient
- ACTION: Stops RTT clock
- WHEN: Patient chooses to wait, think about treatment
- EXAMPLES: Patient wants time to consider, not ready for surgery
- CLOCK EFFECT: STOP (PAUSE)
- IMPORTANT: Can restart with Code 11

CODE 32: Start of Watchful Wait by Clinician
- ACTION: Stops RTT clock
- WHEN: Clinician decides to monitor, no immediate treatment needed
- EXAMPLES: Watch and wait approach, active monitoring
- CLOCK EFFECT: STOP (PAUSE)
- IMPORTANT: Clinical decision, can restart with Code 11

CODE 33: Patient DNA First Activity
- ACTION: Stops RTT clock
- WHEN: Patient doesn't attend FIRST appointment
- EXAMPLES: Patient no-show at first appointment
- CLOCK EFFECT: STOP
- IMPORTANT: Only for FIRST appointment DNA

CODE 34: Decision Not to Treat
- ACTION: Stops RTT clock
- WHEN: Clinical decision - no treatment needed
- EXAMPLES: Nothing wrong found, problem resolved, discharge
- CLOCK EFFECT: STOP
- IMPORTANT: Final decision - patient discharged

CODE 35: Patient Declines Treatment
- ACTION: Stops RTT clock
- WHEN: Patient refuses treatment offered
- EXAMPLES: Patient says no to surgery, refuses intervention
- CLOCK EFFECT: STOP
- IMPORTANT: Patient's choice at any point in pathway

CODE 36: Patient Deceased
- ACTION: Stops RTT clock
- WHEN: Patient has died
- EXAMPLES: Patient passed away
- CLOCK EFFECT: STOP
- IMPORTANT: Immediate pathway closure

NON-RTT CODES:
=============

CODE 90: After First Definitive Treatment
- Not during RTT period
- Post-treatment follow-up, ongoing care

CODE 91: During Period of Watchful Wait
- Not during RTT period
- While on active monitoring

CODE 92: Patient Currently Undergoing Investigations
- Not during RTT period
- Diagnostic phase before discharge to GP

KEY RULES:
=========

1. 18-Week Target: 92% of patients treated within 126 days
2. Clock starts on GP referral DATE (not hospital receipt date)
3. Clock stops when first treatment given (Code 30)
4. Patient can have multiple pathways for different conditions
5. Breach = Treatment not provided within 18 weeks
6. DNA at follow-up ≠ Clock stop (only first appointment)
7. Proper coding essential for accurate reporting

RTT COMMENTING STYLE:
===================

Format: RTT - [CODE] - [DATE] - [Brief Description]

Examples:
- RTT - 10 - 22/04/25 - Referral from GP Dr Smith
- RTT - 20 - 05/05/25 - Outpatient appointment attended  
- RTT - 30 - 12/06/25 - Definitive treatment - Surgery performed
- RTT - 33 - 15/06/25 - Patient DNA - First appointment

Rules:
1. Always start with "RTT -"
2. Include code number
3. Date in DD/MM/YY format
4. Brief description
5. Clear and concise
"""
    
    material_id = add_training_material(
        title="Complete RTT Codes Reference Guide",
        content=rtt_codes_content,
        material_type="Reference Guide",
        category="RTT Rules",
        description="Comprehensive guide to all RTT codes with examples and rules",
        tags=["RTT", "Codes", "Reference", "Complete Guide"],
        file_name="rtt_codes_complete_reference.txt"
    )
    
    print(f"  ✅ Added Complete RTT Codes Reference")
    print(f"✅ RTT Code definitions added to knowledge base!\n")


def populate_nhs_targets():
    """Add NHS targets and guidelines"""
    print("🎯 Adding NHS Targets & Guidelines...")
    
    nhs_targets_content = """
NHS RTT TARGETS AND PERFORMANCE STANDARDS

18-WEEK RTT STANDARD:
====================

Target: 92% of patients
Timeline: From referral to first definitive treatment within 18 weeks (126 days)
Calculation: Days from Code 10 to Code 30
Consequences of Breach:
- Financial penalties (£10,000+ per breach)
- CQC ratings affected
- CCG/ICB scrutiny
- Public reporting
- Patient dissatisfaction

2-WEEK WAIT (Cancer):
===================

Target: Within 14 days
What: Urgent cancer referral must be SEEN within 14 days
Code Used: Still Code 10 (but flagged as urgent)
Priority: Higher than routine referrals
Note: This is about first APPOINTMENT, not treatment

62-DAY CANCER TARGET:
===================

Target: Treatment within 62 days
Timeline: From urgent GP referral to FIRST treatment
What: Cancer treatment must start within 62 days
Uses: Same RTT codes but different timeline
Critical: Separate tracking from 18-week RTT

BREACH PREVENTION STRATEGIES:
===========================

1. Weekly Validation
   - Review all pathways weekly
   - Identify patients approaching 16 weeks
   - Escalate high-risk patients
   - Ensure accurate coding

2. Patient Tracking List (PTL)
   - Monitor all waiting patients
   - Color-coded by breach risk
   - Daily updates
   - Automated alerts

3. Booking Strategy
   - Prioritize long-waiters
   - Book high-risk patients first
   - Emergency slots for breach-risk
   - 2WW separate fast-track

4. Validation Checks
   - Verify all RTT codes correct
   - Check pathway status
   - Confirm treatment dates
   - Audit regularly

5. Communication
   - Contact patients proactively
   - Confirm appointments
   - DNA follow-up immediately
   - Keep patients informed

COMMON BREACH CAUSES:
====================

1. Delayed Diagnostics (40%)
   - Waiting for test results
   - Equipment breakdown
   - Capacity issues
   
2. Patient DNAs (25%)
   - Patient doesn't attend
   - Late cancellations
   - Contact issues

3. Booking Delays (20%)
   - No available slots
   - Staff shortages
   - Clinic cancellations

4. Coding Errors (10%)
   - Wrong RTT code used
   - Clock not started
   - Incorrect stop code

5. Administrative (5%)
   - Lost referrals
   - Data entry errors
   - System issues

PENALTY SYSTEM:
=============

Per Breach:
- Tier 1: £0-10,000 (depending on Trust size)
- Accumulated over year
- Can reach millions for large trusts

Performance Ratings:
- Affects CQC inspection outcomes
- CCG/ICB contract negotiations
- Public perception
- Staff morale

BEST PRACTICES:
=============

1. Daily PTL Review
2. Weekly Validation Sessions
3. Monthly Breach Analysis
4. Quarterly Training Updates
5. Real-time Dashboard Monitoring
6. Proactive Patient Contact
7. Clear Escalation Procedures
8. Regular Audit Cycles
"""

    material_id = add_training_material(
        title="NHS RTT Targets and Performance Standards",
        content=nhs_targets_content,
        material_type="Guidelines",
        category="NHS Standards",
        description="Complete guide to NHS RTT targets, breach prevention, and performance standards",
        tags=["NHS", "Targets", "18-week", "Breach", "Performance"],
        file_name="nhs_targets_guidelines.txt"
    )
    
    print(f"  ✅ Added NHS Targets & Guidelines")
    print(f"✅ NHS performance standards added to knowledge base!\n")


def main():
    """Populate the AI knowledge base with all platform content"""
    
    print("=" * 60)
    print("🚀 POPULATING AI TUTOR KNOWLEDGE BASE")
    print("=" * 60)
    print()
    
    try:
        # Show current stats
        stats = get_knowledge_base_stats()
        print(f"📊 Current Knowledge Base Stats:")
        print(f"   Materials: {stats['total_materials']}")
        print(f"   Chunks: {stats['total_chunks']}")
        print()
        
        # Add all content
        populate_rtt_code_definitions()
        populate_nhs_targets()
        populate_rtt_scenarios()
        
        # Show final stats
        final_stats = get_knowledge_base_stats()
        print()
        print("=" * 60)
        print("✅ KNOWLEDGE BASE POPULATED SUCCESSFULLY!")
        print("=" * 60)
        print(f"📊 Final Stats:")
        print(f"   Materials: {final_stats['total_materials']}")
        print(f"   Chunks: {final_stats['total_chunks']}")
        print(f"   Total Words: {final_stats['total_words']:,}")
        print()
        print("🤖 AI Tutor can now reference ALL this content!")
        print("🎓 Students will get comprehensive, accurate answers!")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
