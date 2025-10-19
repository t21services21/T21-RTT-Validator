"""
T21 AI RTT TUTOR - 24/7 INTELLIGENT ASSISTANT
Powered by OpenAI GPT-4 to answer ANY RTT, NHS, and Healthcare Admin question

Features:
- Real AI intelligence (GPT-4)
- Comprehensive RTT knowledge
- NHS administrative procedures
- Hospital management
- PAS systems expertise
- Natural language understanding
- Conversational interface
- Chat history
- Available on all pages
"""

from datetime import datetime
import re
import streamlit as st
from ai_knowledge_base import search_knowledge_base, export_knowledge_for_ai

# OpenAI integration
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

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
            "name": "Patient-Initiated Pause (Watchful Wait)",
            "action": "Stops RTT clock (PAUSE)",
            "description": "When a PATIENT chooses to pause their pathway to think about treatment options or see how their condition develops. This is a PAUSE, not a refusal. Patient wants time to consider.",
            "examples": ["Patient wants time to think", "Patient considering options", "Patient requests pause to decide", "Let me think about surgery"],
            "clock_effect": "STOP (Can restart with Code 11)",
            "restart": "YES - Use Code 11 when patient ready"
        },
        "32": {
            "name": "Hospital/Clinician-Initiated Pause (Active Monitoring)",
            "action": "Stops RTT clock (PAUSE)",
            "description": "When HOSPITAL/CLINICIAN decides to actively monitor the patient's condition instead of immediate treatment. This is clinical watchful waiting, not patient's decision.",
            "examples": ["Clinician-initiated monitoring", "Watch and wait approach", "Active surveillance", "Hospital decides to monitor for 6 months"],
            "clock_effect": "STOP (Can restart with Code 11)",
            "restart": "YES - Use Code 11 when treatment needed"
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
# OPENAI GPT-4 INTEGRATION
# ============================================

SYSTEM_PROMPT = """You are an expert RTT (Referral to Treatment), NHS, and Healthcare Administration tutor for T21 Services training platform.

Your expertise covers:
- ALL RTT codes (10-36, 90-92) and their applications
- RTT pathway management and validation
- NHS 18-week target, 2WW, 62-day cancer pathways
- PAS (Patient Administration System) operations
- Hospital administrative procedures
- Booking, scheduling, and waiting list management
- Breach prevention and management
- Patient management (DNAs, cancellations, rescheduling)
- Referral processing
- Reporting and auditing
- Staff roles and responsibilities
- NHS operational procedures
- Healthcare data management
- Clinic management
- Any other healthcare administration topics

**CRITICAL: RTT COMMENTING STYLE**
When asked about "commenting style" or "how to comment RTT", ALWAYS provide this specific format:

**Standard RTT Commenting Format:**
RTT - [CODE] - [DATE] - [Brief Description]

**Examples:**
- RTT - 10 - 22/04/25 - Referral from GP Dr Smith
- RTT - 20 - 05/05/25 - Outpatient appointment attended
- RTT - 30 - 12/06/25 - Definitive treatment - Surgery performed
- RTT - 33 - 15/06/25 - Patient DNA - First appointment

**Key Rules:**
1. Always start with "RTT -"
2. Include the RTT code number
3. Add the date in DD/MM/YY format
4. Include brief description of what happened
5. Keep it clear, concise, and professional
6. Record on the day the event happens

**Why it matters:** Proper commenting ensures accurate pathway tracking, audit compliance, and breach calculations.

INSTRUCTIONS:
1. Provide accurate, professional, and helpful answers
2. Use clear, concise language
3. Include practical examples when relevant
4. Format responses with markdown (bold, lists, etc.)
5. If asked about RTT codes, explain clock effects
6. Be encouraging and supportive to learners
7. If you don't know something specific, say so honestly
8. Always relate answers back to real-world application
9. For commenting style questions, ALWAYS use the exact format shown above

TONE: Professional, friendly, encouraging, and educational."""

def ask_gpt4(question):
    """Use OpenAI GPT-4 to answer ANY question intelligently with YOUR training materials"""
    try:
        # Check if API key is available
        if not OPENAI_AVAILABLE:
            return None
        
        # Get API key from Streamlit secrets
        api_key = st.secrets.get("OPENAI_API_KEY")
        if not api_key:
            return None
        
        # STEP 1: Search YOUR uploaded knowledge base first!
        relevant_materials = search_knowledge_base(question, limit=3)
        
        # Build context from your materials
        custom_knowledge = ""
        if relevant_materials:
            custom_knowledge = "\n\n**IMPORTANT: Use this information from T21 training materials:**\n\n"
            for idx, material in enumerate(relevant_materials, 1):
                custom_knowledge += f"**From {material['material_title']}:**\n{material['content']}\n\n"
        
        # STEP 2: Create enhanced prompt with YOUR materials
        enhanced_prompt = SYSTEM_PROMPT
        if custom_knowledge:
            enhanced_prompt += custom_knowledge
            enhanced_prompt += "\n\n**CRITICAL: Always reference and prioritize the T21 training materials provided above when answering!**"
        
        # Initialize OpenAI client
        client = OpenAI(api_key=api_key)
        
        # Call GPT-4 with YOUR knowledge
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": enhanced_prompt},
                {"role": "user", "content": question}
            ],
            max_tokens=1000,
            temperature=0.7
        )
        
        answer = response.choices[0].message.content
        
        # Add reference note if materials were used
        if relevant_materials:
            answer += f"\n\n📚 *Answer based on T21 training materials*"
        
        return answer
        
    except Exception as e:
        # Fallback to keyword-based system if GPT-4 fails
        print(f"GPT-4 error: {e}")
        return None


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
    Answer RTT-related questions using SMART 4-TIER SYSTEM:
    1. Check cache (previous answers) - FREE & INSTANT!
    2. Try built-in knowledge - FREE!
    3. Use OpenAI if needed - Paid, but SAVE to cache
    4. Fallback helper
    
    This system LEARNS from every question to reduce costs!
    """
    from ai_question_cache import search_cache, save_to_cache
    
    question_lower = question.lower()
    
    # TIER 0: Check if we've answered this before! (FREE & INSTANT! ⚡)
    cached_answer = search_cache(question, similarity_threshold=0.85)
    if cached_answer:
        match_type = cached_answer.get('match_type', 'exact')
        times_used = cached_answer.get('times_used', 1)
        
        if match_type == 'exact':
            footer = f"\n\n🎯 *Instant answer from cache (asked {times_used} times before) - $0 cost!*"
        else:
            similarity = cached_answer.get('similarity', 0.85)
            footer = f"\n\n🎯 *Similar question answered before ({similarity*100:.0f}% match, used {times_used} times) - $0 cost!*"
        
        return cached_answer['answer'] + footer
    
    # TIER 1: Try built-in knowledge base (FREE! 🆓)
    builtin_answer = get_builtin_answer(question_lower)
    
    # If we got a good answer from built-in knowledge, use it AND cache it!
    if builtin_answer:
        final_answer = builtin_answer + "\n\n💡 *Answered using T21's built-in RTT knowledge base*"
        save_to_cache(question, final_answer, source="builtin")
        return final_answer
    
    # TIER 2: Use OpenAI if needed (Paid, but we'll SAVE it!)
    gpt4_answer = ask_gpt4(question)
    if gpt4_answer:
        final_answer = gpt4_answer + "\n\n🤖 *Enhanced answer using AI (built-in knowledge + OpenAI)*"
        # IMPORTANT: Save to cache so next student gets it FREE!
        save_to_cache(question, final_answer, source="openai")
        return final_answer
    
    # TIER 3: Generic fallback if everything fails
    return """
I'm here to help with RTT questions! 

Try asking about:
- RTT codes (e.g., "What is Code 10?")
- Clock rules (e.g., "When does the clock start?")
- NHS targets (e.g., "What is the 18-week target?")
- Specific scenarios (e.g., "How do I handle DNA?")

Or browse the Training Library for real RTT scenarios!
"""


def get_builtin_answer(question_lower):
    """
    Get answer from built-in knowledge base (FREE!)
    Returns None if question is too complex for built-in knowledge
    """
    
    # RTT meaning / what is RTT questions
    if ("what is rtt" in question_lower or "rtt meaning" in question_lower or 
        "what does rtt mean" in question_lower or "rtt stand for" in question_lower or
        "define rtt" in question_lower):
        return """
# 🏥 RTT - Referral to Treatment

## What is RTT?
**RTT stands for Referral to Treatment** - it's the NHS system for tracking how long patients wait from their GP referral to receiving first definitive treatment.

## The 18-Week Target
- 🎯 **92% of patients** must receive treatment within **18 weeks** (126 days)
- 📅 This is a **legal NHS requirement**
- 💰 Trusts can be fined £10,000+ per breach

## Why RTT Matters
✅ **Patient Care** - Faster treatment = better outcomes  
✅ **Performance** - NHS monitors Trust performance  
✅ **Funding** - Affects Trust ratings and funding  
✅ **Legal** - Patients have right to treatment within 18 weeks  

## Key RTT Concepts
📋 **Pathway**: Patient's journey from referral to treatment  
⏰ **Clock Start**: When 18-week countdown begins (Code 10)  
🏁 **Clock Stop**: When countdown ends (Code 30 - treatment)  
🚨 **Breach**: When treatment takes longer than 18 weeks  

## RTT Codes
RTT uses codes (10-36, 90-92) to track pathway events:
- **Code 10**: GP Referral (Clock START)
- **Code 20**: Appointments/Diagnostics (Clock CONTINUES)
- **Code 30**: First Treatment (Clock STOP)

## Example RTT Pathway
```
RTT - 10 - 22/04/25 - Referral from GP Dr Smith (Clock starts)
RTT - 20 - 05/05/25 - Outpatient appointment attended (Clock continues)
RTT - 30 - 12/06/25 - Definitive treatment - Surgery performed (Clock stops)
Wait time: 51 days ✅ (within 126 days)
```

## Your Role as RTT Administrator
- Track patient pathways
- Ensure timely treatment
- Use correct RTT codes
- Prevent breaches
- Report to NHS
"""
    
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
    
    # Return None to signal that OpenAI should handle this question
    # This allows complex questions to get AI-enhanced answers
    return None


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
