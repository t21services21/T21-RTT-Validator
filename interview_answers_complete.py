"""
COMPLETE INTERVIEW ANSWERS DATABASE
Comprehensive answers for ALL interview questions
GUARANTEED: Every question gets a full, professional answer!
"""

def get_complete_answer(question, category):
    """
    Get a complete, professional answer for ANY interview question
    NEVER returns empty - ALWAYS returns a full answer
    """
    
    question_lower = question.lower()
    
    # Build comprehensive answer database
    # Each answer is complete, professional, and ready to use
    
    answers_database = {
        
        # INTRODUCTION QUESTIONS
        'tell_me_about_yourself': {
            'answer': """Good morning/afternoon. My name is [Your Name] and I have [X years] of experience in [NHS/healthcare administration/RTT validation/care work/teaching].

Currently, I work at [Current Organization] as a [Current Role], where I'm responsible for [key responsibilities].

I have particular expertise in [mention 2-3 key skills from job description], and I'm passionate about [patient care/education/service excellence].

I'm excited about this opportunity because [specific reason - growth opportunity/organization's reputation/career alignment].""",
            'tips': ["Keep it to 60-90 seconds", "Focus on relevant experience only", "End with why you're interested"]
        },
        
        # RTT QUESTIONS
        'what_is_rtt': {
            'answer': """The RTT pathway is the patient journey from referral to first definitive treatment, with an 18-week constitutional standard.

It's important because:
1. **Patient care** - ensures timely treatment and better outcomes
2. **Trust performance** - monitored nationally
3. **Legal compliance** - constitutional right under NHS Constitution

The pathway starts when GP referral is received (Code 10) or consultant decides to treat (Code 20), and stops when patient receives first treatment (Code 30) or declines treatment (Code 31/32).

Accurate tracking prevents breaches and ensures patients aren't delayed.""",
            'tips': ["Show clinical AND admin understanding", "Mention patient care first", "Know RTT codes"]
        },
        
        'rtt_clock_stops': {
            'answer': """**Main Clock Stops:**
- Code 30: First definitive treatment
- Code 31: Patient declined before offer  
- Code 32: Patient declined after offer
- Code 33: Patient DNA'd and removed

**Clock Pauses:**
- Active Monitoring (Codes 90-92): Patient not ready
- Patient-led delays: Patient requests postponement  
- Capacity constraints: Hospital can't provide treatment

Key difference: Stops END the pathway, Pauses SUSPEND it temporarily.""",
            'tips': ["Know stops vs pauses", "Understand when each applies", "Mention documentation"]
        },
        
        'handle_18_week_breach': {
            'answer': """**Immediate Actions:**
1. Escalate to line manager and booking team
2. Document breach reason (capacity/DNA/clinical/admin)
3. Mark patient as urgent priority

**Investigation:**
4. Root cause analysis - Why did it occur?
5. Implement preventive measures
6. Complete breach report for RTT Manager

**Key Principle:** Learn from breaches to prevent future ones, and prioritize affected patient for treatment.""",
            'tips': ["Show systematic approach", "Demonstrate reporting knowledge", "Focus on prevention"]
        },
        
        # HEALTHCARE QUESTIONS
        'hca_role': {
            'answer': """Healthcare Assistant role involves:

**Personal Care:**
- Washing, dressing, toileting
- Meals and nutrition support
- Mobility assistance

**Clinical Tasks (supervised):**
- Recording vital signs
- Monitoring intake/output
- Specimen collection

**Emotional Support:**
- Companionship and reassurance
- Maintaining dignity
- Supporting families

Most important: Compassion, communication, teamwork, and observation skills.""",
            'tips': ["Emphasize compassion", "Show holistic understanding", "Mention teamwork"]
        },
        
        'vital_signs': {
            'answer': """**Key Observations:**

**Vital Signs:**
- Temperature: 36.5-37.5°C
- Blood Pressure: ~120/80
- Pulse: 60-100 bpm
- Respirations: 12-20/min
- O2 Saturation: 95-100%

**Physical:** Skin color, mobility, pain levels
**Behavioral:** Consciousness, confusion, appetite
**Emotional:** Mood, communication ability

**Most Important:** Report ANY concerns immediately to qualified staff.""",
            'tips': ["Know normal ranges", "Emphasize reporting", "Show holistic approach"]
        },
        
        # SAFEGUARDING
        'what_is_safeguarding': {
            'answer': """Safeguarding means protecting children, young people, and vulnerable adults from harm, abuse, and neglect.

**It's Important Because:**
- Legal duty - everyone's responsibility
- Prevents serious harm through early intervention
- Protects those who can't protect themselves

**Types of Abuse:** Physical, emotional, sexual, neglect, financial

**If I Have Concerns:**
- Report immediately to Designated Safeguarding Lead
- Record facts only
- Don't investigate myself
- Keep confidential

Better to raise a concern that's nothing, than stay silent when someone's being harmed.""",
            'tips': ["Know abuse types", "Understand reporting procedures", "Emphasize everyone's responsibility"]
        },
        
        # TEACHING ASSISTANT
        'ta_role': {
            'answer': """Teaching Assistant supports both teachers and pupils:

**1. Learning Support:**
- Small groups/individual pupils
- Reinforcing lessons
- Adapting resources
- Supporting SEND pupils

**2. Classroom Support:**
- Preparing materials
- Managing displays
- Supervising breaks

**3. Pastoral Care:**
- Building relationships
- Supporting wellbeing
- Encouraging positive behavior

Most important: Patience, teamwork, safeguarding, and confidentiality.""",
            'tips': ["Show academic AND pastoral understanding", "Mention SEND", "Emphasize safeguarding"]
        },
        
        'support_send': {
            'answer': """**Supporting SEND Pupils:**

**1. Understand Needs:** Read EHCP, talk to SENCO/teacher/parents

**2. Adapt Learning:**
- Break tasks into smaller steps
- Use visual aids
- Provide extra time
- Multi-sensory approaches

**3. Create Supportive Environment:**
- Predictable routines
- Quiet workspace if needed
- Positive reinforcement

**4. Communication:**
- Check understanding frequently
- Use preferred communication method
- Be patient

Every SEND child is unique - stay flexible and maintain dignity.""",
            'tips': ["Know SEND terminology", "Give specific strategies", "Emphasize individuality"]
        },
        
        # CUSTOMER SERVICE
        'excellent_customer_service': {
            'answer': """Excellent customer service means:

**1. Professionalism:** Polite, respectful, taking ownership
**2. Responsiveness:** Quick acknowledgment, prompt responses
**3. Understanding:** Active listening, showing empathy
**4. Problem-Solving:** Finding solutions, not excuses
**5. Clear Communication:** No jargon, keeping informed
**6. Consistency:** Every customer gets high standard

In healthcare: Customer service = Patient experience. Professional, caring approach reduces anxiety and improves outcomes.""",
            'tips': ["Give specific examples", "Show empathy", "Demonstrate problem-solving"]
        },
        
        # MOTIVATION
        'why_work_here': {
            'answer': """Why I want to work for [Organization]:

**1. Reputation:** Impressed by [specific achievement/rating]. Your commitment to [value] aligns with my professional values.

**2. Development:** Attracted to [training/progression opportunities]. Keen to develop skills in [relevant area].

**3. Excellence:** Your [patient satisfaction/Ofsted rating/staff retention] demonstrates quality commitment.

**4. Culture:** Supportive team environment is important to me.

**5. Impact:** Motivated by [patient care/student achievement], and this organization offers opportunity to make real difference.

**Tip:** Research their website, CQC/Ofsted, social media, news - then reference SPECIFIC findings!""",
            'tips': ["Research beforehand - be specific!", "Align your values", "Show enthusiasm"]
        },
        
        # COMPETENCY QUESTIONS (STAR METHOD)
        'teamwork_star': {
            'answer': """**STAR Method:**

**Situation:** Department faced backlog of 300 referrals with two team members sick.

**Task:** Clear backlog in 2 weeks while maintaining daily workload, ensuring no breaches.

**Action:** I:
- Coordinated the effort
- Created shared tracker
- Divided work by strengths
- Held daily 10-min huddles
- Supported struggling colleagues
- Stayed late when needed

**Result:** Cleared in 12 days, zero breaches, positive morale, manager praised approach.""",
            'tips': ["ALWAYS use STAR", "Use specific numbers", "Focus on YOUR actions", "Show leadership"]
        },
        
        # SCENARIO QUESTIONS
        'angry_customer': {
            'answer': """**STAR Method:**

**Situation:** Patient arrived for cancelled appointment (system error), became very angry.

**Task:** De-escalate, resolve issue, maintain professional environment.

**Action:** I:
1. Stayed calm
2. Listened without interrupting
3. Acknowledged feelings: "I understand this is frustrating"
4. Moved to private area
5. Investigated error
6. Offered next-day appointment
7. Followed up by phone

**Result:** Patient calmed down, accepted appointment, later wrote positive comment.

**Key Principles:** Don't take personally, stay calm, listen first, apologize, focus on solutions.""",
            'tips': ["Use STAR method", "Show emotional intelligence", "Demonstrate de-escalation"]
        },
        
        'anxious_patient': {
            'answer': """**Supporting Anxious/Distressed Patient:**

1. **Approach Calmly:** Gentle tone, get to eye level
2. **Listen and Validate:** "I can see you're upset"
3. **Create Safe Environment:** Quiet area, reduce stimulation
4. **Use Reassurance:** Explain what's happening, give control
5. **Practical Support:** Water/tissues, call family if wanted
6. **Stay With Them:** Don't leave alone
7. **Report:** Tell qualified staff, document

**Key Point:** Empathy and presence are powerful. Sometimes people just need to feel heard.""",
            'tips': ["Show empathy", "Demonstrate calm approach", "Know when to escalate"]
        },
        
        'refuses_medication': {
            'answer': """**If Patient Refuses Medication:**

1. **Stay Calm:** Never force
2. **Explore Why:** Ask gently what concerns them
3. **Provide Information:** Explain purpose in simple language
4. **Offer Alternatives:** Different form? With food? Different time?
5. **Report IMMEDIATELY:** Nurse/doctor must assess
6. **Document:** Record refusal, reason, time reported

**Do NOT:** Hide in food (illegal!), lie, make guilty, give up

**Important:** Patients can refuse (if have capacity), but I must always report to qualified staff who will assess.""",
            'tips': ["Never force", "Always report", "Show understanding of rights", "Know when urgent"]
        },
        
        'suspected_abuse': {
            'answer': """**If I Suspected Abuse:**

**1. Ensure Safety:** If immediate danger, call 999
**2. Report to DSL:** SAME DAY to Designated Safeguarding Lead
**3. Record Everything:** Facts only, what I saw/heard, when/where
**4. Do NOT:** Investigate, ask leading questions, promise confidentiality, tell alleged abuser

**Documentation:** "Bruising on arm in hand shape" NOT "I think they were hit"

**Key Principle:** Report concerns immediately. Not my job to prove it - that's social services' role.""",
            'tips': ["Immediate reporting", "Facts only", "Know who DSL is", "Never investigate"]
        },
        
        # CLOSING QUESTIONS
        'questions_for_us': {
            'answer': """Yes, I have several questions:

1. What does a typical day look like in this role?
2. What are the main challenges the team currently faces?
3. How is success measured in this position?
4. What training and development opportunities are available?
5. What do you enjoy most about working here?
6. What are the next steps in the interview process?""",
            'tips': ["ALWAYS have 3-5 questions", "Shows genuine interest", "Don't ask salary first time"]
        },
        
        'strengths_weaknesses': {
            'answer': """**My Strengths:**
1. **Attention to Detail:** Critical for data validation - I catch errors others miss
2. **Communication:** Good at explaining complex info simply
3. **Calm Under Pressure:** Stay focused when busy

**My Weakness:**
I can be **too detail-focused** sometimes. For example, I once spent too long perfecting a report when "good enough" would have been fine. I'm learning to balance quality with efficiency - asking "Is this good enough for the purpose?" before going deeper.

**Key:** Turn weakness into positive - show self-awareness and how you're improving.""",
            'tips': ["Give real strengths with examples", "Weakness should be genuine but not critical", "Show how you're improving"]
        },
        
        # MEDICAL SECRETARY QUESTIONS
        'audio_typing': {
            'answer': """**My Audio Typing Experience:**

I have [X years] experience with audio typing and medical correspondence:

**Audio Typing Skills:**
- Typing speed: [X] words per minute with 98%+ accuracy
- Experience with digital dictation systems (e.g., Winscribe, BigHand, Olympus)
- Familiar with foot pedal controls for efficient typing
- Can handle difficult accents and poor audio quality

**Medical Correspondence:**
- Clinic letters to GPs
- Discharge summaries
- Outpatient appointment letters
- Referral letters to other consultants
- Patient information letters

**Medical Terminology:**
- Familiar with medical terminology across specialties
- Can spell complex medical terms correctly
- Understand abbreviations (e.g., Hx, Dx, Rx, O/E)
- Use medical dictionaries when needed

**Quality Standards:**
- Always proofread before sending
- Check patient details are correct
- Ensure letters sent within 24-48 hours
- Follow NHS correspondence guidelines

**Example:** In my previous role, I typed an average of 15-20 clinic letters per day with a 24-hour turnaround, maintaining high accuracy even with complex cardiology terminology.""",
            'tips': ["Give your actual typing speed if known", "Mention specific systems you've used", "Emphasize accuracy and speed"]
        },
        
        'diary_management': {
            'answer': """**Managing Consultant's Diary and Clinic Coordination:**

**Diary Management:**
1. **Prioritization:** Urgent appointments, MDTs, admin time, leave
2. **Forward Planning:** Book meetings 2-3 months in advance where possible
3. **Buffer Time:** Leave gaps between appointments for overruns
4. **Clash Management:** Check for double-bookings daily
5. **Reminders:** Send consultant reminders day before

**Clinic Coordination:**
1. **Booking Clinics:**
   - Book clinic slots in PAS system
   - Ensure room availability
   - Coordinate with nursing staff
   - Arrange equipment if needed

2. **Patient Lists:**
   - Prepare clinic lists 2-3 days in advance
   - Print patient notes/test results
   - Flag urgent cases
   - Check DNAs and cancellations

3. **Follow-up:**
   - Chase missing patients
   - Rebook DNAs
   - Send outcome letters after clinic

**Communication:**
- Liaise with other consultants' secretaries
- Coordinate cross-specialty appointments
- Inform patients of changes promptly

**Example:** I managed a busy cardiology consultant's diary with 3 clinics per week, 2 theatre sessions, and weekly MDTs. I used Outlook calendar and set up color-coding: Red=Urgent, Blue=Clinic, Green=Admin. This prevented double-bookings and kept consultant on schedule.""",
            'tips': ["Show systematic approach", "Mention specific tools used (Outlook, etc.)", "Demonstrate organization skills"]
        },
        
        'medical_terminology': {
            'answer': """**My Medical Terminology Experience:**

**How I Developed Knowledge:**
- [Previous role] exposed me to [specialty] terminology
- Completed medical terminology course/training
- Use medical dictionaries and online resources
- Ask clinicians when unsure

**Specialties I'm Familiar With:**
- [List relevant specialties, e.g., Cardiology, Respiratory, etc.]

**Common Terms I Know:**
- **Procedures:** Angioplasty, colonoscopy, arthroscopy, etc.
- **Conditions:** Hypertension, COPD, diabetes, etc.
- **Abbreviations:** Hx (history), Dx (diagnosis), Rx (treatment), O/E (on examination)
- **Body Systems:** Cardiovascular, respiratory, gastrointestinal, etc.

**Anatomical Terms:**
- Understanding of body parts and systems
- Medical prefixes/suffixes (e.g., cardio = heart, -itis = inflammation)

**How I Handle Unknown Terms:**
1. Look it up in medical dictionary
2. Ask consultant or clinical staff
3. Make a personal glossary for future reference
4. Never guess - always verify

**Example:** When I started in cardiology, I created a glossary of terms like "myocardial infarction," "arrhythmia," "echocardiogram." Within 3 months, I could type clinic letters without constantly checking terminology.

**Key Point:** Medical terminology knowledge grows with experience - I'm committed to continuous learning and always verify if unsure.""",
            'tips': ["Be honest about your level", "Show willingness to learn", "Mention any training", "Never guess medical terms!"]
        },
        
        'conflicting_priorities': {
            'answer': """**STAR Method:**

**Situation:** In my previous role, I supported 3 consultants. One day, all three needed urgent tasks completed: Consultant A needed clinic list prepared for afternoon clinic, Consultant B needed urgent referral letter typed, Consultant C needed theatre list finalized.

**Task:** Complete all three tasks before their deadlines while maintaining quality.

**Action:** I:
1. **Assessed Urgency:** Ranked by deadline and patient impact
   - Theatre list (highest - patients arriving next morning)
   - Urgent referral (2-week wait patient)
   - Clinic list (clinic at 2pm, currently 10am)

2. **Communicated:** Told each consultant my plan and expected completion times

3. **Worked Efficiently:**
   - Theatre list: 30 minutes (highest priority)
   - Urgent referral: 20 minutes (time-sensitive)
   - Clinic list: 40 minutes (had time before clinic)

4. **Managed Interruptions:** Put phone on divert during critical tasks

5. **Quality Checked:** Still proofread each document despite time pressure

**Result:** 
- All three tasks completed before deadlines
- No errors in any document
- All three consultants thanked me for managing well under pressure
- This became my standard approach for conflicting priorities

**Key Principles:**
- Assess urgency and patient impact first
- Communicate with stakeholders
- Stay calm and focused
- Never sacrifice quality for speed""",
            'tips': ["Use STAR method", "Show diplomatic communication", "Demonstrate prioritization skills", "Stay calm"]
        },
        
        'patient_correspondence': {
            'answer': """**Patient Correspondence Experience:**

**Types of Letters I've Produced:**

1. **Outpatient Clinic Letters:**
   - Sent to GPs after appointments
   - Include diagnosis, treatment plan, follow-up
   - Typed from consultant's dictation
   - 24-48 hour turnaround

2. **Discharge Summaries:**
   - Sent when patient discharged from hospital
   - Include admission reason, treatment given, medications, follow-up
   - Must be accurate - GP relies on this information

3. **Appointment Letters:**
   - First appointment letters (with directions, what to bring)
   - Follow-up appointment letters
   - Cancellation/rearrangement letters

4. **Follow-up Letters:**
   - Test results letters
   - Treatment outcome letters
   - Referral confirmation letters

**Quality Standards I Follow:**

1. **Accuracy:**
   - Check patient demographics (name, DOB, NHS number, address)
   - Verify GP details
   - Spell medical terms correctly

2. **Tone:**
   - Professional but empathetic
   - Clear and easy to understand
   - Avoid jargon when writing to patients

3. **Timeliness:**
   - Clinic letters within 24-48 hours
   - Urgent letters same day
   - Test results within deadline

4. **Confidentiality:**
   - Use NHS Mail for patient information
   - Never discuss patient info inappropriately
   - Secure all correspondence

**Example:** In my previous role, I produced average 15-20 letters daily. I implemented a tracking system to ensure no letters were missed. My consultant received compliments from GPs about timely, accurate correspondence.

**Key Point:** Patient correspondence is critical - delays or errors can impact patient care, so I take it very seriously.""",
            'tips': ["Emphasize accuracy", "Mention volume handled", "Show understanding of importance", "Highlight timelines"]
        }
    }
    
    # Match question to answer
    for key, data in answers_database.items():
        if any(keyword in question_lower for keyword in key.split('_')):
            return data
    
    # DEFAULT ANSWER - ALWAYS RETURN SOMETHING
    # Build generic but professional answer based on question type
    return generate_default_answer(question, category)


def generate_default_answer(question, category):
    """Generate a professional answer even if not in database"""
    
    # This ensures EVERY question gets an answer
    return {
        'answer': f"""**Professional Answer Template:**

When answering "{question}", consider this framework:

1. **Understand the Question:**
   - What is the interviewer really asking?
   - What competency are they assessing?

2. **Structure Your Answer:**
   - Start with your main point
   - Provide specific example if possible
   - Explain the impact or result

3. **Key Points to Include:**
   - Relevant experience or knowledge
   - How it relates to this role
   - Your approach or philosophy

4. **If Using STAR Method:**
   - **Situation:** Set the context
   - **Task:** What needed to be done
   - **Action:** What YOU did (be specific)
   - **Result:** What happened (use numbers if possible)

**Remember:** Be honest, be specific, and relate your answer back to the job requirements.""",
        'tips': ["Use STAR method if competency question", "Give specific examples", "Relate to job description"]
    }
