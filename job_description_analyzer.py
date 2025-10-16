"""
INTELLIGENT JOB DESCRIPTION ANALYZER
ACTUALLY reads and analyzes the job description to generate SPECIFIC questions

This addresses the critical issue: System was ignoring job description content!
"""

import re
from typing import List, Dict, Tuple

def analyze_job_description_deeply(job_desc: str, job_title: str) -> Dict:
    """
    DEEPLY analyze job description to extract SPECIFIC requirements
    Generate questions DIRECTLY from what the employer wrote
    """
    
    job_desc_lower = job_desc.lower()
    
    analysis = {
        'specific_systems': [],
        'specific_skills': [],
        'specific_responsibilities': [],
        'specific_qualifications': [],
        'key_phrases': [],
        'mandatory_requirements': [],
        'desirable_requirements': [],
        'specific_questions': []
    }
    
    # 1. EXTRACT SPECIFIC SYSTEMS/SOFTWARE MENTIONED
    systems_patterns = [
        r'(oracle|cerner|meditech|epic|allscripts|e-Care|RiO|SystmOne|EMIS|TPP)\s+(PAS|EPR|system)',
        r'(Lorenzo|Careflow|Evolve|Trak|eCare|iCare|Vision|DXC)',
        r'Microsoft\s+(Excel|Word|Outlook|Office|365)',
        r'using\s+([A-Z][a-z]+\s+[A-Z][a-z]+)',  # "using Cerner Millennium"
    ]
    
    for pattern in systems_patterns:
        matches = re.findall(pattern, job_desc, re.IGNORECASE)
        for match in matches:
            system = match if isinstance(match, str) else ' '.join(filter(None, match))
            if system and len(system) > 3:
                analysis['specific_systems'].append(system)
    
    # 2. EXTRACT SPECIFIC RESPONSIBILITIES (lines starting with action verbs)
    responsibility_verbs = [
        'manage', 'coordinate', 'ensure', 'provide', 'maintain', 'develop',
        'support', 'deliver', 'monitor', 'validate', 'review', 'update',
        'process', 'handle', 'arrange', 'liaise', 'communicate', 'prepare',
        'investigate', 'resolve', 'implement', 'oversee', 'conduct', 'assist'
    ]
    
    sentences = job_desc.split('.')
    for sentence in sentences:
        sentence = sentence.strip()
        for verb in responsibility_verbs:
            if sentence.lower().startswith(verb):
                if len(sentence) < 200:  # Not too long
                    analysis['specific_responsibilities'].append(sentence)
                break
    
    # 3. EXTRACT MANDATORY vs DESIRABLE
    # Look for "essential", "required", "must have" vs "desirable", "preferred"
    lines = job_desc.split('\n')
    in_essential_section = False
    in_desirable_section = False
    
    for line in lines:
        line_lower = line.lower().strip()
        
        # Section headers
        if any(word in line_lower for word in ['essential', 'required', 'must have', 'mandatory']):
            in_essential_section = True
            in_desirable_section = False
            continue
        elif any(word in line_lower for word in ['desirable', 'preferred', 'advantageous', 'beneficial']):
            in_desirable_section = True
            in_essential_section = False
            continue
        elif any(word in line_lower for word in ['person specification', 'responsibilities', 'duties', 'role overview']):
            in_essential_section = False
            in_desirable_section = False
        
        # Extract requirements
        if line.strip() and (line.startswith('•') or line.startswith('-') or line.startswith('*') or line[0].isdigit()):
            requirement = line.strip('•-*0123456789. ').strip()
            if requirement and len(requirement) > 10:
                if in_essential_section:
                    analysis['mandatory_requirements'].append(requirement)
                elif in_desirable_section:
                    analysis['desirable_requirements'].append(requirement)
    
    # 4. EXTRACT SPECIFIC QUALIFICATIONS/CERTIFICATIONS
    qualification_patterns = [
        r'(NVQ|QCF|BTEC|Degree|Diploma|Certificate|Level\s+\d+|GCSE|A-Level)',
        r'(qualified|certification|certified)\s+in\s+([A-Za-z\s]+)',
        r'([A-Za-z]+)\s+qualification',
    ]
    
    for pattern in qualification_patterns:
        matches = re.findall(pattern, job_desc, re.IGNORECASE)
        for match in matches:
            qual = match if isinstance(match, str) else ' '.join(filter(None, match))
            if qual and len(qual) > 2:
                analysis['specific_qualifications'].append(qual)
    
    # 5. EXTRACT KEY NUMERIC REQUIREMENTS
    # e.g., "2 years experience", "5+ years", "3 days per week"
    numeric_patterns = [
        r'(\d+[\+]?)\s+(years?|months?)\s+(?:of\s+)?(?:experience|exp)',
        r'(\d+)\s+(?:hours?|days?)\s+(?:per|a)\s+week',
        r'minimum\s+of\s+(\d+)',
        r'at least\s+(\d+)',
    ]
    
    for pattern in numeric_patterns:
        matches = re.findall(pattern, job_desc, re.IGNORECASE)
        for match in matches:
            # Find the full context around this number
            for sentence in sentences:
                if any(str(m) in sentence for m in (match if isinstance(match, tuple) else [match])):
                    if len(sentence.strip()) < 150:
                        analysis['key_phrases'].append(sentence.strip())
                        break
    
    # 6. EXTRACT SPECIALTY/DEPARTMENT SPECIFIC INFO
    specialty_patterns = [
        r'(Cardiology|Oncology|Orthopaedics|ENT|General\s+Surgery|Urology|Gynaecology)',
        r'(A&E|Emergency|Outpatient|Inpatient|Day\s+Case)',
        r'working\s+in\s+([A-Za-z\s]+\s+(?:department|clinic|ward|unit))',
    ]
    
    for pattern in specialty_patterns:
        matches = re.findall(pattern, job_desc, re.IGNORECASE)
        for match in matches:
            spec = match if isinstance(match, str) else ' '.join(filter(None, match))
            if spec and len(spec) > 3:
                analysis['specific_skills'].append(spec)
    
    return analysis


def generate_specific_questions_from_job_desc(analysis: Dict, job_title: str) -> List[Dict]:
    """
    Generate SPECIFIC interview questions based on ACTUAL job description content
    NOT generic questions!
    """
    
    specific_questions = []
    
    # 1. QUESTIONS ABOUT SPECIFIC SYSTEMS MENTIONED
    for system in set(analysis['specific_systems'][:5]):  # Top 5 unique systems
        specific_questions.append({
            'category': f'Technical - {system}',
            'question': f'What experience do you have working with {system}?',
            'why_asked': f'Job specifically requires {system} - they want to know your proficiency',
            'likelihood': '95%',
            'source': f'Mentioned in job description: "{system}"'
        })
    
    # 2. QUESTIONS ABOUT SPECIFIC RESPONSIBILITIES
    for i, responsibility in enumerate(analysis['specific_responsibilities'][:8]):
        # Create question from responsibility
        # e.g., "Manage outpatient clinics" → "How would you manage outpatient clinics?"
        question_text = responsibility.strip()
        
        # Convert to question
        if question_text.lower().startswith(('manage', 'coordinate', 'ensure')):
            question = f'How would you {question_text.lower()}?'
        elif question_text.lower().startswith(('provide', 'deliver', 'support')):
            question = f'Can you describe your experience in {question_text.lower()}?'
        else:
            question = f'This role requires you to {question_text}. How would you approach this?'
        
        specific_questions.append({
            'category': 'Role-Specific Responsibility',
            'question': question,
            'why_asked': 'This is a specific responsibility listed in the job description',
            'likelihood': '85%',
            'source': f'From job description: "{responsibility}"'
        })
    
    # 3. QUESTIONS ABOUT MANDATORY REQUIREMENTS
    for req in analysis['mandatory_requirements'][:5]:
        # Create question to assess this requirement
        question = f'The job requires: {req}. Can you tell me about your experience with this?'
        
        specific_questions.append({
            'category': 'Essential Requirement',
            'question': question,
            'why_asked': 'This is listed as an essential requirement',
            'likelihood': '90%',
            'source': f'Essential requirement: "{req}"'
        })
    
    # 4. QUESTIONS ABOUT DESIRABLE REQUIREMENTS
    for req in analysis['desirable_requirements'][:3]:
        question = f'The job mentions {req} as desirable. Do you have any experience with this?'
        
        specific_questions.append({
            'category': 'Desirable Requirement',
            'question': question,
            'why_asked': 'This is listed as a desirable skill',
            'likelihood': '60%',
            'source': f'Desirable requirement: "{req}"'
        })
    
    # 5. QUESTIONS ABOUT SPECIFIC QUALIFICATIONS
    for qual in set(analysis['specific_qualifications'][:3]):
        question = f'Do you have {qual}? If so, how has it prepared you for this role?'
        
        specific_questions.append({
            'category': 'Qualifications',
            'question': question,
            'why_asked': 'Job requires or prefers this qualification',
            'likelihood': '80%',
            'source': f'Qualification mentioned: "{qual}"'
        })
    
    # 6. QUESTIONS ABOUT KEY PHRASES (experience requirements, etc.)
    for phrase in analysis['key_phrases'][:3]:
        question = f'The job description states: "{phrase}". Can you demonstrate how you meet this requirement?'
        
        specific_questions.append({
            'category': 'Experience Requirement',
            'question': question,
            'why_asked': 'Specific experience requirement from job description',
            'likelihood': '85%',
            'source': f'From job description: "{phrase}"'
        })
    
    return specific_questions


def extract_key_competencies_from_job_desc(job_desc: str) -> List[str]:
    """Extract what competencies they'll assess based on job description"""
    
    competencies = []
    job_desc_lower = job_desc.lower()
    
    competency_keywords = {
        'teamwork': ['team', 'collaborate', 'work with others', 'colleagues'],
        'communication': ['communicate', 'liaison', 'written', 'verbal', 'presentation'],
        'problem_solving': ['problem', 'resolve', 'solution', 'troubleshoot'],
        'time_management': ['priorit', 'deadline', 'manage time', 'workload'],
        'attention_to_detail': ['accurate', 'detail', 'quality', 'precision'],
        'customer_service': ['customer', 'service', 'patient care', 'satisfaction'],
        'leadership': ['lead', 'supervise', 'manage staff', 'mentor'],
        'adaptability': ['flexible', 'adapt', 'change', 'various']
    }
    
    for competency, keywords in competency_keywords.items():
        if any(keyword in job_desc_lower for keyword in keywords):
            competencies.append(competency)
    
    return competencies


def create_comprehensive_question_list(job_desc: str, job_title: str) -> List[Dict]:
    """
    Create COMPREHENSIVE question list that:
    1. Uses ACTUAL job description content (SPECIFIC questions)
    2. Adds relevant generic questions
    3. Ensures questions are RELEVANT to this specific job
    """
    
    all_questions = []
    
    # STEP 1: DEEP ANALYSIS of job description
    analysis = analyze_job_description_deeply(job_desc, job_title)
    
    # STEP 2: Generate SPECIFIC questions from job description
    specific_questions = generate_specific_questions_from_job_desc(analysis, job_title)
    all_questions.extend(specific_questions)
    
    # STEP 3: Add standard opening/closing (always asked)
    all_questions.extend([
        {
            'category': 'Introduction',
            'question': 'Tell me about yourself and your experience',
            'why_asked': 'Standard opening question',
            'likelihood': '100%',
            'source': 'Standard interview question'
        },
        {
            'category': 'Motivation',
            'question': f'Why do you want to work as a {job_title}?',
            'why_asked': 'Assesses genuine interest',
            'likelihood': '95%',
            'source': 'Standard interview question'
        },
        {
            'category': 'Motivation',
            'question': 'Why do you want to work for our organization?',
            'why_asked': 'Tests research and cultural fit',
            'likelihood': '95%',
            'source': 'Standard interview question'
        }
    ])
    
    # STEP 4: Add competency questions based on what job requires
    competencies = extract_key_competencies_from_job_desc(job_desc)
    
    competency_question_templates = {
        'teamwork': {
            'question': 'Describe a time when you worked effectively as part of a team',
            'category': 'Competency - Teamwork'
        },
        'communication': {
            'question': 'Give an example of when you had to explain complex information to someone',
            'category': 'Competency - Communication'
        },
        'problem_solving': {
            'question': 'Tell me about a challenging situation you faced and how you resolved it',
            'category': 'Competency - Problem Solving'
        },
        'time_management': {
            'question': 'How do you prioritize your workload when under pressure?',
            'category': 'Competency - Time Management'
        },
        'attention_to_detail': {
            'question': 'Give an example of when attention to detail was critical in your work',
            'category': 'Competency - Attention to Detail'
        },
        'customer_service': {
            'question': 'Describe a time when you went above and beyond for a customer/patient',
            'category': 'Competency - Customer Service'
        }
    }
    
    for competency in competencies:
        if competency in competency_question_templates:
            template = competency_question_templates[competency]
            all_questions.append({
                'category': template['category'],
                'question': template['question'],
                'why_asked': f'Job requires {competency} - they want STAR method example',
                'likelihood': '85%',
                'source': f'Competency identified from job description: {competency}'
            })
    
    # STEP 5: Closing questions (always asked)
    all_questions.extend([
        {
            'category': 'Closing',
            'question': 'Do you have any questions for us?',
            'why_asked': 'You MUST have questions prepared!',
            'likelihood': '100%',
            'source': 'Standard interview question'
        },
        {
            'category': 'Closing',
            'question': 'What are your strengths and weaknesses?',
            'why_asked': 'Tests self-awareness',
            'likelihood': '80%',
            'source': 'Standard interview question'
        }
    ])
    
    return all_questions
