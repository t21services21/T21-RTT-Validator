"""
T21 CAREER SERVICES - Universal Job Interview Preparation Tool
AI-Powered Interview Question Generator for ALL Career Paths

Supports:
- RTT Validation & NHS Admin
- Healthcare Assistant / Care Worker
- Adult Social Care
- Teaching Assistant
- Customer Service
- Business Administration
- IT Support
- And ALL other NHS/Care roles!
"""

import json
from datetime import datetime
import streamlit as st

# OpenAI integration for intelligent answer generation
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

def analyze_job_description(job_title, job_description, company_name=""):
    """
    Analyze job description and generate likely interview questions
    NOW USES GPT-4 TO ACTUALLY READ AND ANALYZE THE JOB DESCRIPTION!
    """
    
    # Try GPT-4 analysis first (intelligent, reads actual job description)
    if OPENAI_AVAILABLE:
        try:
            api_key = st.secrets.get("OPENAI_API_KEY")
            if api_key:
                st.info("📋 Analyzing your job description and generating interview questions...")
                return analyze_with_gpt4(job_title, job_description, company_name, api_key)
            else:
                st.warning("""
                ⚠️ **OpenAI API Key Not Configured**
                
                The system is using a basic keyword-matching fallback method instead of AI.
                
                **To enable GPT-4 AI (MUCH better results):**
                1. Go to Streamlit Cloud Dashboard
                2. Click your app → Settings → Secrets
                3. Add this line:
                   ```
                   OPENAI_API_KEY = "sk-your-key-here"
                   ```
                4. Save and restart app
                
                **Get your API key:** https://platform.openai.com/api-keys
                
                **Without GPT-4:** You'll get basic questions (like you're seeing now)  
                **With GPT-4:** 30-40 expert questions tailored to the job description
                """)
        except Exception as e:
            st.error("❌ Unable to analyze job description. Using basic keyword matching.")
            print(f"AI analysis failed: {e}, falling back to keyword matching")
    
    # Fallback to keyword matching if AI unavailable
    st.warning("""
    ⚠️ **Using basic keyword matching**
    
    Advanced analysis unavailable. Using basic detection.
    Questions will be based on keywords found in the job description.
    """)
    
    # PRIORITY KEYWORDS - Only match if they're STRONG indicators
    priority_keywords = {
        'rtt': ['referral to treatment', 'RTT pathway', 'RTT code', 'RTT clock', '18-week', '18 week'],
        'medical_secretary': ['medical secretary', 'secretary to consultant', 'audio typing', 'clinic correspondence'],
        'healthcare_assistant': ['healthcare assistant', 'HCA', 'care assistant role', 'nursing duties'],
        'teaching_assistant': ['teaching assistant', 'classroom support', 'supporting pupils'],
        'validation': ['validation officer', 'data validation', 'RTT validation', 'quality assurance'],
    }
    
    # SECONDARY KEYWORDS - Only include if primary role identified
    secondary_keywords = {
        'pas': ['PAS system', 'patient administration system', 'PAS experience'],
        'typing': ['audio typing', 'typing speed', 'transcription'],
        'diary': ['diary management', 'calendar management', 'booking clinics'],
        'admin': ['administrative', 'clerical', 'office duties'],
    }
    
    # Find PRIMARY role first
    found_skills = []
    primary_role = None
    
    job_lower = job_description.lower()
    
    # Check for primary role
    for role, terms in priority_keywords.items():
        for term in terms:
            if term.lower() in job_lower:
                found_skills.append(role)
                primary_role = role
                break
        if primary_role:
            break
    
    # Only add secondary skills if they're relevant to primary role
    if primary_role:
        for skill, terms in secondary_keywords.items():
            for term in terms:
                if term.lower() in job_lower:
                    found_skills.append(skill)
                    break
    
    # If NO clear role found, show generic message
    if not found_skills:
        st.error("""
        ❌ **Could not identify specific role from job description**
        
        GPT-4 failed and basic keyword matching found no clear job role.
        
        **To get accurate interview questions:**
        1. Configure OpenAI API key in Streamlit secrets
        2. OR provide a clearer job description with role title
        """)
        return None
    
    questions = generate_questions(job_title, found_skills, job_description)
    prep_tips = generate_prep_tips(job_title, found_skills)
    
    from interview_answers_complete import get_complete_answer
    example_answers = []
    for q in questions:
        answer_data = get_complete_answer(q['question'], q['category'])
        example_answers.append({
            'question': q['question'],
            'example_answer': answer_data['answer'],
            'tips': answer_data['tips']
        })
    
    return {
        'job_title': job_title,
        'company_name': company_name,
        'identified_skills': found_skills,
        'interview_questions': questions,
        'preparation_tips': prep_tips,
        'example_answers': example_answers,
        'research_areas': generate_research_areas(company_name, job_title)
    }


def analyze_with_gpt4(job_title, job_description, company_name, api_key):
    """
    Use GPT-4 to INTELLIGENTLY analyze job description and generate questions + answers
    This is what we SHOULD be using!
    """
    from openai import OpenAI
    
    try:
        client = OpenAI(
            api_key=api_key,
            timeout=30.0  # 30 second timeout for faster response
        )
    except Exception as e:
        st.error(f"❌ Failed to initialize OpenAI client: {e}")
        raise
    
    # COMPREHENSIVE PROMPT - Generate 40-50+ job-specific questions!
    prompt = f"""You are preparing a candidate for a job interview. Analyze the job description and generate 15-20 CATEGORIES with 3-4 questions EACH (total: 45-80 questions).

JOB TITLE: {job_title}
ORGANIZATION: {company_name}

JOB DESCRIPTION:
{job_description[:2000]}

REQUIREMENTS:
1. Generate 15-20 CATEGORIES of questions
2. For EACH category, generate 3-4 SPECIFIC questions (not just 1!)
3. Total questions: 45-80 (15 categories × 3-4 questions each)
4. All questions must be SPECIFIC to this job description
5. Include categories like:
   - Technical questions (about systems/skills mentioned - 3-4 questions)
   - Competency-based (STAR method scenarios - 3-4 questions)
   - Scenario questions (realistic situations - 3-4 questions)
   - Motivation questions (why this role/organization - 3-4 questions)
   - Closing questions (strengths, weaknesses, etc. - 3-4 questions)

6. For EACH question provide:
   - Exact question text
   - Why they ask it
   - Likelihood percentage
   - Professional 100-150 word answer
   - 3-5 practical tips

Return ONLY valid JSON (no markdown):

{{
  "questions": [
    {{
      "category": "Technical - Medical Terminology",
      "question": "Can you explain your experience with medical terminology?",
      "why_asked": "Tests knowledge of core skill",
      "likelihood": "95%",
      "answer": "Professional answer here...",
      "tips": ["Tip 1", "Tip 2", "Tip 3"]
    }},
    {{
      "category": "Technical - Medical Terminology",
      "question": "How do you ensure accuracy when using medical terms in correspondence?",
      "why_asked": "Tests attention to detail",
      "likelihood": "90%",
      "answer": "Professional answer here...",
      "tips": ["Tip 1", "Tip 2", "Tip 3"]
    }},
    {{
      "category": "Technical - Medical Terminology",
      "question": "Give an example of a complex medical term you've used in your work.",
      "why_asked": "Tests practical application",
      "likelihood": "85%",
      "answer": "Professional answer here...",
      "tips": ["Tip 1", "Tip 2", "Tip 3"]
    }},
    ... (continue with 3-4 questions per category, 15-20 categories total = 45-80 questions)
  ]
}}

CRITICAL: Generate 3-4 questions per category! Don't just generate 1 question per category. Total output should be 45-80 questions."""

    try:
        st.info("⚙️ Generating personalized interview questions...")
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an experienced HR professional helping candidates prepare for job interviews. Provide comprehensive, professional interview preparation based on job descriptions. Return ONLY valid JSON, no markdown formatting."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=16000,  # For 45-80 questions with full answers (increased from 8000)
            response_format={"type": "json_object"}  # Force JSON output (no markdown)
        )
        
        # Success message will be shown after formatting is complete
        
        import json
        raw_content = response.choices[0].message.content
        
        # Strip markdown code blocks if present
        raw_content = raw_content.strip()
        
        # Remove markdown code fence
        if raw_content.startswith('```json'):
            raw_content = raw_content[7:].lstrip()
        elif raw_content.startswith('```'):
            raw_content = raw_content[3:].lstrip()
        
        # Remove closing fence
        if raw_content.endswith('```'):
            raw_content = raw_content[:-3].rstrip()
        
        # Final cleanup
        raw_content = raw_content.strip()
        
        try:
            result = json.loads(raw_content)
        except json.JSONDecodeError as e:
            st.error("""
            ❌ **Unable to Generate Interview Prep Pack**
            
            There was an issue processing your job description. Please try again or contact support if the issue persists.
            """)
            raise
        
        # Format for our system
        questions = []
        example_answers = []
        
        for q in result.get('questions', []):
            questions.append({
                'category': q.get('category', 'General'),
                'question': q.get('question', ''),
                'why_asked': q.get('why_asked', ''),
                'likelihood': q.get('likelihood', '80%')
            })
            
            # Build comprehensive answer with tips AND red flags
            answer_text = q.get('answer', '')
            
            # Add red flags section if provided
            red_flags = q.get('red_flags', [])
            if red_flags:
                answer_text += "\n\n**❌ RED FLAGS TO AVOID:**\n"
                for flag in red_flags:
                    answer_text += f"- {flag}\n"
            
            example_answers.append({
                'question': q.get('question', ''),
                'example_answer': answer_text,
                'tips': q.get('tips', [])
            })
        
        # Extract comprehensive prep tips from GPT-4 response
        prep_tips = result.get('prep_tips', {
            'before_interview': [
                f"Research {company_name} thoroughly - mission, values, recent news, CQC rating",
                "Review the job description and match your experience to each requirement",
                "Prepare STAR method examples for competency questions",
                "Practice answering questions out loud",
                "Prepare 10-12 thoughtful questions to ask them",
                "Plan your route and arrival time (10-15 mins early)",
                "Choose professional attire appropriate for the role"
            ],
            'on_the_day': [
                "Arrive 10-15 minutes early (not too early!)",
                "Bring: CV copies, notebook, pen, certificates, portfolio",
                "Dress professionally (smart business attire)",
                "Turn off mobile phone completely",
                "Greet everyone professionally with a smile",
                "Make eye contact and use confident body language",
                "Listen carefully to questions, take a moment to think before answering"
            ],
            'technical_prep': [
                "Review all key skills mentioned in job description",
                "Prepare examples demonstrating each required skill",
                "Know the terminology for this role",
                "Research organization's mission, vision, and values",
                "Understand what makes this organization unique",
                "Know their recent achievements and challenges"
            ],
            'key_documents': [
                "Up-to-date CV/resume (multiple copies)",
                "Copies of relevant certificates",
                "Portfolio of work (if applicable)",
                "References contact details",
                "Right to work documents",
                "Notepad and professional pen"
            ]
        })
        
        # Extract organization research from GPT-4
        organization_research = result.get('organization_research', {})
        
        # Extract interview etiquette from GPT-4
        interview_etiquette = result.get('interview_etiquette', {})
        
        # Extract questions to ask them from GPT-4
        questions_to_ask = result.get('questions_to_ask', [])
        
        return {
            'job_title': job_title,
            'company_name': company_name,
            'identified_skills': [],  # GPT-4 handles this
            'interview_questions': questions,
            'preparation_tips': prep_tips,
            'example_answers': example_answers,
            'research_areas': generate_research_areas(company_name, job_title),
            'organization_research': organization_research,  # Mission, vision, values, etc.
            'interview_etiquette': interview_etiquette,  # Opening, during, closing interview
            'questions_to_ask': questions_to_ask,  # Smart questions for them
            'post_interview': result.get('post_interview', {}),  # Thank-you email, follow-up
            'salary_discussion': result.get('salary_discussion', {})  # How to handle salary talk
        }
        
    except Exception as e:
        st.error(f"""
        ❌ **GPT-4 Error Detected!**
        
        **Error Type:** {type(e).__name__}
        **Error Message:** {str(e)}
        
        **Falling back to basic keyword matching...**
        
        **Possible causes:**
        1. API key invalid or expired
        2. OpenAI rate limit exceeded
        3. Network/connection issue
        4. JSON parsing error
        
        **Check your OpenAI account:** https://platform.openai.com/usage
        """)
        import traceback
        print(f"GPT-4 FULL ERROR:")
        print(traceback.format_exc())
        raise  # Re-raise to fallback to keyword matching


def generate_questions(job_title, skills, job_desc):
    """Generate likely interview questions"""
    
    questions = []
    
    # Standard opening questions (always asked)
    questions.extend([
        {
            'category': 'Introduction',
            'question': 'Tell me about yourself and your experience',
            'why_asked': 'Standard opening to assess communication skills and background',
            'likelihood': '100%'
        },
        {
            'category': 'Motivation',
            'question': 'Why do you want to work for our organisation?',
            'why_asked': 'Tests your research and genuine interest',
            'likelihood': '95%'
        },
        {
            'category': 'Motivation',
            'question': 'Why are you interested in this particular role?',
            'why_asked': 'Assesses fit for position',
            'likelihood': '90%'
        }
    ])
    
    # RTT-specific questions
    if 'rtt' in skills:
        questions.extend([
            {
                'category': 'Technical - RTT',
                'question': 'What is the RTT pathway and why is it important?',
                'why_asked': 'Tests fundamental RTT knowledge',
                'likelihood': '100%'
            },
            {
                'category': 'Technical - RTT',
                'question': 'What are the main RTT clock stops and pauses?',
                'why_asked': 'Assesses practical RTT understanding',
                'likelihood': '95%'
            },
            {
                'category': 'Technical - RTT',
                'question': 'How would you handle an 18-week breach?',
                'why_asked': 'Tests problem-solving under pressure',
                'likelihood': '90%'
            },
            {
                'category': 'Scenario - RTT',
                'question': 'A patient has been waiting 16 weeks with no TCI date. What actions would you take?',
                'why_asked': 'Practical scenario to test knowledge application',
                'likelihood': '85%'
            },
            {
                'category': 'Technical - RTT',
                'question': 'Explain the difference between Code 10, Code 20, and Code 30',
                'why_asked': 'Tests detailed RTT coding knowledge',
                'likelihood': '80%'
            }
        ])
    
    # PAS/Admin questions
    if 'pas' in skills:
        questions.extend([
            {
                'category': 'Technical - PAS',
                'question': 'What experience do you have with PAS systems?',
                'why_asked': 'Assesses system familiarity',
                'likelihood': '95%'
            },
            {
                'category': 'Technical - PAS',
                'question': 'How would you ensure data quality in PAS?',
                'why_asked': 'Tests attention to detail',
                'likelihood': '85%'
            }
        ])
    
    # Validation questions
    if 'validation' in skills:
        questions.extend([
            {
                'category': 'Technical - Validation',
                'question': 'What is your approach to validation and auditing?',
                'why_asked': 'Tests systematic thinking',
                'likelihood': '90%'
            },
            {
                'category': 'Scenario - Validation',
                'question': 'You find multiple errors in a colleague\'s work. How do you handle it?',
                'why_asked': 'Assesses diplomacy and professionalism',
                'likelihood': '75%'
            }
        ])
    
    # Competency-based questions (common for all NHS roles)
    questions.extend([
        {
            'category': 'Competency - Teamwork',
            'question': 'Describe a time when you worked effectively as part of a team',
            'why_asked': 'Assesses collaboration skills (STAR method expected)',
            'likelihood': '90%'
        },
        {
            'category': 'Competency - Problem Solving',
            'question': 'Tell me about a challenging situation you faced and how you resolved it',
            'why_asked': 'Tests resilience and problem-solving',
            'likelihood': '85%'
        },
        {
            'category': 'Competency - Time Management',
            'question': 'How do you prioritize your workload when under pressure?',
            'why_asked': 'Assesses organizational skills',
            'likelihood': '80%'
        },
        {
            'category': 'Competency - Communication',
            'question': 'Give an example of when you had to explain complex information to someone',
            'why_asked': 'Tests communication skills',
            'likelihood': '75%'
        },
        {
            'category': 'Values - NHS',
            'question': 'What do the NHS values mean to you?',
            'why_asked': 'Tests cultural fit and values alignment',
            'likelihood': '70%'
        }
    ])
    
    # Healthcare Assistant / Care Worker questions
    if 'healthcare_assistant' in skills or 'care_work' in skills or 'adult_social_care' in skills:
        questions.extend([
            {
                'category': 'Technical - Healthcare',
                'question': 'What do you understand about the role of a Healthcare Assistant/Care Worker?',
                'why_asked': 'Tests understanding of role responsibilities',
                'likelihood': '100%'
            },
            {
                'category': 'Technical - Healthcare',
                'question': 'What experience do you have in providing personal care?',
                'why_asked': 'Assesses hands-on care experience',
                'likelihood': '95%'
            },
            {
                'category': 'Scenario - Healthcare',
                'question': 'How would you support a patient who is anxious or distressed?',
                'why_asked': 'Tests empathy and patient care skills',
                'likelihood': '90%'
            },
            {
                'category': 'Technical - Healthcare',
                'question': 'What are the key observations you would monitor for a patient?',
                'why_asked': 'Tests clinical knowledge (vital signs, etc.)',
                'likelihood': '85%'
            },
            {
                'category': 'Scenario - Healthcare',
                'question': 'A patient refuses to take their medication. What would you do?',
                'why_asked': 'Tests problem-solving and following procedures',
                'likelihood': '80%'
            }
        ])
    
    # Safeguarding questions (Care roles)
    if 'safeguarding' in skills or 'care_work' in skills or 'adult_social_care' in skills:
        questions.extend([
            {
                'category': 'Safeguarding',
                'question': 'What is safeguarding and why is it important?',
                'why_asked': 'Essential knowledge for care roles',
                'likelihood': '95%'
            },
            {
                'category': 'Scenario - Safeguarding',
                'question': 'If you suspected abuse or neglect, what would you do?',
                'why_asked': 'Tests safeguarding procedures',
                'likelihood': '90%'
            },
            {
                'category': 'Safeguarding',
                'question': 'How would you maintain dignity and respect when providing personal care?',
                'why_asked': 'Tests person-centered care approach',
                'likelihood': '85%'
            }
        ])
    
    # Teaching Assistant questions
    if 'teaching_assistant' in skills or 'education' in skills:
        questions.extend([
            {
                'category': 'Technical - Education',
                'question': 'What do you understand about the role of a Teaching Assistant?',
                'why_asked': 'Tests understanding of TA responsibilities',
                'likelihood': '100%'
            },
            {
                'category': 'Technical - Education',
                'question': 'How would you support a child with special educational needs?',
                'why_asked': 'Tests SEN/SEND knowledge',
                'likelihood': '95%'
            },
            {
                'category': 'Scenario - Education',
                'question': 'How would you manage challenging behavior in the classroom?',
                'why_asked': 'Tests behavior management skills',
                'likelihood': '90%'
            },
            {
                'category': 'Safeguarding - Education',
                'question': 'What safeguarding procedures would you follow if a child disclosed something concerning?',
                'why_asked': 'Essential safeguarding knowledge',
                'likelihood': '95%'
            },
            {
                'category': 'Scenario - Education',
                'question': 'How would you differentiate learning activities for different ability levels?',
                'why_asked': 'Tests understanding of inclusive education',
                'likelihood': '80%'
            }
        ])
    
    # Customer Service questions
    if 'customer_service' in skills or 'reception' in skills:
        questions.extend([
            {
                'category': 'Technical - Customer Service',
                'question': 'What does excellent customer service mean to you?',
                'why_asked': 'Tests customer service philosophy',
                'likelihood': '95%'
            },
            {
                'category': 'Scenario - Customer Service',
                'question': 'How would you deal with an angry or difficult customer/patient?',
                'why_asked': 'Tests conflict resolution skills',
                'likelihood': '95%'
            },
            {
                'category': 'Scenario - Customer Service',
                'question': 'Describe a time when you went above and beyond for a customer',
                'why_asked': 'Tests commitment to service excellence',
                'likelihood': '85%'
            },
            {
                'category': 'Technical - Customer Service',
                'question': 'How do you handle multiple customers/queries at once?',
                'why_asked': 'Tests multitasking and prioritization',
                'likelihood': '80%'
            }
        ])
    
    # Business Administration questions
    if 'admin' in skills or 'business_admin' in skills:
        questions.extend([
            {
                'category': 'Technical - Administration',
                'question': 'What administrative systems and software are you familiar with?',
                'why_asked': 'Assesses technical skills',
                'likelihood': '90%'
            },
            {
                'category': 'Technical - Administration',
                'question': 'How do you ensure accuracy when managing records or data?',
                'why_asked': 'Tests attention to detail',
                'likelihood': '85%'
            },
            {
                'category': 'Scenario - Administration',
                'question': 'How would you organize and prioritize your daily tasks?',
                'why_asked': 'Tests organizational skills',
                'likelihood': '80%'
            }
        ])
    
    # IT Support questions
    if 'it_support' in skills:
        questions.extend([
            {
                'category': 'Technical - IT Support',
                'question': 'Describe your experience with troubleshooting technical issues',
                'why_asked': 'Tests problem-solving ability',
                'likelihood': '95%'
            },
            {
                'category': 'Scenario - IT Support',
                'question': 'How would you explain a technical issue to a non-technical person?',
                'why_asked': 'Tests communication skills',
                'likelihood': '90%'
            }
        ])
    
    # IT Skills (General)
    if 'it_skills' in skills:
        questions.extend([
            {
                'category': 'Technical - IT',
                'question': 'How proficient are you with Excel/Microsoft Office?',
                'why_asked': 'Assesses technical capability',
                'likelihood': '85%'
            }
        ])
    
    # Medical Secretary specific questions
    if 'medical_secretary' in skills or 'typing' in skills or 'diary_management' in skills:
        questions.extend([
            {
                'category': 'Technical - Medical Secretary',
                'question': 'What experience do you have with audio typing and medical correspondence?',
                'why_asked': 'Core skill for medical secretary role',
                'likelihood': '95%'
            },
            {
                'category': 'Technical - Medical Secretary',
                'question': 'How would you manage a consultant\'s diary and coordinate clinic schedules?',
                'why_asked': 'Tests organizational and coordination skills',
                'likelihood': '90%'
            },
            {
                'category': 'Technical - Medical Secretary',
                'question': 'What experience do you have with medical terminology?',
                'why_asked': 'Essential for medical secretary work',
                'likelihood': '90%'
            },
            {
                'category': 'Scenario - Medical Secretary',
                'question': 'How would you handle conflicting priorities from multiple consultants?',
                'why_asked': 'Tests prioritization and diplomacy',
                'likelihood': '85%'
            },
            {
                'category': 'Technical - Medical Secretary',
                'question': 'Describe your experience with patient correspondence and follow-up letters',
                'why_asked': 'Key responsibility in medical secretary roles',
                'likelihood': '85%'
            }
        ])
    
    # Confidentiality / GDPR (important for all roles)
    if 'confidentiality' in skills or 'nhs' in skills or 'care_work' in skills or 'medical_secretary' in skills:
        questions.extend([
            {
                'category': 'Confidentiality',
                'question': 'What do you understand about confidentiality and data protection?',
                'why_asked': 'Tests GDPR/confidentiality awareness',
                'likelihood': '85%'
            },
            {
                'category': 'Scenario - Confidentiality',
                'question': 'A friend asks you about a patient/student you work with. What would you do?',
                'why_asked': 'Tests understanding of confidentiality boundaries',
                'likelihood': '75%'
            }
        ])
    
    # Closing questions (always asked)
    questions.extend([
        {
            'category': 'Closing',
            'question': 'What are your strengths and weaknesses?',
            'why_asked': 'Tests self-awareness',
            'likelihood': '80%'
        },
        {
            'category': 'Closing',
            'question': 'Where do you see yourself in 5 years?',
            'why_asked': 'Assesses ambition and commitment',
            'likelihood': '70%'
        },
        {
            'category': 'Closing',
            'question': 'Do you have any questions for us?',
            'why_asked': 'You MUST have questions prepared!',
            'likelihood': '100%'
        }
    ])
    
    # Sort by likelihood
    questions.sort(key=lambda x: float(x['likelihood'].replace('%', '')), reverse=True)
    
    return questions


def generate_ai_powered_answers(questions, job_title, job_description):
    """Generate intelligent answers for ALL interview questions using GPT-4"""
    
    if not OPENAI_AVAILABLE:
        # Fallback to basic answers
        return generate_example_answers(questions[:5])
    
    try:
        # Get API key
        api_key = st.secrets.get("OPENAI_API_KEY")
        if not api_key:
            return generate_example_answers(questions[:5])
        
        # Initialize OpenAI client
        client = OpenAI(api_key=api_key)
        
        all_answers = []
        
        # Generate answers for top 5 most likely questions (fast generation, most important)
        for q in questions[:5]:
            try:
                # Create prompt for GPT-4
                prompt = f"""You are an expert interview coach helping a candidate prepare for a {job_title} interview.

Job Description:
{job_description[:500]}

Interview Question: {q['question']}
Question Category: {q['category']}
Why it's asked: {q['why_asked']}

Provide an excellent example answer that:
1. Uses STAR method if it's a competency/scenario question (Situation, Task, Action, Result)
2. Is specific and detailed with examples
3. Demonstrates relevant skills and experience
4. Is professional and appropriate for {job_title} role
5. Is 150-250 words long
6. Includes 2-3 practical tips at the end

Format:
**Example Answer:**
[Your detailed answer here]

**Tips:**
- [Tip 1]
- [Tip 2]
- [Tip 3]"""

                # Call GPT-4
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are an expert interview coach with deep knowledge of NHS, healthcare, education, and administrative roles. You provide detailed, professional example answers using STAR method where appropriate."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=500,
                    temperature=0.7
                )
                
                answer_text = response.choices[0].message.content
                
                all_answers.append({
                    'question': q['question'],
                    'category': q['category'],
                    'answer': answer_text
                })
                
            except Exception as e:
                # If individual question fails, continue with next
                print(f"Error generating answer for question: {e}")
                continue
        
        return all_answers
        
    except Exception as e:
        # Fallback to basic answers if GPT-4 fails
        print(f"GPT-4 error in interview prep: {e}")
        return generate_example_answers(questions[:5])


def generate_example_answers(questions):
    """Generate example answers using STAR method where appropriate"""
    
    answers = []
    
    for q in questions:
        if q['category'] == 'Introduction':
            answers.append({
                'question': q['question'],
                'example_answer': """Good morning/afternoon. My name is [Your Name] and I have [X years] of experience in [NHS/healthcare administration/RTT validation].

Currently, I work at [Current Organization] as a [Current Role], where I'm responsible for [key responsibilities].

I have particular expertise in [RTT pathways/PAS systems/data validation], and I'm passionate about ensuring patients receive timely treatment within the 18-week standard.

I'm excited about this opportunity because [specific reason related to job description].""",
                'tips': [
                    "Keep it to 60-90 seconds",
                    "Focus on relevant experience only",
                    "End with why you're interested in THIS role"
                ]
            })
        
        elif 'RTT' in q['category'] and 'pathway' in q['question'].lower():
            answers.append({
                'question': q['question'],
                'example_answer': """The RTT pathway is the patient journey from referral to first definitive treatment, with an 18-week target.

It's important because:
1. Patient care - ensures timely access to treatment
2. Trust performance - monitored nationally
3. Compliance - constitutional right for patients

The pathway starts when a GP referral is received (Code 10) or when a decision to treat is made (Code 20), and continues until first definitive treatment (Code 30) or other clock stop.

Accurate tracking is essential to identify delays and ensure patients aren't breaching the 18-week standard.""",
                'tips': [
                    "Show you understand both clinical AND admin aspects",
                    "Mention patient care first",
                    "Demonstrate knowledge of codes"
                ]
            })
        
        elif q['category'].startswith('Competency'):
            answers.append({
                'question': q['question'],
                'example_answer': """**STAR Method:**

**Situation**: In my previous role at [Trust], we had a backlog of 200 unvalidated referrals.

**Task**: I was tasked with clearing the backlog within 2 weeks while maintaining accuracy.

**Action**: I:
- Prioritized urgent/2WW cases first
- Created a tracking spreadsheet
- Collaborated with the team to divide workload
- Implemented quality checks at each stage

**Result**: We cleared the backlog in 10 days with 98% accuracy, and no patients breached due to validation delays. This process became our standard operating procedure.""",
                'tips': [
                    "ALWAYS use STAR method for competency questions",
                    "Use specific numbers/metrics",
                    "Focus on YOUR actions (not 'we')",
                    "End with positive result"
                ]
            })
        
        elif q['category'] == 'Closing' and 'questions for us' in q['question'].lower():
            answers.append({
                'question': q['question'],
                'example_answer': """Yes, I have a few questions:

1. What does a typical day look like in this role?

2. What are the main challenges the team is currently facing?

3. How does the team measure success in this position?

4. What opportunities are there for professional development and training?

5. What are the next steps in the interview process?""",
                'tips': [
                    "ALWAYS have 3-5 questions prepared",
                    "Shows genuine interest",
                    "Ask about role, team, development",
                    "DON'T ask about salary at first interview"
                ]
            })
    
    return answers


def generate_prep_tips(job_title, skills):
    """Generate specific preparation tips"""
    
    tips = {
        'before_interview': [
            "Research the NHS Trust/Organization thoroughly",
            "Review their CQC rating and recent news",
            "Know their specialties and services",
            "Understand their RTT performance (check NHS England data)",
            "Prepare 3-5 questions to ask them",
            "Review the job description and person specification",
            "Prepare STAR examples for common competencies",
            "Practice answering questions out loud"
        ],
        'on_the_day': [
            "Arrive 10-15 minutes early",
            "Bring: CV copies, notebook, pen, certificates",
            "Dress professionally (smart business attire)",
            "Turn off mobile phone",
            "Greet everyone professionally",
            "Make eye contact and smile",
            "Listen carefully to questions",
            "Take a moment to think before answering"
        ],
        'technical_prep': [],
        'key_documents': [
            "Up-to-date CV/resume",
            "Copies of certificates (RTT training, etc.)",
            "Portfolio of work (if applicable)",
            "References contact details",
            "Right to work documents (if required)"
        ]
    }
    
    # Add technical prep based on skills
    if 'rtt' in skills:
        tips['technical_prep'].extend([
            "Review all 16 RTT codes and their meanings",
            "Know the difference between clock stops and pauses",
            "Understand breach thresholds (18, 26, 52 weeks)",
            "Revise Active Monitoring rules",
            "Know current NHS RTT guidance version"
        ])
    
    if 'pas' in skills:
        tips['technical_prep'].extend([
            "Review PAS system functions",
            "Know appointment booking procedures",
            "Understand waiting list management"
        ])
    
    if 'validation' in skills:
        tips['technical_prep'].extend([
            "Know validation best practices",
            "Understand data quality metrics",
            "Revise audit procedures"
        ])
    
    return tips


def generate_research_areas(company_name, job_title):
    """Generate areas to research about the organization"""
    
    return [
        {
            'area': '🎯 MISSION, VISION & VALUES (CRITICAL!)',
            'what_to_find': [
                "⭐ MISSION: What is the organization's purpose? (Look on their website 'About Us' page)",
                "⭐ VISION: Where do they want to be in the future?",
                "⭐ VALUES: What principles guide them? (e.g., Respect, Dignity, Excellence)",
                "⭐ For NHS: Learn the 6 NHS Core Values (Care, Compassion, Respect, Dignity, Commitment, Communication)",
                "⭐ For Care Homes: Check CQC values (Safe, Effective, Caring, Responsive, Well-led)",
                "⭐ For Schools: Understand their ethos and safeguarding commitment",
                "💡 TIP: Mention their specific values in your answers! Shows you did research!"
            ]
        },
        {
            'area': 'Organization Background',
            'what_to_find': [
                "Type of organization (NHS Trust, private care, academy school, etc.)",
                "Size (number of staff, beds, students, service users)",
                "Locations and sites",
                "Specialties and services offered",
                "Year established",
                "Part of larger group/trust?"
            ]
        },
        {
            'area': 'Leadership & Structure',
            'what_to_find': [
                "Who is the CEO/Headteacher/Manager?",
                "Leadership team structure",
                "Department you're joining",
                "Who will be your line manager?",
                "Organizational chart (if available)"
            ]
        },
        {
            'area': 'Recent News & Achievements',
            'what_to_find': [
                "Recent media coverage (Google the organization name + news)",
                "New services or expansions",
                "Awards or recognitions",
                "Community projects",
                "Social media activity (Twitter, LinkedIn, Facebook)"
            ]
        },
        {
            'area': 'Performance & Quality',
            'what_to_find': [
                "For NHS: RTT performance, waiting times (NHS England website)",
                "For Care: CQC rating and recent inspection report (cqc.org.uk)",
                "For Schools: Ofsted rating (reports.ofsted.gov.uk)",
                "Patient/service user satisfaction scores",
                "Staff satisfaction scores",
                "Any quality improvement initiatives"
            ]
        },
        {
            'area': 'Culture & Staff Experience',
            'what_to_find': [
                "What do staff say? (Check Glassdoor, Indeed reviews)",
                "Staff benefits and perks",
                "Training and development opportunities",
                "Career progression paths",
                "Work-life balance policies"
            ]
        },
        {
            'area': 'The Team/Department',
            'what_to_find': [
                "Department structure",
                "Team size",
                "Who you'll be working with",
                "LinkedIn profiles of interviewers (if known)",
                "Recent team achievements"
            ]
        },
        {
            'area': 'Challenges & Opportunities',
            'what_to_find': [
                "What challenges is the organization facing?",
                "Any recent changes or reorganizations?",
                "Growth plans",
                "How can YOU add value to this team?"
            ]
        }
    ]


def generate_smart_questions_to_ask(job_title):
    """Questions candidate should ask at interview"""
    
    return [
        {
            'question': 'What does a typical day look like in this role?',
            'why_good': 'Shows genuine interest and helps you understand the role'
        },
        {
            'question': 'What are the main challenges facing the team currently?',
            'why_good': 'Demonstrates you want to add value and solve problems'
        },
        {
            'question': 'How is success measured in this position?',
            'why_good': 'Shows you care about performance and meeting expectations'
        },
        {
            'question': 'What training and development opportunities are available?',
            'why_good': 'Demonstrates ambition and commitment to growth'
        },
        {
            'question': 'What do you enjoy most about working here?',
            'why_good': 'Personal question that builds rapport'
        },
        {
            'question': 'How does this role fit into the wider organizational goals?',
            'why_good': 'Shows strategic thinking'
        },
        {
            'question': 'What are the next steps in the process?',
            'why_good': 'Professional closing question'
        }
    ]


def generate_red_flags_to_avoid():
    """Common mistakes to avoid"""
    
    return [
        {
            'mistake': 'Arriving late',
            'why_bad': 'Shows poor time management and lack of respect',
            'instead': 'Arrive 10-15 minutes early'
        },
        {
            'mistake': 'Not researching the organization',
            'why_bad': 'Shows lack of interest and preparation',
            'instead': 'Spend 2-3 hours researching before interview'
        },
        {
            'mistake': 'Bad-mouthing previous employer',
            'why_bad': 'Raises concerns about professionalism',
            'instead': 'Focus on positive reasons for moving'
        },
        {
            'mistake': 'Not having questions prepared',
            'why_bad': 'Suggests lack of genuine interest',
            'instead': 'Prepare 5 questions minimum'
        },
        {
            'mistake': 'Giving one-word answers',
            'why_bad': 'Doesn\'t demonstrate your capabilities',
            'instead': 'Use STAR method, provide examples'
        },
        {
            'mistake': 'Checking phone during interview',
            'why_bad': 'Extremely unprofessional',
            'instead': 'Turn phone OFF before entering building'
        },
        {
            'mistake': 'Lying or exaggerating',
            'why_bad': 'Will be discovered and cost you the job',
            'instead': 'Be honest, focus on what you CAN do'
        }
    ]
