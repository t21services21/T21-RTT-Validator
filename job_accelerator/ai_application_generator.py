"""
AI APPLICATION GENERATOR
Uses GPT-4 to create perfectly tailored CVs and cover letters
This is our SECRET WEAPON - competitors can't match this quality!
"""

import openai
import json
import logging
from typing import Dict, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class AIApplicationGenerator:
    """
    AI-powered CV and cover letter generator
    
    What makes this BETTER than competitors:
    1. Uses GPT-4 (not GPT-3.5) - higher quality
    2. TQUK certification integration - shows quality
    3. NHS-specific language and terminology
    4. ATS-optimized (uses keywords from job description)
    5. Personalized for each student and job
    6. Professional UK business standards
    """
    
    def __init__(self, openai_api_key: str, config: dict):
        self.api_key = openai_api_key
        self.config = config
        openai.api_key = openai_api_key
        
        self.model = config.get('model', 'gpt-4-turbo-preview')
        self.backup_model = config.get('backup_model', 'gpt-3.5-turbo')
        self.temperature = config.get('temperature', 0.7)
        self.max_tokens = config.get('max_tokens', 2000)
    
    async def generate_tailored_cv(
        self, 
        student: Dict, 
        job: Dict,
        tquk_certification: Dict
    ) -> str:
        """
        Generate CV tailored to specific job
        
        Args:
            student: Student profile dict
            job: Job details dict
            tquk_certification: TQUK certification details
            
        Returns:
            Tailored CV as formatted text
        """
        
        logger.info(f"🤖 Generating tailored CV for {student['first_name']} {student['last_name']}")
        logger.info(f"📄 Job: {job['title']} at {job['company']}")
        
        # Build student profile summary
        student_profile = self._build_student_profile(student)
        
        # Build TQUK certification text
        tquk_text = self._build_tquk_certification_text(tquk_certification)
        
        # Create prompt
        prompt = self.config['ai_prompts']['cv_tailor'].format(
            job_title=job['title'],
            company=job['company'],
            job_description=job.get('description', job.get('salary_text', '')),
            student_profile=student_profile,
            tquk_certification=tquk_text
        )
        
        try:
            # Call GPT-4
            response = await self._call_openai(prompt, max_tokens=1500)
            
            cv_text = response.strip()
            
            logger.info(f"✅ Generated CV ({len(cv_text)} characters)")
            
            return cv_text
            
        except Exception as e:
            logger.error(f"❌ CV generation failed: {str(e)}")
            
            # Fallback to template-based CV
            return self._generate_template_cv(student, job, tquk_certification)
    
    async def generate_cover_letter(
        self,
        student: Dict,
        job: Dict,
        tquk_certification: Dict
    ) -> str:
        """
        Generate personalized cover letter
        
        Args:
            student: Student profile dict
            job: Job details dict
            tquk_certification: TQUK certification details
            
        Returns:
            Professional cover letter
        """
        
        logger.info(f"✉️ Generating cover letter for {student['first_name']} {student['last_name']}")
        
        student_profile = self._build_student_profile(student)
        tquk_text = self._build_tquk_certification_text(tquk_certification)
        
        prompt = self.config['ai_prompts']['cover_letter'].format(
            job_title=job['title'],
            company=job['company'],
            job_description=job.get('description', job.get('salary_text', '')),
            student_name=f"{student['first_name']} {student['last_name']}",
            student_profile=student_profile,
            tquk_certification=tquk_text
        )
        
        try:
            response = await self._call_openai(prompt, max_tokens=800)
            
            cover_letter = response.strip()
            
            # Add proper letter formatting
            formatted_letter = self._format_cover_letter(
                cover_letter,
                student,
                job,
                datetime.now().strftime("%d %B %Y")
            )
            
            logger.info(f"✅ Generated cover letter ({len(formatted_letter)} characters)")
            
            return formatted_letter
            
        except Exception as e:
            logger.error(f"❌ Cover letter generation failed: {str(e)}")
            
            # Fallback to template
            return self._generate_template_cover_letter(student, job, tquk_certification)
    
    async def calculate_match_score(
        self,
        student: Dict,
        job: Dict
    ) -> Dict:
        """
        Calculate how well student matches job
        
        Returns:
            {
                'score': 0-100,
                'reasoning': 'explanation',
                'missing_requirements': ['req1', 'req2']
            }
        """
        
        logger.info(f"📊 Calculating match score: {student['first_name']} → {job['title']}")
        
        student_profile = self._build_student_profile(student)
        job_description = job.get('description', '') + '\n' + job.get('requirements', '')
        
        prompt = self.config['ai_prompts']['job_match_score'].format(
            student_profile=student_profile,
            job_description=job_description
        )
        
        try:
            response = await self._call_openai(prompt, max_tokens=500)
            
            # Parse JSON response
            match_data = json.loads(response)
            
            logger.info(f"✅ Match score: {match_data['score']}/100")
            
            return match_data
            
        except Exception as e:
            logger.error(f"❌ Match score calculation failed: {str(e)}")
            
            # Fallback to simple keyword matching
            return self._calculate_simple_match_score(student, job)
    
    async def predict_interview_likelihood(
        self,
        student: Dict,
        job: Dict,
        match_score: float,
        historical_success_rate: float = 15.0
    ) -> Dict:
        """
        Predict likelihood of getting interview
        
        Returns:
            {
                'interview_probability': 0-100,
                'confidence': 'low|medium|high',
                'key_factors': ['factor1', 'factor2']
            }
        """
        
        logger.info(f"🔮 Predicting interview likelihood")
        
        student_profile = self._build_student_profile(student)
        
        prompt = self.config['ai_prompts']['interview_prediction'].format(
            student_profile=student_profile,
            job_title=job['title'],
            company=job['company'],
            job_board=job['job_board'],
            match_score=match_score,
            historical_success_rate=historical_success_rate
        )
        
        try:
            response = await self._call_openai(prompt, max_tokens=400)
            
            prediction = json.loads(response)
            
            logger.info(f"✅ Interview probability: {prediction['interview_probability']}%")
            
            return prediction
            
        except Exception as e:
            logger.error(f"❌ Interview prediction failed: {str(e)}")
            
            # Fallback to rule-based prediction
            return self._predict_simple_interview_likelihood(match_score, historical_success_rate)
    
    async def _call_openai(self, prompt: str, max_tokens: int = 1000) -> str:
        """Call OpenAI API with retry logic"""
        
        try:
            # Try GPT-4 first
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert CV writer and career coach specializing in NHS and healthcare roles in the UK."},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature,
                max_tokens=max_tokens
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.warning(f"⚠️ GPT-4 failed, trying backup model: {str(e)}")
            
            # Fallback to GPT-3.5
            try:
                response = openai.ChatCompletion.create(
                    model=self.backup_model,
                    messages=[
                        {"role": "system", "content": "You are an expert CV writer and career coach specializing in NHS and healthcare roles in the UK."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=self.temperature,
                    max_tokens=max_tokens
                )
                
                return response.choices[0].message.content
                
            except Exception as e2:
                logger.error(f"❌ Both AI models failed: {str(e2)}")
                raise
    
    def _build_student_profile(self, student: Dict) -> str:
        """Build student profile text for AI prompts"""
        
        profile_parts = [
            f"Name: {student['first_name']} {student['last_name']}",
            f"Email: {student['email']}",
            f"Phone: {student['phone']}",
        ]
        
        if student.get('skills'):
            skills_list = student['skills'] if isinstance(student['skills'], list) else json.loads(student.get('skills', '[]'))
            if skills_list:
                profile_parts.append(f"Skills: {', '.join(skills_list)}")
        
        if student.get('experience_years'):
            profile_parts.append(f"Experience: {student['experience_years']} years in healthcare/administration")
        
        if student.get('qualifications'):
            quals = student['qualifications'] if isinstance(student['qualifications'], list) else json.loads(student.get('qualifications', '[]'))
            if quals:
                profile_parts.append(f"Qualifications: {', '.join(quals)}")
        
        if student.get('previous_roles'):
            profile_parts.append(f"Previous Experience: {student['previous_roles']}")
        
        return "\n".join(profile_parts)
    
    def _build_tquk_certification_text(self, tquk_cert: Dict) -> str:
        """Build TQUK certification text"""
        
        cert_text = [
            "TQUK-Recognized Professional Development:",
            f"- TQUK Approved Centre #{tquk_cert.get('centre_number', '36257481088')}",
            f"- Course: {tquk_cert.get('course_name', 'Understanding RTT and Hospital Administration')}",
            f"- Course Code: {tquk_cert.get('course_code', 'PDLC-01-039')}",
        ]
        
        if tquk_cert.get('certification_level'):
            cert_text.append(f"- Achievement: {tquk_cert['certification_level']}")
        
        if tquk_cert.get('certification_date'):
            cert_text.append(f"- Certified: {tquk_cert['certification_date']}")
        
        cert_text.append(f"- Verification: {tquk_cert.get('verification_url', 'https://t21-healthcare-platform.streamlit.app')}")
        
        return "\n".join(cert_text)
    
    def _format_cover_letter(
        self,
        letter_body: str,
        student: Dict,
        job: Dict,
        date: str
    ) -> str:
        """Format cover letter with proper UK business letter format"""
        
        formatted = f"""
{student['first_name']} {student['last_name']}
{student.get('address_line1', '')}
{student.get('city', '')} {student.get('postcode', '')}
{student['email']}
{student['phone']}

{date}

Recruitment Team
{job['company']}
{job.get('location', '')}

Dear Hiring Manager,

{letter_body}

Yours sincerely,

{student['first_name']} {student['last_name']}
"""
        
        return formatted.strip()
    
    def _generate_template_cv(
        self,
        student: Dict,
        job: Dict,
        tquk_cert: Dict
    ) -> str:
        """Fallback template-based CV if AI fails"""
        
        cv = f"""
{student['first_name']} {student['last_name'].upper()}
{student['email']} | {student['phone']}
{student.get('city', '')} {student.get('postcode', '')}

PROFESSIONAL SUMMARY
TQUK-certified healthcare professional with comprehensive training in RTT (Referral to Treatment) pathways, hospital administration, and NHS procedures. Seeking to apply validated skills and knowledge to support {job['company']} in delivering exceptional patient care and administrative excellence.

CERTIFICATIONS & TRAINING
TQUK Approved Centre #{tquk_cert.get('centre_number', '36257481088')}
{tquk_cert.get('course_name', 'Understanding RTT and Hospital Administration')}
Course Code: {tquk_cert.get('course_code', 'PDLC-01-039')}
Achievement Level: {tquk_cert.get('certification_level', 'Certified')}
Verification: {tquk_cert.get('verification_url', 'https://t21-healthcare-platform.streamlit.app')}

KEY SKILLS
- RTT Pathway Management & Validation
- NHS 18-Week Pathway Standards
- Patient Administration Systems (PAS)
- Medical Terminology
- Data Analysis & Reporting
- Microsoft Office Suite (Word, Excel, Outlook)
- Attention to Detail
- Time Management
- Communication Skills

RELEVANT EXPERIENCE
{student.get('previous_roles', 'Recent graduate of comprehensive TQUK-endorsed healthcare administration training')}

EDUCATION
{', '.join(student.get('qualifications', []) or ['Secondary Education'])}

REFERENCES
Available upon request
"""
        return cv.strip()
    
    def _generate_template_cover_letter(
        self,
        student: Dict,
        job: Dict,
        tquk_cert: Dict
    ) -> str:
        """Fallback template cover letter"""
        
        letter = f"""
{student['first_name']} {student['last_name']}
{student['email']} | {student['phone']}

{datetime.now().strftime("%d %B %Y")}

Recruitment Team
{job['company']}

Dear Hiring Manager,

I am writing to express my strong interest in the {job['title']} position at {job['company']}.

As a recent graduate of the TQUK-endorsed Professional Development Learning Course (Course Code: PDLC-01-039) delivered by TQUK Approved Centre #36257481088, I have comprehensive training in RTT pathways, hospital administration, and NHS procedures.

My training has equipped me with:
• Deep understanding of the NHS 18-week RTT pathway standards
• Proficiency in patient administration systems and processes
• Strong analytical skills for data management and reporting
• Excellent attention to detail essential for accurate record-keeping

I am particularly drawn to this opportunity at {job['company']} because of your commitment to delivering high-quality patient care. I am confident that my TQUK-recognized training and dedication to professional excellence would make me a valuable addition to your team.

I am immediately available and eager to contribute to reducing waiting lists and ensuring patients receive timely care. I would welcome the opportunity to discuss how my skills and training align with your needs.

Thank you for considering my application. I look forward to hearing from you.

Yours sincerely,

{student['first_name']} {student['last_name']}
"""
        return letter.strip()
    
    def _calculate_simple_match_score(self, student: Dict, job: Dict) -> Dict:
        """Simple keyword-based matching as fallback"""
        
        score = 50  # Base score
        
        student_skills = set((student.get('skills') or '').lower().split(','))
        job_text = (job.get('description', '') + ' ' + job.get('requirements', '')).lower()
        
        # Check skill matches
        matches = sum(1 for skill in student_skills if skill.strip() in job_text)
        score += min(matches * 10, 40)
        
        # TQUK bonus
        if 'rtt' in job_text or 'referral to treatment' in job_text:
            score += 10
        
        return {
            'score': min(score, 100),
            'reasoning': 'Calculated based on keyword matching',
            'missing_requirements': []
        }
    
    def _predict_simple_interview_likelihood(
        self,
        match_score: float,
        historical_rate: float
    ) -> Dict:
        """Simple rule-based prediction"""
        
        # Base probability on match score
        probability = (match_score / 100) * 30  # Max 30% for perfect match
        
        # Add historical success rate
        probability += historical_rate * 0.7  # Weight historical data
        
        # Determine confidence
        if match_score >= 80:
            confidence = 'high'
        elif match_score >= 60:
            confidence = 'medium'
        else:
            confidence = 'low'
        
        return {
            'interview_probability': min(probability, 100),
            'confidence': confidence,
            'key_factors': ['Match score', 'Historical success rate']
        }


# ============================================
# USAGE EXAMPLE
# ============================================

async def main():
    """Example usage"""
    
    import os
    from config import OPENAI_CONFIG, AI_PROMPTS, TQUK_CONFIG
    
    # Sample student
    student = {
        'first_name': 'Sarah',
        'last_name': 'Johnson',
        'email': 'sarah.johnson@email.com',
        'phone': '07700900123',
        'city': 'London',
        'postcode': 'SW1A 1AA',
        'skills': ['RTT Validation', 'PAS Systems', 'Microsoft Excel', 'Data Analysis'],
        'experience_years': 0,
        'qualifications': ['A-Levels in Biology and Mathematics'],
        'previous_roles': 'Completed comprehensive TQUK-endorsed RTT and Hospital Administration training'
    }
    
    # Sample job
    job = {
        'title': 'RTT Validator',
        'company': 'London NHS Trust',
        'location': 'London',
        'description': 'We are seeking an RTT Validator to join our busy outpatient department...',
        'requirements': 'Experience with RTT pathways, attention to detail, Microsoft Excel proficiency'
    }
    
    # TQUK certification
    tquk_cert = TQUK_CONFIG
    
    # Create generator
    generator = AIApplicationGenerator(
        openai_api_key=os.getenv('OPENAI_API_KEY'),
        config={'ai_prompts': AI_PROMPTS, **OPENAI_CONFIG}
    )
    
    # Generate CV
    print("Generating tailored CV...")
    cv = await generator.generate_tailored_cv(student, job, tquk_cert)
    print("\n" + "="*50)
    print("GENERATED CV:")
    print("="*50)
    print(cv)
    
    # Generate cover letter
    print("\n\nGenerating cover letter...")
    cover_letter = await generator.generate_cover_letter(student, job, tquk_cert)
    print("\n" + "="*50)
    print("GENERATED COVER LETTER:")
    print("="*50)
    print(cover_letter)
    
    # Calculate match score
    print("\n\nCalculating match score...")
    match = await generator.calculate_match_score(student, job)
    print("\n" + "="*50)
    print("MATCH ANALYSIS:")
    print("="*50)
    print(json.dumps(match, indent=2))
    
    # Predict interview likelihood
    print("\n\nPredicting interview likelihood...")
    prediction = await generator.predict_interview_likelihood(student, job, match['score'])
    print("\n" + "="*50)
    print("INTERVIEW PREDICTION:")
    print("="*50)
    print(json.dumps(prediction, indent=2))

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
