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
                st.info("🤖 Using GPT-4 AI to analyze your job description...")
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
            st.error(f"❌ GPT-4 analysis error: {e}")
            print(f"GPT-4 analysis failed: {e}, falling back to keyword matching")
    
    # Fallback to keyword matching if GPT-4 unavailable
    st.warning("""
    ⚠️ **Falling back to basic keyword matching**
    
    GPT-4 analysis failed. Using basic detection (less accurate).
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
    st.info("🔄 Connecting to GPT-4...")
    from openai import OpenAI
    
    try:
        client = OpenAI(api_key=api_key)
    except Exception as e:
        st.error(f"❌ Failed to initialize OpenAI client: {e}")
        raise
    
    # Create comprehensive interview preparation
    prompt = f"""Please analyze this job description and provide comprehensive interview preparation.

JOB TITLE: {job_title}
ORGANIZATION: {company_name}

JOB DESCRIPTION:
{job_description}

Please help prepare for this interview by generating 30-40 relevant questions based on the specific job description provided.

Please analyze:
1. The key requirements and responsibilities
2. What the employer prioritizes
3. Likely questions based on:
   - Specific systems/software mentioned
   - Responsibilities listed
   - Essential and desirable requirements
   - Industry standards for this role

Generate 30-40 questions including:

Technical questions (10-15):
- About specific systems mentioned (Oracle PAS, Cerner, etc.)
- About specific responsibilities
- About required qualifications
- Role-specific skills (audio typing, RTT, clinical tasks, etc.)
- Industry standards

Competency questions (8-10):
- Based on required competencies
- STAR method answers with realistic scenarios
- Specific metrics and outcomes
- How to handle role challenges

Scenario questions (5-7):
- Based on challenges mentioned
- "What would you do if..." situations
- Realistic problems for this role
- Tests judgment and priorities

Motivation questions (3-5):
- Why this specific role?
- Why this organization?
- What do you know about us?
- Career goals alignment

Opening and closing (3-5):
- Tell me about yourself
- Strengths/weaknesses
- Questions for us
- Availability, notice period

For each question provide:
1. The exact question (as interviewer would ask)
2. Why they ask (what they're assessing)
3. Likelihood percentage
4. Detailed answer (300-500 words):
   - Specific to this job
   - Uses terminology from job description
   - Includes examples with metrics
   - Shows understanding of role challenges
   - Demonstrates research about organization
   - STAR method for competency questions
5. Tips (3-5):
   - What interviewers want to hear
   - Red flags to avoid
   - How to stand out
   - Specific details to mention

Return as JSON with this COMPLETE structure:
{{
  "questions": [
    {{
      "category": "Technical - [Specific Area]",
      "question": "Exact question as interviewer would ask it",
      "why_asked": "Real reason they're asking (what competency/skill they're testing)",
      "likelihood": "95%",
      "answer": "EXPERT 300-500 word answer with specifics, examples, metrics",
      "tips": ["Insider tip 1", "What they want to hear", "Red flag to avoid", "How to stand out", "Specific detail to mention"],
      "red_flags": ["What NOT to say", "Common mistake candidates make"]
    }}
  ],
  "organization_research": {{
    "mission": "Their mission statement and what it means",
    "vision": "Their vision and how to align with it",
    "values": ["Value 1: How to demonstrate it", "Value 2: Example of living it"],
    "recent_news": ["Recent achievement 1", "Recent news 2"],
    "services": "What they're known for",
    "cqc_rating": "CQC rating and what to say about it (if NHS)",
    "challenges": "Challenges they face and how you can help",
    "culture": "What they value in employees"
  }},
  "interview_etiquette": {{
    "what_to_wear": "Specific advice for this role/industry",
    "arrival_time": "When to arrive and what to do",
    "panel_composition": "Who you'll likely meet",
    "interview_format": "Competency-based, values-based, etc.",
    "duration": "How long it typically lasts",
    "opening": ["How to introduce yourself", "Small talk tips", "First impression"],
    "during": ["Active listening", "How to think before answering", "Body language"],
    "closing": ["How to ask questions", "Express interest", "Thank panel", "Exit strategy"]
  }},
  "questions_to_ask": [
    {{"question": "Smart question 1", "why_good": "Shows X"}},
    {{"question": "Smart question 2", "why_good": "Demonstrates Y"}},
    {{"question": "Smart question 3", "why_good": "Proves Z"}}
  ],
  "post_interview": {{
    "thank_you_email": "Template for same-day thank you",
    "when_to_follow_up": "Timeline guidance",
    "how_to_follow_up": "Professional follow-up template",
    "handling_rejection": "How to request feedback and stay professional"
  }},
  "salary_discussion": {{
    "when_to_discuss": "When to bring up salary",
    "how_to_answer": "Template for 'What are your expectations?'",
    "nhs_pay_bands": "Explanation of NHS bands (if applicable)",
    "negotiation_tips": "How to negotiate if private sector"
  }},
  "prep_tips": {{
    "before_interview": ["Tip 1", "Tip 2"],
    "on_the_day": ["Tip 1", "Tip 2"],
    "technical_prep": ["Tip 1", "Tip 2"],
    "key_documents": ["Doc 1", "Doc 2"]
  }}
}}

Quality guidelines:
- Questions come from actual job description
- Answers reference specific systems/responsibilities from the job
- Include industry-specific knowledge
- STAR examples are realistic for this role
- Tips include insider knowledge
- Answers are 300-500 words comprehensive
- Every answer includes metrics/specifics
- Show understanding of role challenges
- Demonstrate research about organization

Additional comprehensive sections to include:

About the organization (if company name provided):
1. Mission Statement - What it means and how to reference it
2. Vision Statement - How to align your answers with it
3. Core Values - Specific examples of demonstrating each value
4. Recent News/Achievements - What to mention to show research
5. Services/Specialties - What they're known for
6. CQC Rating (if NHS) - What it means, how to discuss
7. Key Challenges - What problems they face, how you can help
8. Culture/Team - What they value in employees

Interview etiquette and process:
1. What to wear (specific to role/industry)
2. What time to arrive (10-15 mins early)
3. Who you'll meet (typical panel composition)
4. Interview format (competency-based, values-based, etc.)
5. How long interview typically lasts
6. What to bring (documents, certificates, portfolio)
7. Body language tips
8. How to greet the panel professionally
9. How to handle nerves
10. How to close the interview positively

Opening the interview:
1. How to introduce yourself when you walk in
2. Small talk tips
3. First impression strategies
4. How to sit (posture, where to put hands)
5. Initial rapport building

During the interview:
1. Active listening techniques
2. How to take a moment to think before answering
3. How to ask for clarification if needed
4. How to handle questions you don't know
5. How to redirect if you go off-topic
6. How to read panel body language
7. When to give examples vs concise answers
8. How to manage time

Closing the interview:
1. How to ask your prepared questions
2. What questions to ask (5-7 smart questions provided)
3. How to express continued interest
4. How to ask about next steps
5. How to thank the panel
6. Exit strategy

Post-interview:
1. When to send thank-you email (same day)
2. Template for thank-you email
3. When to expect to hear back
4. How to follow up if you don't hear
5. How to handle rejection professionally
6. How to request feedback

Questions to ask them (10-12 smart questions):
Categorized by:
- About the role (day-to-day, challenges, success measures)
- About the team (size, culture, support)
- About development (training, progression, growth)
- About the organization (future plans, priorities)
- Practical (next steps, timeline, start date)

Salary and negotiation:
1. When to discuss salary
2. How to answer "What are your salary expectations?"
3. NHS pay bands explained (if applicable)
4. How to negotiate (if private sector)
5. Benefits to ask about

Red flags to watch for:
Not just what they ask about you, but warning signs about them:
- High turnover mentions
- Vague job description
- Unprofessional panel behavior
- Unrealistic expectations
- Poor communication

Please provide comprehensive, detailed preparation that helps the candidate be well-prepared for their interview."""

    try:
        st.info("📤 Sending request to GPT-4...")
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an experienced HR professional helping candidates prepare for job interviews. Provide comprehensive, professional interview preparation based on job descriptions. Return ONLY valid JSON, no markdown formatting."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=16000,  # For 30-40 detailed questions
            response_format={"type": "json_object"}  # Force JSON output (no markdown)
        )
        
        st.success("✅ Got response from GPT-4!")
        st.info("🔄 Parsing response...")
        
        import json
        raw_content = response.choices[0].message.content
        
        # Show first 500 chars for debugging
        st.text(f"Response preview: {raw_content[:500]}...")
        
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
        
        # Debug: Show what we're actually trying to parse
        st.text(f"After cleanup (first 200 chars): {raw_content[:200]}...")
        st.text(f"After cleanup (last 200 chars): ...{raw_content[-200:]}")
        
        try:
            result = json.loads(raw_content)
            st.success("✅ Successfully parsed response!")
        except json.JSONDecodeError as e:
            st.error(f"""
            ❌ **JSON Parsing Error**
            
            **Error:** {str(e)}
            **Error Position:** Line {e.lineno}, Column {e.colno}
            
            **Content around error (chars {max(0, e.pos-100)}-{min(len(raw_content), e.pos+100)}):**
            ```
            {raw_content[max(0, e.pos-100):min(len(raw_content), e.pos+100)]}
            ```
            
            **First 500 chars of cleaned content:**
            ```
            {raw_content[:500]}
            ```
            
            **Last 500 chars of cleaned content:**
            ```
            {raw_content[-500:]}
            ```
            """)
            
            # Try to fix common issues
            st.warning("Attempting to fix JSON...")
            
            # Check if response was truncated (no closing brace)
            if not raw_content.rstrip().endswith('}'):
                st.error("❌ Response appears truncated (no closing brace). GPT-4 hit token limit.")
            
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
