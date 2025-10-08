"""
T21 AI RTT TUTOR - 24/7 INTELLIGENT ASSISTANT
Powered by AI to answer ANY RTT question instantly

Features:
- Natural language understanding
- RTT-specific knowledge base
- Conversational interface
- Chat history
- Example generation
- Quiz suggestions
- Available on all pages
"""

from datetime import datetime
import re

# ============================================
# RTT KNOWLEDGE BASE
# ============================================

RTT_KNOWLEDGE_BASE = {
    "codes": {
        "10": {
            "name": "1st Activity After Referral in RTT",
            "action": "Starts RTT clock",
            "description": "Any referral from GP's or Dentists as the patient's referral is registered. First appointment in a new patient pathway.",
            "examples": ["GP referral letter received", "Dentist referral", "First outpatient appointment", "Starting a new pathway"],
            "clock_effect": "START"
        },
        "11": {
            "name": "1st Activity After Watchful Wait Ends",
            "action": "Restarts RTT clock",
            "description": "If a patient has been on active monitoring and treatment is now needed. Activity at the start of a new RTT period.",
            "examples": ["End of active monitoring", "Patient ready for treatment", "Watchful wait concluded"],
            "clock_effect": "START"
        },
        "12": {
            "name": "Consultant Referral for a New Condition",
            "action": "Starts RTT clock",
            "description": "When a Consultant referral for another specialty is added to the existing referral made.",
            "examples": ["Consultant refers to another specialty", "New condition discovered", "Additional specialty needed"],
            "clock_effect": "START"
        },
        "20": {
            "name": "Subsequent Consultant/Diagnostic Tests",
            "action": "Clock continues (still ticking)",
            "description": "For anything that happens along a pathway after the 1st activity. Includes diagnostics, subsequent appointments, additions to waiting list.",
            "examples": ["Diagnostic test ordered", "Follow-up appointment", "Added to waiting list", "Subsequent consultant visit"],
            "clock_effect": "CONTINUE"
        },
        "21": {
            "name": "Tertiary Referral",
            "action": "Clock continues (still ticking)",
            "description": "When a patient is referred to another health care provider for the same condition and it is not anticipated that they will return.",
            "examples": ["Referred to specialist center", "Transfer to tertiary hospital", "Specialist treatment elsewhere"],
            "clock_effect": "CONTINUE"
        },
        "30": {
            "name": "Start 1st Definitive Treatment",
            "action": "Stops RTT clock",
            "description": "When 1st definitive treatment is given. Can be in outpatient or inpatient setting. This is the start of treatment that is intended to manage the patient's disease, condition or injury.",
            "examples": ["Surgery performed", "Cryotherapy", "Injection given", "First treatment started"],
            "clock_effect": "STOP"
        },
        "31": {
            "name": "Start of Watchful Wait by Patient",
            "action": "Stops RTT clock",
            "description": "When a patient chooses to decline treatment for the time being to see how their condition develops. Patient may think about treatment or is on a waiting list and comes back for a follow up appointment.",
            "examples": ["Patient wants to wait", "Patient thinking about treatment", "Patient declines for now"],
            "clock_effect": "STOP"
        },
        "32": {
            "name": "Start of Watchful Wait by Clinician",
            "action": "Stops RTT clock",
            "description": "When a clinician decides to monitor the patient's condition and not offer treatment. May occur following an outpatient appointment, a diagnostic procedure, or if a patients' treatment plan changes.",
            "examples": ["Clinician decides to monitor", "Watch and wait approach", "Active monitoring", "No immediate treatment needed"],
            "clock_effect": "STOP"
        },
        "33": {
            "name": "Patient DNA's the 1st Activity",
            "action": "Stops RTT clock",
            "description": "When a patient is not brought to (DNA's) their 1st appointment/episode of an 18 week pathway having been added to a waiting list without attending an outpatient appointment.",
            "examples": ["First appointment DNA", "Patient didn't attend first visit", "No show at first appointment"],
            "clock_effect": "STOP"
        },
        "34": {
            "name": "Decision Not to Treat",
            "action": "Stops RTT clock",
            "description": "When a clinical decision not to treat has been made.",
            "examples": ["No treatment required", "Nothing wrong found", "Clinical decision no action needed"],
            "clock_effect": "STOP"
        },
        "35": {
            "name": "Patient Declines Treatment",
            "action": "Stops RTT clock",
            "description": "If the patient/carer declines treatment at any point along the 18 week pathway.",
            "examples": ["Patient refuses treatment", "Patient declines surgery", "Patient says no"],
            "clock_effect": "STOP"
        },
        "36": {
            "name": "Patient Deceased",
            "action": "Stops RTT clock",
            "description": "To be used if the patient died.",
            "examples": ["Patient passed away", "Patient deceased"],
            "clock_effect": "STOP"
        },
        "90": {
            "name": "After 1st Definitive Treatment",
            "action": "Not during RTT period",
            "description": "For activity after 1st definitive treatment has started. For any activity that follows an emergency admission or when a patient is undergoing treatment.",
            "examples": ["Follow-up after treatment", "Post-operative care", "Treatment ongoing"],
            "clock_effect": "NOT RTT"
        },
        "91": {
            "name": "During a Period of Watchful Wait",
            "action": "Not during RTT period",
            "description": "During a period of watchful wait underway and continues with this episode of care (i.e. no decision to treat has been made).",
            "examples": ["During active monitoring", "Watchful wait ongoing", "Monitoring period"],
            "clock_effect": "NOT RTT"
        },
        "92": {
            "name": "Patient Currently Undergoing Investigations",
            "action": "Not during RTT period",
            "description": "Patient needs from CPC requesting diagnostic investigations only. Where it is envisaged that the patient will be returned to the care of their GP but hasn't yet been discharged.",
            "examples": ["Diagnostic tests requested", "Investigations in progress", "Awaiting test results"],
            "clock_effect": "NOT RTT"
        }
    },
    
    "targets": {
        "18_week": {
            "name": "18-Week RTT Standard",
            "target": "92% of patients",
            "description": "From referral to first definitive treatment within 18 weeks (126 days)",
            "calculation": "Days from Code 10 to Code 30 (or other stop code)"
        },
        "2ww": {
            "name": "2-Week Wait (Cancer)",
            "target": "Within 14 days",
            "description": "Urgent cancer referral must be seen within 14 days (2 weeks)",
            "note": "Still uses Code 10 for referral, but booking priority is higher"
        },
        "62_day": {
            "name": "62-Day Cancer Target",
            "target": "From referral to treatment",
            "description": "Cancer treatment must start within 62 days of urgent GP referral",
            "note": "Uses same RTT codes, but different timeline"
        }
    },
    
    "concepts": {
        "clock_start": "RTT clock STARTS with: Code 10 (referral), Code 11 (after watchful wait), Code 12 (consultant referral for new condition).",
        "clock_stop": "Clock STOPS with: Code 30 (treatment), Code 31 (patient watchful wait), Code 32 (clinician watchful wait), Code 33 (DNA 1st activity), Code 34 (decision not to treat), Code 35 (patient declines), Code 36 (deceased).",
        "clock_continue": "Clock CONTINUES with: Code 20 (subsequent consultant/diagnostics), Code 21 (tertiary referral).",
        "not_rtt": "NOT during RTT period: Code 90 (after treatment), Code 91 (during watchful wait), Code 92 (undergoing investigations).",
        "multiple_pathways": "A patient can have multiple RTT pathways for different conditions simultaneously.",
        "breach": "Breach occurs when treatment not provided within 18 weeks (126 days). Fines can apply.",
        "pas_system": "PAS = Patient Administration System. Core NHS IT system for managing pathways.",
        "commenting_style": """RTT Commenting Style is the format used to record RTT events in patient records (PAS system).

**Standard Format: RTT - [Code] - [Date] - [Brief Description]**

**Examples:**
- RTT - 10 - 22/04/25 - Referral from GP Dr Smith
- RTT - 20 - 05/05/25 - Outpatient appointment attended
- RTT - 30 - 12/06/25 - Definitive treatment - Surgery performed

**Key Rules:**
1. Always start with "RTT -"
2. Include the RTT code number
3. Add the date (DD/MM/YY format)
4. Brief description of what happened
5. Keep it clear and concise

**Why it matters:** Proper commenting helps track pathways, audit compliance, and ensure accurate breach calculations."""
    }
}


# ============================================
# AI TUTOR FUNCTIONS
# ============================================

def get_code_info(code_number):
    """Get information about a specific RTT code"""
    code = str(code_number).strip()
    if code in RTT_KNOWLEDGE_BASE["codes"]:
        info = RTT_KNOWLEDGE_BASE["codes"][code]
        return f"""
**Code {code}: {info['name']}**

📋 **What it means:** {info['description']}

⏰ **Clock effect:** {info['action']} (Clock {info['clock_effect']})

💡 **Examples:**
{chr(10).join(f'- {ex}' for ex in info['examples'])}
"""
    return None


def answer_question(question):
    """
    Answer RTT-related questions using knowledge base
    """
    question_lower = question.lower()
    
    # Code-specific questions
    for code, info in RTT_KNOWLEDGE_BASE["codes"].items():
        if f"code {code}" in question_lower or f"code{code}" in question_lower:
            return get_code_info(code)
    
    # DNA questions
    if "dna" in question_lower or "did not attend" in question_lower or "didn't attend" in question_lower:
        return get_code_info("33")
    
    # Commenting style questions
    if "comment" in question_lower or "commenting style" in question_lower or "how to comment" in question_lower or "how do i comment" in question_lower:
        return f"""
📝 **RTT Commenting Style**

{RTT_KNOWLEDGE_BASE['concepts']['commenting_style']}

💡 **Quick tip:** Always record events on the day they happen to ensure accurate pathway tracking!
"""
    
    # Treatment questions
    if "treatment" in question_lower and ("first" in question_lower or "definitive" in question_lower):
        return get_code_info("30")
    
    # Referral questions
    if "referral" in question_lower and "gp" in question_lower:
        return get_code_info("10")
    
    # Clock questions
    if "clock" in question_lower:
        if "start" in question_lower:
            return f"""
⏰ **When Does the RTT Clock Start?**

{RTT_KNOWLEDGE_BASE['concepts']['clock_start']}

📋 **Code used:** Code 10 (GP Referral)

💡 **Important:** The clock starts on the DATE the GP wrote the referral letter, NOT the date your hospital received it!

**Example:** GP writes referral on 01/03/2024, you receive it on 05/03/2024. Clock starts 01/03/2024.
"""
        elif "stop" in question_lower:
            return f"""
⏰ **When Does the RTT Clock Stop?**

{RTT_KNOWLEDGE_BASE['concepts']['clock_stop']}

📋 **Codes that STOP the clock:**
- Code 30: First Definitive Treatment
- Code 31: Patient Declined Treatment
- Code 34: Discharge - No Treatment Needed

⚠️ **Remember:** DNA (Code 33) does NOT stop the clock - it continues!

💡 **After multiple DNAs:** Trust policy may discharge patient (Code 34).
"""
        elif "pause" in question_lower:
            return f"""
⏰ **When Does the RTT Clock Pause?**

{RTT_KNOWLEDGE_BASE['concepts']['clock_pause']}

📋 **Codes that PAUSE the clock:**
- Code 32: Active Monitoring (clinician decision)
- Code 35: Patient Medically Unfit

🔄 **To restart:** Use Code 11 when patient is ready

💡 **Pause vs Stop:** Paused clocks can resume. Stopped clocks are final.
"""
    
    # 18-week target
    if "18 week" in question_lower or "18-week" in question_lower:
        target = RTT_KNOWLEDGE_BASE["targets"]["18_week"]
        return f"""
📅 **18-Week RTT Standard**

🎯 **Target:** {target['target']} must be treated within 18 weeks

📊 **What it means:** {target['description']}

🧮 **Calculation:** {target['calculation']}

⏰ **Timeline:** 18 weeks = 126 days

⚠️ **Breach:** If treatment not provided within 126 days, it's a breach. NHS trusts can be fined £10,000+ per breach.

💡 **Tip:** Weekly validation helps identify patients approaching breach!
"""
    
    # 2WW questions
    if "2ww" in question_lower or "2-week wait" in question_lower or "2 week wait" in question_lower:
        target = RTT_KNOWLEDGE_BASE["targets"]["2ww"]
        return f"""
🚨 **2-Week Wait (Cancer Pathway)**

⏰ **Target:** {target['target']}

📋 **Description:** {target['description']}

💡 **Important:** {target['note']}

🎯 **What this means:**
- Patient must be SEEN (first appointment) within 14 days
- Still uses Code 10 for the referral
- Higher booking priority than routine
- Separate from 62-day target

❓ **Common question:** "Does 2WW use a different code?" 
✅ **Answer:** NO! Still Code 10, but urgency is higher.
"""
    
    # Breach questions
    if "breach" in question_lower:
        return """
⚠️ **RTT Breach Explained**

📊 **What is a breach?**
A breach occurs when a patient doesn't receive their first definitive treatment within 18 weeks (126 days) of referral.

💰 **Cost:**
- Fines can be £10,000+ per breach
- NHS trusts lose millions annually

🛡️ **How to prevent:**
1. Weekly pathway validation
2. Monitor patients approaching 16 weeks
3. Escalate high-risk patients
4. Use breach risk calculator
5. Ensure accurate coding

🚨 **If breach imminent:**
1. Escalate to RTT Manager IMMEDIATELY
2. Contact patient urgently
3. Book emergency appointment
4. Document reason
5. Report to ICB/CCG

💡 **Remember:** Prevention is better than cure! Proactive monitoring is key.
"""
    
    # Multiple pathways
    if "multiple pathway" in question_lower or "multiple pathways" in question_lower:
        return """
👥 **Multiple RTT Pathways**

✅ **YES, a patient can have multiple RTT pathways!**

📋 **Examples:**
- Patient has knee replacement pathway (Orthopedics)
- Same patient has cataract surgery pathway (Ophthalmology)
- Both pathways run independently

🎯 **Each pathway:**
- Has its own clock
- Has its own RTT code
- Tracks separately
- Independent timelines

💡 **Important:** Same patient, different conditions = different pathways!
"""
    
    # PAS System
    if "pas" in question_lower or "patient administration" in question_lower:
        return """
🖥️ **PAS System (Patient Administration System)**

📋 **What is PAS?**
Core NHS IT system for managing:
- Patient registration
- Appointments
- RTT pathways
- Waiting lists
- Documents
- Referrals

🎯 **Why it's important:**
- All RTT codes entered in PAS
- Tracks patient journeys
- Generates reports
- Monitors breaches
- Essential for RTT management

💡 **Skills needed:**
- Patient registration
- Booking appointments
- Creating pathways
- Entering RTT codes
- Validating data
- Running reports

🎓 **T21 Training includes:**
Full PAS system simulator for hands-on practice!
"""
    
    # Try to give helpful response based on keywords
    response_parts = []
    
    # Check for any code mentions
    if "code" in question_lower:
        response_parts.append("""
📋 **RTT Codes Overview:**

**STARTING CODES (Clock Starts):**
- Code 10: GP Referral
- Code 11: After Watchful Wait
- Code 12: Consultant Referral

**CONTINUING CODES (Clock Continues):**
- Code 20: Subsequent appointments/diagnostics
- Code 21: Tertiary referral

**STOPPING CODES (Clock Stops):**
- Code 30: First Definitive Treatment
- Code 31: Patient Declined
- Code 32: Clinician Watchful Wait
- Code 33: Patient DNA 1st Activity
- Code 34: Decision Not to Treat
- Code 35: Patient Declines Treatment
- Code 36: Patient Deceased

**NON-RTT CODES:**
- Code 90: After Treatment Complete
- Code 91: During Watchful Wait
- Code 92: Undergoing Investigations
""")
    
    # Check for pathway-related terms
    if "pathway" in question_lower:
        response_parts.append("""
🛤️ **RTT Pathways:**

An RTT pathway is a patient's journey from referral to treatment.

**Key points:**
- Starts with referral (Code 10)
- Tracks through appointments and diagnostics (Code 20)
- Ends with treatment (Code 30) or other stop event
- Must complete within 18 weeks (126 days)
- Each patient can have multiple pathways for different conditions
""")
    
    # Check for target-related terms
    if "target" in question_lower or "18 week" in question_lower or "week" in question_lower:
        response_parts.append("""
🎯 **NHS RTT Targets:**

**18-Week RTT Target:**
- 92% of patients must receive treatment within 18 weeks
- Clock starts at referral
- Clock stops at first definitive treatment
- 18 weeks = 126 days

**Other NHS targets:**
- 2-Week Wait (Cancer): Urgent referral to first appointment
- 62-Day Cancer: Urgent referral to first treatment
""")
    
    # Check for breach-related terms
    if "breach" in question_lower or "breach" in question_lower:
        response_parts.append("""
⚠️ **RTT Breaches:**

A breach occurs when a patient doesn't receive treatment within 18 weeks.

**Preventing breaches:**
- Book appointments promptly
- Monitor waiting lists daily
- Escalate long-waiters
- Ensure accurate RTT coding
- Validate pathways regularly
- Communicate with patients

**Consequences:**
- Financial penalties for Trust
- Affects Trust performance ratings
- Impact on patient care
- Regulatory scrutiny
""")
    
    # If we found relevant content, return it
    if response_parts:
        return "\n\n".join(response_parts) + "\n\n💡 **Need more specific info?** Ask me about a specific code, scenario, or topic!"
    
    # Default helpful response
    return """
🤖 **I'm here to help with RTT!**

I can answer questions about:
- 📋 RTT Codes (10-36, 90-92)
- ⏰ Clock management (start, stop, continue)
- 🎯 NHS targets (18-week, 2WW, 62-day)
- ⚠️ Breaches and prevention
- 🖥️ PAS systems and commenting
- 👥 Multiple pathways
- 🚨 DNAs and patient events
- 📝 RTT commenting style

**Try asking:**
- "What is commenting style?"
- "When does the clock stop?"
- "What code for GP referral?"
- "How to prevent breaches?"
- "What's Code 20?"
- "Explain the 18-week target"
- "What happens if patient DNA?"

💡 **Be specific and I'll give you a detailed answer!**
"""


def generate_related_quiz(topic):
    """Suggest related quiz based on topic"""
    quiz_suggestions = {
        "dna": "Try Quiz: Patient DNA Management (Code 33)",
        "treatment": "Try Quiz: First Definitive Treatment (Code 30)",
        "referral": "Try Quiz: GP Referrals and Code 10",
        "clock": "Try Quiz: Clock Management Basics",
        "breach": "Try Quiz: Breach Prevention Strategies",
        "cancer": "Try Quiz: Cancer Pathways (2WW and 62-day)"
    }
    
    for key, suggestion in quiz_suggestions.items():
        if key in topic.lower():
            return f"\n\n📝 **Want to practice?** {suggestion}"
    
    return "\n\n📝 **Want to practice?** Head to Interactive Learning Center for quizzes!"


# ============================================
# CHAT HISTORY MANAGEMENT
# ============================================

class ChatHistory:
    """Manage chat history for student"""
    
    def __init__(self):
        self.messages = []
    
    def add_message(self, role, content):
        """Add message to history"""
        self.messages.append({
            'role': role,  # 'user' or 'assistant'
            'content': content,
            'timestamp': datetime.now()
        })
    
    def get_history(self, limit=10):
        """Get recent chat history"""
        return self.messages[-limit:]
    
    def clear(self):
        """Clear chat history"""
        self.messages = []
    
    def export(self):
        """Export chat for download"""
        export_text = "T21 AI TUTOR - CHAT HISTORY\n"
        export_text += "="*50 + "\n\n"
        
        for msg in self.messages:
            timestamp = msg['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
            role = "YOU" if msg['role'] == 'user' else "AI TUTOR"
            export_text += f"[{timestamp}] {role}:\n"
            export_text += f"{msg['content']}\n\n"
        
        return export_text
