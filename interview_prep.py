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
    """
    
    # Extract key skills and requirements from job description
    keywords = {
        # RTT & NHS Admin
        'rtt': ['RTT', 'referral to treatment', '18 weeks', 'pathway', 'clock'],
        'pas': ['PAS', 'patient administration', 'booking', 'appointment'],
        'nhs': ['NHS', 'trust', 'hospital', 'clinic'],
        'validation': ['validation', 'data quality', 'accuracy', 'audit'],
        'coding': ['coding', 'ICD', 'OPCS', 'HRG'],
        
        # Healthcare & Care Work
        'healthcare_assistant': ['healthcare assistant', 'HCA', 'care assistant', 'support worker'],
        'care_work': ['care', 'caring', 'personal care', 'patient care', 'service user'],
        'adult_social_care': ['adult social care', 'social care', 'care home', 'domiciliary'],
        'clinical_tasks': ['observations', 'vital signs', 'blood pressure', 'temperature'],
        'safeguarding': ['safeguarding', 'safeguard', 'vulnerable', 'abuse', 'dignity'],
        
        # Teaching & Education
        'teaching_assistant': ['teaching assistant', 'TA', 'classroom', 'pupils', 'students'],
        'education': ['education', 'learning', 'SEND', 'SEN', 'special needs'],
        'child_development': ['child development', 'early years', 'behaviour management'],
        
        # Customer Service
        'customer_service': ['customer service', 'customer', 'client', 'complaint', 'query'],
        'reception': ['reception', 'front desk', 'telephone', 'booking'],
        
        # Business Administration
        'admin': ['administration', 'admin', 'office', 'filing', 'record keeping'],
        'business_admin': ['business administration', 'processes', 'procedures', 'compliance'],
        
        # IT & Technical
        'it_skills': ['Excel', 'Microsoft', 'IT', 'systems', 'software', 'computer'],
        'it_support': ['IT support', 'helpdesk', 'technical', 'troubleshooting'],
        
        # Universal Skills
        'communication': ['communication', 'team', 'stakeholder', 'interpersonal'],
        'confidentiality': ['confidentiality', 'GDPR', 'data protection', 'sensitive']
    }
    
    found_skills = []
    for skill_category, terms in keywords.items():
        for term in terms:
            if term.lower() in job_description.lower():
                found_skills.append(skill_category)
                break
    
    # Generate interview questions based on job requirements
    questions = generate_questions(job_title, found_skills, job_description)
    
    # Generate preparation tips
    prep_tips = generate_prep_tips(job_title, found_skills)
    
    # Generate example answers using GPT-4 for ALL questions (intelligent AI answers)
    example_answers = generate_ai_powered_answers(questions, job_title, job_description)
    
    return {
        'job_title': job_title,
        'company_name': company_name,
        'identified_skills': found_skills,
        'interview_questions': questions,
        'preparation_tips': prep_tips,
        'example_answers': example_answers,
        'research_areas': generate_research_areas(company_name, job_title)
    }


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
    
    # Confidentiality / GDPR (important for all roles)
    if 'confidentiality' in skills or 'nhs' in skills or 'care_work' in skills:
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
