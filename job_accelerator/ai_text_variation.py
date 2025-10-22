"""
AI TEXT VARIATION SYSTEM

CRITICAL FEATURE: Avoid Detection When Multiple Students Apply to Same Job

Problem:
- If 20 T21 students apply to same NHS job
- All with identical/similar AI-generated text
- NHS will notice and flag as spam/automated

Solution:
- Generate DIFFERENT text for each student
- Same meaning, different words
- Different sentence structure
- Different examples
- Looks like 20 different people wrote them!
"""

import openai
import random
from typing import List, Dict
import hashlib

class TextVariationEngine:
    """
    Generate varied text to avoid detection
    
    Features:
    1. Multiple writing styles (formal, conversational, enthusiastic)
    2. Different sentence structures
    3. Synonym replacement
    4. Example variation
    5. Paragraph order variation
    6. Tone variation
    """
    
    def __init__(self, openai_api_key: str):
        self.api_key = openai_api_key
        openai.api_key = openai_api_key
        
        self.writing_styles = [
            "professional and formal",
            "warm and enthusiastic",
            "confident and direct",
            "thoughtful and detailed",
            "concise and focused"
        ]
        
        self.tones = [
            "eager and motivated",
            "experienced and capable",
            "passionate about patient care",
            "detail-oriented and thorough",
            "collaborative and team-focused"
        ]
    
    async def generate_varied_cover_letter(
        self,
        student: Dict,
        job: Dict,
        tquk_cert: Dict,
        variation_seed: int = None
    ) -> str:
        """
        Generate cover letter with variation
        
        Args:
            student: Student profile
            job: Job details
            tquk_cert: TQUK certification
            variation_seed: Seed for variation (use student_id + job_id hash)
        
        Returns:
            Unique cover letter for this student
        """
        
        # Create variation seed from student_id and job_id
        if variation_seed is None:
            seed_string = f"{student.get('id', '')}_{job.get('id', '')}"
            variation_seed = int(hashlib.md5(seed_string.encode()).hexdigest(), 16) % 1000
        
        # Select style and tone based on seed
        random.seed(variation_seed)
        style = random.choice(self.writing_styles)
        tone = random.choice(self.tones)
        
        # Generate varied prompt
        prompt = f"""
Write a professional NHS job application cover letter with these specific characteristics:

WRITING STYLE: {style}
TONE: {tone}

Job: {job['title']} at {job['company']}
Applicant: {student['first_name']} {student['last_name']}

Key Points to Cover (but vary HOW you express them):
- TQUK Approved Centre #36257481088 training
- Understanding of RTT pathways
- Passion for NHS and patient care
- Relevant skills for this specific role
- Immediate availability

CRITICAL REQUIREMENTS:
1. Use {style} writing style
2. Maintain {tone} tone throughout
3. Use DIFFERENT examples than typical
4. Vary sentence structure
5. Use synonyms for common words (e.g., "passionate" vs "dedicated" vs "committed")
6. 250-300 words
7. UK professional letter format

Make this letter sound DIFFERENT from other applications while maintaining quality!
"""
        
        # Call OpenAI with higher temperature for variation
        response = await self._call_openai_varied(prompt, temperature=0.9)
        
        return response
    
    async def generate_varied_cv_section(
        self,
        student: Dict,
        job: Dict,
        section: str,
        variation_seed: int = None
    ) -> str:
        """
        Generate varied CV section
        
        Args:
            section: 'summary', 'skills', 'experience'
            variation_seed: For consistent variation
        """
        
        if variation_seed is None:
            seed_string = f"{student.get('id', '')}_{job.get('id', '')}_{section}"
            variation_seed = int(hashlib.md5(seed_string.encode()).hexdigest(), 16) % 1000
        
        random.seed(variation_seed)
        
        if section == 'summary':
            # Vary professional summary
            summary_styles = [
                "Start with years of experience or training",
                "Start with key achievement",
                "Start with career objective",
                "Start with key skills"
            ]
            style = random.choice(summary_styles)
            
            prompt = f"""
Write a professional summary for CV using this approach: {style}

Background:
- TQUK-certified RTT professional
- Trained in hospital administration
- Seeking: {job['title']}

Style: {style}
Length: 2-3 sentences
Make it UNIQUE and different from typical summaries!
"""
        
        elif section == 'skills':
            # Vary how skills are presented
            skills_formats = [
                "Bullet points with brief descriptions",
                "Grouped by category (Technical, Communication, etc.)",
                "Simple comma-separated list",
                "Skills with proficiency levels"
            ]
            format_style = random.choice(skills_formats)
            
            prompt = f"""
List key skills for RTT/healthcare role using: {format_style}

Include:
- RTT pathway knowledge
- PAS systems
- Microsoft Office
- Communication
- Attention to detail

Format: {format_style}
Make it look DIFFERENT from other CVs!
"""
        
        response = await self._call_openai_varied(prompt, temperature=0.8)
        return response
    
    async def _call_openai_varied(self, prompt: str, temperature: float = 0.9) -> str:
        """
        Call OpenAI with HIGH temperature for variation
        
        Temperature 0.9 = More creative and varied
        Temperature 0.1 = More consistent and predictable
        """
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {
                        "role": "system", 
                        "content": "You are an expert CV writer who creates UNIQUE, VARIED applications that sound like different people wrote them. Never use template language."
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,  # HIGH for variation!
                max_tokens=800
            )
            
            return response.choices[0].message.content
        
        except Exception as e:
            # Fallback to template with variation
            return self._generate_template_with_variation(prompt, temperature)
    
    def _generate_template_with_variation(self, prompt: str, seed: int) -> str:
        """Fallback template with basic variation"""
        random.seed(seed)
        
        # Multiple phrase variations
        openings = [
            "I am writing to express my strong interest",
            "I am excited to apply for",
            "I wish to submit my application for",
            "I would like to be considered for",
            "This is to apply for"
        ]
        
        tquk_mentions = [
            "As a TQUK-certified healthcare professional",
            "Having completed TQUK-endorsed training",
            "With my TQUK-recognized professional development",
            "As a graduate of TQUK Approved Centre training"
        ]
        
        nhs_passion = [
            "I am passionate about supporting the NHS",
            "I am dedicated to NHS values and patient care",
            "I am committed to delivering excellent NHS services",
            "I believe strongly in the NHS mission"
        ]
        
        # Randomly combine
        opening = random.choice(openings)
        tquk = random.choice(tquk_mentions)
        passion = random.choice(nhs_passion)
        
        return f"{opening}...\n\n{tquk}...\n\n{passion}..."


class SynonymReplacer:
    """
    Replace common words with synonyms to create variation
    """
    
    SYNONYMS = {
        'passionate': ['dedicated', 'committed', 'enthusiastic', 'devoted'],
        'experience': ['background', 'expertise', 'knowledge', 'proficiency'],
        'skills': ['abilities', 'competencies', 'capabilities', 'strengths'],
        'qualified': ['certified', 'trained', 'proficient', 'skilled'],
        'understand': ['comprehend', 'grasp', 'appreciate', 'recognize'],
        'excellent': ['outstanding', 'exceptional', 'superior', 'superb'],
        'responsible': ['accountable', 'reliable', 'dependable', 'trustworthy'],
        'achieve': ['accomplish', 'attain', 'reach', 'secure'],
        'improve': ['enhance', 'develop', 'advance', 'strengthen'],
        'ensure': ['guarantee', 'maintain', 'secure', 'confirm']
    }
    
    @staticmethod
    def replace_with_synonyms(text: str, seed: int) -> str:
        """Replace words with synonyms based on seed"""
        random.seed(seed)
        
        for word, synonyms in SynonymReplacer.SYNONYMS.items():
            if word in text.lower():
                # Randomly choose synonym
                synonym = random.choice(synonyms)
                # Replace (case-sensitive)
                text = text.replace(word, synonym)
                text = text.replace(word.capitalize(), synonym.capitalize())
        
        return text


class ApplicationDeduplication:
    """
    Track applications to same job and ensure variation
    """
    
    def __init__(self):
        self.applications_per_job = {}  # job_id -> list of application_ids
    
    def get_variation_level(self, job_id: str) -> int:
        """
        Get variation level based on number of applications to this job
        
        Returns:
            0 = First application (can use standard)
            1-5 = Low variation needed
            6-10 = Medium variation needed
            11+ = HIGH variation needed!
        """
        count = len(self.applications_per_job.get(job_id, []))
        return count
    
    def register_application(self, job_id: str, application_id: str):
        """Register that we applied someone to this job"""
        if job_id not in self.applications_per_job:
            self.applications_per_job[job_id] = []
        
        self.applications_per_job[job_id].append(application_id)
    
    def get_variation_strategy(self, job_id: str) -> Dict:
        """
        Get variation strategy based on application count
        
        Returns guidance on how much to vary
        """
        count = self.get_variation_level(job_id)
        
        if count == 0:
            return {
                'variation_level': 'standard',
                'temperature': 0.7,
                'use_synonyms': False,
                'vary_structure': False
            }
        elif count <= 5:
            return {
                'variation_level': 'low',
                'temperature': 0.8,
                'use_synonyms': True,
                'vary_structure': False,
                'message': 'Using synonym replacement'
            }
        elif count <= 10:
            return {
                'variation_level': 'medium',
                'temperature': 0.9,
                'use_synonyms': True,
                'vary_structure': True,
                'message': 'Using synonyms and structure variation'
            }
        else:
            return {
                'variation_level': 'high',
                'temperature': 1.0,
                'use_synonyms': True,
                'vary_structure': True,
                'vary_examples': True,
                'vary_tone': True,
                'message': f'HIGH VARIATION! {count} students already applied'
            }


# ============================================
# MAIN APPLICATION GENERATOR WITH VARIATION
# ============================================

class VariationAwareApplicationGenerator:
    """
    Application generator that tracks and varies applications
    """
    
    def __init__(self, openai_api_key: str):
        self.variation_engine = TextVariationEngine(openai_api_key)
        self.dedup_tracker = ApplicationDeduplication()
    
    async def generate_application(
        self,
        student: Dict,
        job: Dict,
        tquk_cert: Dict
    ) -> Dict:
        """
        Generate application with appropriate variation
        
        Returns:
            {
                'cv': tailored CV text,
                'cover_letter': varied cover letter,
                'variation_level': how much we varied,
                'applications_to_this_job': count
            }
        """
        
        job_id = job['id']
        student_id = student['id']
        
        # Check how many students already applied
        variation_strategy = self.dedup_tracker.get_variation_strategy(job_id)
        
        # Create variation seed
        variation_seed = int(hashlib.md5(f"{student_id}_{job_id}".encode()).hexdigest(), 16) % 10000
        
        # Generate cover letter with variation
        cover_letter = await self.variation_engine.generate_varied_cover_letter(
            student,
            job,
            tquk_cert,
            variation_seed
        )
        
        # Apply synonym replacement if needed
        if variation_strategy.get('use_synonyms'):
            cover_letter = SynonymReplacer.replace_with_synonyms(cover_letter, variation_seed)
        
        # Generate varied CV sections
        cv_summary = await self.variation_engine.generate_varied_cv_section(
            student, job, 'summary', variation_seed
        )
        
        cv_skills = await self.variation_engine.generate_varied_cv_section(
            student, job, 'skills', variation_seed + 1
        )
        
        # Register this application
        application_id = f"{student_id}_{job_id}"
        self.dedup_tracker.register_application(job_id, application_id)
        
        return {
            'cv_summary': cv_summary,
            'cv_skills': cv_skills,
            'cover_letter': cover_letter,
            'variation_level': variation_strategy['variation_level'],
            'variation_strategy': variation_strategy,
            'applications_to_this_job': self.dedup_tracker.get_variation_level(job_id)
        }


# ============================================
# USAGE EXAMPLE
# ============================================

async def main():
    """
    Example: Apply 20 students to same job with variation
    """
    import os
    
    generator = VariationAwareApplicationGenerator(
        openai_api_key=os.getenv('OPENAI_API_KEY')
    )
    
    # Same job
    job = {
        'id': 'nhs_job_12345',
        'title': 'RTT Validator - Band 4',
        'company': 'London NHS Trust',
        'description': '...'
    }
    
    tquk_cert = {
        'centre_number': '36257481088',
        'course_code': 'PDLC-01-039'
    }
    
    # Apply 20 different students
    for i in range(20):
        student = {
            'id': f'student_{i}',
            'first_name': f'Student{i}',
            'last_name': 'Test'
        }
        
        result = await generator.generate_application(student, job, tquk_cert)
        
        print(f"\n{'='*60}")
        print(f"Student {i+1} - Variation Level: {result['variation_level']}")
        print(f"Applications to this job: {result['applications_to_this_job']}")
        print(f"Strategy: {result['variation_strategy'].get('message', '')}")
        print(f"\nCover Letter Preview:")
        print(result['cover_letter'][:200] + "...")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
