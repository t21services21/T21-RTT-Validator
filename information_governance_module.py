"""
INFORMATION GOVERNANCE MODULE
NHS-Compliant Data Protection & Confidentiality Training

MANDATORY TOPICS:
- GDPR & Data Protection Act 2018
- NHS Caldicott Principles
- Information Security
- Patient Confidentiality
- Cyber Security
- Data Breach Procedures
- Patient Consent
- Legal Requirements

COMPLETION REQUIREMENT:
All NHS staff must achieve 100% on IG assessment annually
"""

# Core content for Information Governance training
IG_TRAINING_MODULES = {
    "gdpr_basics": {
        "title": "GDPR & Data Protection Fundamentals",
        "content": """
**What is GDPR?**

GDPR (General Data Protection Regulation) is UK/EU law protecting personal data.

**8 Key GDPR Principles:**
1. **Lawfulness, fairness, transparency** - Process data legally and openly
2. **Purpose limitation** - Collect data for specific purposes only
3. **Data minimisation** - Only collect what you need
4. **Accuracy** - Keep data accurate and up to date
5. **Storage limitation** - Don't keep data longer than necessary
6. **Integrity and confidentiality** - Keep data secure
7. **Accountability** - Prove compliance
8. **Individual rights** - Respect patient rights

**Patient Rights Under GDPR:**
- Right to be informed
- Right of access (Subject Access Request)
- Right to rectification
- Right to erasure ("right to be forgotten")
- Right to restrict processing
- Right to data portability
- Right to object
- Rights related to automated decision making

**Lawful Basis for NHS Processing:**
- Patient consent
- Legal obligation
- Vital interests (life/death)
- Public task (NHS statutory duty)
- Legitimate interests

**NHS Specific: We process patient data under "public task" and sometimes "vital interests".**
        """,
        "quiz": [
            {
                "question": "How many key GDPR principles are there?",
                "options": ["5", "6", "7", "8"],
                "correct": 3,
                "explanation": "There are 8 key GDPR principles that organizations must follow."
            },
            {
                "question": "What does 'data minimisation' mean?",
                "options": [
                    "Delete data after 1 year",
                    "Only collect data you actually need",
                    "Share data with minimum people",
                    "Store data in minimum space"
                ],
                "correct": 1,
                "explanation": "Data minimisation means only collecting the data you actually need for your purpose."
            }
        ]
    },
    
    "caldicott_principles": {
        "title": "NHS Caldicott Principles",
        "content": """
**The 8 Caldicott Principles** (NHS Confidentiality Framework)

**Principle 1: Justify the Purpose**
Every use of confidential patient information must be clearly justified.
❌ DON'T: Look up a friend's medical record out of curiosity
✅ DO: Access records only for direct patient care

**Principle 2: Don't Use Personal Confidential Data Unless Necessary**
Use anonymised data whenever possible.
❌ DON'T: Include full name/NHS number in general statistics
✅ DO: Use anonymised data for reports and analysis

**Principle 3: Use the Minimum Necessary**
Only access/share the minimum information needed.
❌ DON'T: Share entire medical history when only appointment date needed
✅ DO: Share only the specific information required

**Principle 4: Access on a Strict Need-to-Know Basis**
Only people who need the information should have access.
❌ DON'T: Discuss patient details with colleagues not involved in their care
✅ DO: Only share with staff directly caring for the patient

**Principle 5: Everyone Should Be Aware of Their Responsibilities**
All staff must understand confidentiality rules.
✅ Complete annual Information Governance training
✅ Read and follow your Trust's confidentiality policy

**Principle 6: Comply with the Law**
Follow GDPR, Data Protection Act, and common law duty of confidence.
✅ Understand legal requirements
✅ Report breaches immediately

**Principle 7: The Duty to Share Information Can Be as Important as the Duty to Protect**
Sometimes you MUST share information (safeguarding, public health).
✅ DO: Share information to protect vulnerable adults/children
✅ DO: Report notifiable diseases to Public Health England

**Principle 8: Inform Patients How Their Data Is Used**
Patients should know how their information is used.
✅ Display privacy notices in clinics
✅ Provide information about data sharing
✅ Obtain consent where required
        """,
        "quiz": [
            {
                "question": "How many Caldicott Principles are there?",
                "options": ["5", "6", "7", "8"],
                "correct": 3,
                "explanation": "There are 8 Caldicott Principles governing NHS confidentiality."
            },
            {
                "question": "Which principle allows you to share information for safeguarding?",
                "options": [
                    "Principle 1 - Justify the purpose",
                    "Principle 3 - Minimum necessary",
                    "Principle 7 - Duty to share can be as important as duty to protect",
                    "Principle 8 - Inform patients"
                ],
                "correct": 2,
                "explanation": "Principle 7 recognizes that sharing information to protect vulnerable people is sometimes mandatory."
            }
        ]
    },
    
    "confidentiality_scenarios": {
        "title": "Confidentiality Scenarios - What Would You Do?",
        "content": """
**Real-World Scenarios**

Test your knowledge with these realistic situations!
        """,
        "scenarios": [
            {
                "scenario": """
**Scenario 1: The Curious Colleague**

Your colleague asks: "Did you see Mrs. Jones' test results? I heard she's really ill!"

Mrs. Jones is NOT your colleague's patient.

**What should you do?**
                """,
                "options": [
                    "Tell them the results - they're a colleague",
                    "Refuse to discuss - it's confidential",
                    "Say 'I can't remember' to avoid conflict",
                    "Check if Mrs. Jones would mind first"
                ],
                "correct": 1,
                "explanation": """
**CORRECT: Refuse to discuss - it's confidential**

Caldicott Principle 4: Need-to-know basis only!

Your colleague has NO clinical need to know Mrs. Jones' information.
This is a breach of confidentiality if you share.

Even saying "I can't remember" is wrong - you should educate your colleague about confidentiality.
                """
            },
            {
                "scenario": """
**Scenario 2: Family Phone Call**

A woman phones claiming to be patient John Smith's daughter. She asks when his next appointment is.

You have NOT verified her identity.

**What should you do?**
                """,
                "options": [
                    "Give her the appointment date - she's family",
                    "Refuse until you verify her identity",
                    "Ask her to call back when John is there",
                    "Give partial information only"
                ],
                "correct": 1,
                "explanation": """
**CORRECT: Refuse until you verify her identity**

NEVER give patient information without:
1. Verifying the caller's identity
2. Checking patient has consented to share with them
3. Confirming they have a legitimate need to know

Even appointment dates are confidential!
The fact someone is a patient is confidential information.

Proper response: "For confidentiality, I need to verify your identity and check Mr. Smith's consent."
                """
            },
            {
                "scenario": """
**Scenario 3: The Left-Open Computer**

You're called away urgently from your computer. The patient record is still on screen.

**What should you do?**
                """,
                "options": [
                    "Leave it - you'll only be 2 minutes",
                    "Ask colleague to watch your screen",
                    "Lock your screen immediately",
                    "Minimize the window"
                ],
                "correct": 2,
                "explanation": """
**CORRECT: Lock your screen immediately**

ALWAYS lock your screen when leaving your desk (even for 10 seconds!)

- Press Windows + L (lock screen)
- This prevents unauthorized access
- It's a requirement of NHS Information Security policy

Minimizing is NOT enough - anyone can open the window.
Asking someone to watch is NOT secure.

**If you don't lock your screen and there's a breach, YOU are responsible!**
                """
            }
        ]
    }
}

# Assessment questions (must score 100%)
IG_ASSESSMENT = [
    {
        "q": "What is the legal basis for NHS to process patient data?",
        "opts": ["Patient consent only", "Public task (statutory duty)", "Commercial interest", "No legal basis needed"],
        "ans": 1,
        "exp": "NHS processes data under 'public task' - our statutory duty to provide healthcare."
    },
    {
        "q": "Can you access your own medical record on the NHS system?",
        "opts": ["Yes - it's your data", "No - this is a breach", "Yes - if supervisor approves", "Only for emergencies"],
        "ans": 1,
        "exp": "NO! Accessing your own record on NHS systems is a BREACH. Use official channels (GP, Subject Access Request)."
    },
    {
        "q": "A journalist asks for patient statistics. Can you share anonymised data?",
        "opts": ["Yes - it's anonymised", "No - never share with media", "Yes - with manager approval", "Only if patient consents"],
        "ans": 2,
        "exp": "You MUST get manager/Caldicott Guardian approval before sharing ANY data externally, even anonymised."
    },
    {
        "q": "What should you do if you suspect a data breach?",
        "opts": ["Ignore if minor", "Report immediately to IG team", "Fix it yourself", "Wait to see if anyone notices"],
        "ans": 1,
        "exp": "Report ALL suspected breaches immediately to your Information Governance team. They must be reported to ICO within 72 hours if serious."
    },
    {
        "q": "Can you email patient information to a GP surgery?",
        "opts": ["Yes - always", "Yes - if using NHSmail", "No - never email patient data", "Yes - if encrypted"],
        "ans": 1,
        "exp": "Patient information can ONLY be emailed using secure NHS email (NHSmail to NHSmail) or encrypted email."
    }
]

# Data breach procedure
DATA_BREACH_PROCEDURE = """
**WHAT TO DO IF YOU SUSPECT A DATA BREACH**

**STEP 1: STOP & SECURE** ⚠️
- Don't make it worse
- Contain the breach immediately
- Lock computers, retrieve documents, stop email

**STEP 2: REPORT IMMEDIATELY** 📞
- Tell your line manager NOW
- Contact Information Governance team
- Complete incident form

**STEP 3: DOCUMENT EVERYTHING** 📝
- What happened?
- What data was involved?
- Who was affected?
- When did it occur?
- How did you discover it?

**STEP 4: FOLLOW INSTRUCTIONS** ✅
- IG team will investigate
- May need to notify ICO (72 hours)
- May need to notify patients
- Lessons learned review

**EXAMPLES OF DATA BREACHES:**
❌ Emailing patient list to wrong person
❌ Leaving patient notes on train
❌ Discussing patients in public
❌ Posting patient info on social media
❌ Unauthorized access to records
❌ Lost/stolen laptop with patient data
❌ Sending letter to wrong address

**REMEMBER: Report even if unsure - better safe than sorry!**
"""

__all__ = ['IG_TRAINING_MODULES', 'IG_ASSESSMENT', 'DATA_BREACH_PROCEDURE']
