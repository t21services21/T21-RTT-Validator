"""
AI-Powered Application Generator
Generates UNIQUE supporting information for each job
Uses GPT-4 to create customized, professional content
"""

import openai
from datetime import datetime
import logging
import os
import re

logger = logging.getLogger(__name__)

class AIApplicationGenerator:
    """
    Generates unique supporting information for each NHS job application
    Each application gets custom content tailored to the specific job
    """
    
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.model = "gpt-4"
        self.max_words = 1500
    
    async def generate_supporting_information(self, student: dict, job: dict) -> dict:
        """
        Generates unique 1500-word supporting information
        
        Args:
            student: Student profile with qualifications, experience
            job: Job details including description, criteria, trust
        
        Returns:
            dict with 'supporting_info', 'word_count', 'generation_time'
        """
        start_time = datetime.now()
        
        logger.info(f"🤖 Generating supporting info for: {job['title']} at {job['trust']}")
        
        # Build comprehensive prompt
        prompt = self.build_prompt(student, job)
        
        # Generate with GPT-4
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": self.get_system_prompt()
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.8,  # Creative but professional
                max_tokens=2500,
                presence_penalty=0.6,  # Encourage diverse content
                frequency_penalty=0.3   # Reduce repetition
            )
            
            supporting_info = response.choices[0].message.content.strip()
            
            # Validate and clean
            supporting_info = self.clean_and_validate(supporting_info, job)
            
            # Calculate metrics
            word_count = len(supporting_info.split())
            generation_time = (datetime.now() - start_time).total_seconds()
            
            logger.info(f"✅ Generated {word_count} words in {generation_time:.2f}s")
            
            return {
                'supporting_info': supporting_info,
                'word_count': word_count,
                'generation_time': generation_time,
                'quality_score': self.calculate_quality_score(supporting_info, job)
            }
            
        except Exception as e:
            logger.error(f"❌ AI generation failed: {e}")
            raise
    
    def build_prompt(self, student: dict, job: dict) -> str:
        """
        Builds detailed prompt for AI generation
        """
        # Extract student info
        student_name = student.get('first_name', 'Student')
        qualifications = self.format_qualifications(student.get('qualifications', []))
        experience = self.format_experience(student.get('employment_history', []))
        skills = ', '.join(student.get('skills', ['RTT validation', 'Patient pathway coordination', 'NHS systems']))
        
        # Extract job requirements
        essential_criteria = self.format_criteria(job.get('essential_criteria', {}))
        desirable_criteria = self.format_criteria(job.get('desirable_criteria', {}))
        
        prompt = f"""Write a professional Supporting Information section for this NHS job application.

STUDENT PROFILE:
Name: {student_name}

Key Qualification:
- TQUK-Endorsed Professional Development Learning Course in RTT and Hospital Administration
- Provider: T21 Services (TQUK Approved Centre #36257481088)
- Course Code: PDLC-01-039
- Completion: {student.get('tquk_completion_date', '2025')}
- Duration: 12-week intensive training program

Additional Qualifications:
{qualifications}

Relevant Experience:
{experience}

Key Skills:
{skills}

JOB DETAILS:
Position: {job['title']}
NHS Trust: {job['trust']}
Location: {job['location']}
Band: {job.get('band', 'Band 3-4')}

JOB DESCRIPTION:
{job.get('job_description', '')[:1000]}

MAIN DUTIES AND RESPONSIBILITIES:
{job.get('main_duties', '')[:800]}

ESSENTIAL CRITERIA:
{essential_criteria}

DESIRABLE CRITERIA:
{desirable_criteria}

INSTRUCTIONS:
Write a compelling 1200-1500 word Supporting Information section that:

1. **DEMONSTRATES EACH ESSENTIAL CRITERION** - Show how the student meets EVERY essential requirement with specific examples

2. **HIGHLIGHTS TQUK RTT TRAINING** - Emphasize:
   - RTT pathway understanding (18-week target)
   - Patient tracking and validation
   - Clock start/stop rules
   - Data quality and accuracy
   - NHS systems knowledge (PAS, EPR)
   - Information governance
   
3. **SHOWS MOTIVATION FOR THIS SPECIFIC TRUST** - Research {job['trust']} and mention:
   - Trust's reputation or specialties
   - Why student wants to work there specifically
   - Alignment with NHS values

4. **USES SPECIFIC JOB LANGUAGE** - Mirror terminology from job description:
   - Mention specific systems mentioned in job ad
   - Use exact phrases for key responsibilities
   - Reference the job title naturally

5. **PROFESSIONAL STRUCTURE**:
   - Opening: Enthusiasm for role and trust
   - Body: Evidence for each criterion (use STAR approach)
   - Skills section: Transferable skills relevant to role
   - Closing: Commitment and eagerness to contribute

6. **TONE**: Confident, professional, enthusiastic, evidence-based

DO NOT:
- Include personal details (name, address) - these are in other sections
- Use generic statements that could apply to any job
- Be overly humble or apologetic
- Mention salary or benefits
- Duplicate other application sections
- Use clichés or overused phrases

Begin writing now. Start with a strong opening paragraph expressing genuine interest in THIS specific role at THIS specific trust.
"""
        
        return prompt
    
    def get_system_prompt(self) -> str:
        """
        System prompt for consistent quality
        """
        return """You are an expert NHS job application writer with 15+ years of experience helping candidates secure Band 3-5 administrative positions in NHS trusts across the UK.

You have deep expertise in:
- RTT (Referral to Treatment) pathways and 18-week targets
- NHS administrative processes and Patient Administration Systems (PAS)
- Patient pathway coordination and validation
- TQUK professional development qualifications
- Matching candidate skills to NHS job requirements
- NHS values: Care, Compassion, Competence, Communication, Courage, Commitment
- Person-centered care and patient experience
- Information governance and data protection

Your writing is:
- Professional yet warm and personable
- Evidence-based with specific examples
- Tailored precisely to each job description
- Free from generic statements
- Confident without being arrogant
- Structured logically with clear paragraphs

Every application you write is unique. You never use template phrases or copy-paste content. You research the specific NHS trust and reference their work when possible."""
    
    def format_qualifications(self, qualifications: list) -> str:
        """Format qualifications list"""
        if not qualifications:
            return "- GCSE English and Maths (Grade C or above)"
        
        formatted = []
        for qual in qualifications:
            if isinstance(qual, dict):
                formatted.append(f"- {qual.get('subject', '')} - {qual.get('grade', '')} ({qual.get('year', '')})")
            else:
                formatted.append(f"- {qual}")
        
        return '\n'.join(formatted)
    
    def format_experience(self, employment_history: list) -> str:
        """Format employment history"""
        if not employment_history:
            return "- Recent completion of intensive RTT training program"
        
        formatted = []
        for job in employment_history[:3]:  # Last 3 jobs
            if isinstance(job, dict):
                formatted.append(f"- {job.get('job_title', '')} at {job.get('employer', '')} ({job.get('start_date', '')} - {job.get('end_date', 'Present')})")
        
        return '\n'.join(formatted) if formatted else "- Recent completion of intensive RTT training program"
    
    def format_criteria(self, criteria: dict) -> str:
        """Format essential/desirable criteria"""
        if not criteria:
            return "Not specified"
        
        if isinstance(criteria, dict):
            if 'raw' in criteria:
                return criteria['raw']
            return str(criteria)
        
        return str(criteria)
    
    def clean_and_validate(self, text: str, job: dict) -> str:
        """
        Clean and validate generated text
        """
        # Remove any personal info patterns that AI might have added
        text = re.sub(r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b', '', text)  # Phone numbers
        text = re.sub(r'\b[A-Z]{2}\d{6}[A-Z]?\b', '', text)  # NI numbers
        text = re.sub(r'\b\d{1,3}\s+\w+\s+(Street|Road|Avenue|Lane)\b', '', text, flags=re.IGNORECASE)  # Addresses
        
        # Ensure word count
        words = text.split()
        if len(words) > self.max_words:
            text = ' '.join(words[:self.max_words])
        
        # Ensure minimum quality
        if len(words) < 800:
            logger.warning(f"⚠️ Generated text too short: {len(words)} words")
        
        return text.strip()
    
    def calculate_quality_score(self, text: str, job: dict) -> float:
        """
        Calculate quality score 0-100
        """
        score = 0
        
        # Check mentions of trust (20 points)
        if job.get('trust', '').lower() in text.lower():
            score += 20
        
        # Check mentions of position (20 points)
        if job.get('title', '').lower() in text.lower():
            score += 20
        
        # Check mentions of RTT (20 points)
        if 'rtt' in text.lower() or 'referral to treatment' in text.lower():
            score += 20
        
        # Check mentions of TQUK (15 points)
        if 'tquk' in text.lower() or 't21' in text.lower():
            score += 15
        
        # Word count appropriate (10 points)
        word_count = len(text.split())
        if 1000 <= word_count <= 1500:
            score += 10
        elif 800 <= word_count < 1000:
            score += 5
        
        # Professional tone - no weak language (15 points)
        weak_words = ['maybe', 'perhaps', 'i think', 'probably', 'might']
        if not any(word in text.lower() for word in weak_words):
            score += 15
        
        return score
    
    async def generate_batch(self, student: dict, jobs: list, max_concurrent: int = 5) -> list:
        """
        Generate supporting information for multiple jobs in parallel
        """
        import asyncio
        
        results = []
        
        # Process in batches to avoid rate limits
        for i in range(0, len(jobs), max_concurrent):
            batch = jobs[i:i+max_concurrent]
            
            tasks = [
                self.generate_supporting_information(student, job)
                for job in batch
            ]
            
            batch_results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Filter out exceptions
            for result in batch_results:
                if isinstance(result, dict):
                    results.append(result)
                else:
                    logger.error(f"Batch generation error: {result}")
            
            # Rate limiting
            await asyncio.sleep(1)  # 1 second between batches
        
        logger.info(f"✅ Generated {len(results)} supporting information texts")
        
        return results


# Example usage
if __name__ == '__main__':
    import asyncio
    
    # Test data
    student = {
        'first_name': 'John',
        'qualifications': [
            {'subject': 'BSc Health Management', 'grade': '2:1', 'year': '2020'}
        ],
        'employment_history': [],
        'skills': ['RTT validation', 'Patient coordination', 'Data entry'],
        'tquk_completion_date': 'April 2025'
    }
    
    job = {
        'title': 'RTT Validator',
        'trust': 'University College London Hospitals NHS Foundation Trust',
        'location': 'London',
        'band': 'Band 4',
        'job_description': 'Validate patient pathways and ensure RTT compliance...',
        'main_duties': 'Monitor PTL, validate pathways, produce reports...',
        'essential_criteria': {'raw': 'GCSE English and Maths, administrative experience'}
    }
    
    generator = AIApplicationGenerator()
    result = asyncio.run(generator.generate_supporting_information(student, job))
    
    print(f"Generated {result['word_count']} words")
    print(f"Quality score: {result['quality_score']}/100")
    print(f"\n{result['supporting_info'][:500]}...")
