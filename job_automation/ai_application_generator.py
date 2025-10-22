"""
AI APPLICATION GENERATOR
Uses GPT-4 to generate unique, tailored supporting information for job applications
Creates application records in database ready for submission
"""

import openai
import os
from datetime import datetime
from supabase_database import supabase, SUPABASE_AVAILABLE

def generate_supporting_information(job_title, job_description, trust_name, student_qualifications=None):
    """
    Generate AI-powered supporting information for a job application
    
    Args:
        job_title: The NHS job title
        job_description: Full job description from NHS Jobs
        trust_name: NHS Trust name
        student_qualifications: Student's T21 qualifications and experience
    
    Returns:
        Tuple of (supporting_information_text, word_count, generation_time)
    """
    
    try:
        # Get OpenAI API key from environment or Streamlit secrets
        try:
            import streamlit as st
            api_key = st.secrets.get("OPENAI_API_KEY")
        except:
            api_key = os.environ.get("OPENAI_API_KEY")
        
        if not api_key:
            print("❌ OpenAI API key not found")
            return None, 0, 0
        
        openai.api_key = api_key
        
        # Build prompt
        prompt = f"""You are an expert NHS job application writer. Write compelling supporting information for this job application.

**Job Details:**
- Title: {job_title}
- Trust: {trust_name}
- Description: {job_description[:500]}...

**Student Qualifications:**
{student_qualifications if student_qualifications else '''
- Completed T21 RTT Pathway Intelligence Training
- TQUK-Endorsed Professional Development Certificate
- Expert in NHS RTT validation and pathway management
- Skilled in patient administration systems (PAS)
- Understanding of NHS referral management
- Knowledge of 18-week RTT standards
- Experience with clinic bookings and pathway tracking
'''}

**Requirements:**
1. Write in first person
2. Demonstrate enthusiasm for NHS and patient care
3. Highlight relevant T21 training and RTT expertise
4. Show understanding of NHS values (compassion, respect, excellence)
5. Mention specific skills relevant to the role
6. Keep it professional and compelling
7. Length: 300-400 words
8. Do NOT include any placeholder text like [Your Name] or [Add detail here]
9. Make it ready to submit as-is

Write the supporting information now:"""
        
        start_time = datetime.now()
        
        # Call GPT-4
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert NHS job application writer who creates compelling, professional supporting statements."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=600
        )
        
        end_time = datetime.now()
        generation_time = (end_time - start_time).total_seconds()
        
        supporting_info = response.choices[0].message.content.strip()
        word_count = len(supporting_info.split())
        
        print(f"✅ Generated {word_count} words in {generation_time:.2f}s")
        
        return supporting_info, word_count, generation_time
    
    except Exception as e:
        print(f"❌ Error generating AI content: {str(e)}")
        return None, 0, 0

def create_applications_for_student(student_id, max_applications=10):
    """
    Generate applications for a specific student based on discovered jobs
    
    Args:
        student_id: UUID of the student
        max_applications: Maximum number of applications to create
    
    Returns:
        Number of applications created
    """
    
    if not SUPABASE_AVAILABLE or supabase is None:
        print("❌ Supabase not available")
        return 0
    
    try:
        # Get student settings
        student = supabase.table('student_automation_settings').select('*, users(email)').eq('student_id', student_id).execute()
        
        if not student.data:
            print(f"❌ Student not found: {student_id}")
            return 0
        
        student_data = student.data[0]
        student_email = student_data.get('users', {}).get('email', 'Unknown')
        
        print(f"\n👤 Generating applications for: {student_email}")
        
        # Get student preferences
        locations = student_data.get('preferred_locations', [])
        bands = student_data.get('preferred_bands', [])
        requires_sponsorship = student_data.get('requires_sponsorship', False)
        max_per_day = student_data.get('max_applications_per_day', 50)
        
        # Get today's application count
        today = datetime.now().date().isoformat()
        today_apps = supabase.table('applications').select('id', count='exact').eq('student_id', student_id).gte('created_at', today).execute()
        
        applications_today = today_apps.count if today_apps else 0
        
        if applications_today >= max_per_day:
            print(f"⏸️ Daily limit reached ({applications_today}/{max_per_day})")
            return 0
        
        remaining = min(max_per_day - applications_today, max_applications)
        
        # Get matching jobs that student hasn't applied to yet
        jobs = supabase.table('discovered_jobs').select('*').eq('status', 'active').execute()
        
        if not jobs.data:
            print("ℹ️ No active jobs found")
            return 0
        
        # Filter jobs
        matching_jobs = []
        for job in jobs.data:
            # Check if already applied
            existing = supabase.table('applications').select('id').eq('student_id', student_id).eq('job_id', job['id']).execute()
            if existing.data:
                continue
            
            # Check criteria
            job_location = job.get('location', '')
            job_band = job.get('band', '')
            
            location_match = any(loc.lower() in job_location.lower() for loc in locations) if locations else True
            band_match = any(band.lower() in job_band.lower() for band in bands) if bands else True
            
            if location_match and band_match:
                matching_jobs.append(job)
        
        if not matching_jobs:
            print("ℹ️ No matching jobs found")
            return 0
        
        print(f"📊 Found {len(matching_jobs)} matching jobs")
        print(f"🎯 Creating up to {remaining} applications")
        
        created_count = 0
        
        for job in matching_jobs[:remaining]:
            try:
                print(f"\n📝 Creating application for: {job.get('title', 'Unknown')}")
                
                # Generate AI supporting information
                supporting_info, word_count, gen_time = generate_supporting_information(
                    job_title=job.get('title', ''),
                    job_description=job.get('description', job.get('title', '')),
                    trust_name=job.get('trust', '')
                )
                
                if not supporting_info:
                    print("⚠️ Failed to generate AI content, skipping")
                    continue
                
                # Create application record
                application = {
                    'student_id': student_id,
                    'job_id': job['id'],
                    'status': 'queued',
                    'ai_supporting_information': supporting_info,
                    'ai_word_count': word_count,
                    'ai_generation_time': gen_time,
                    'priority': 'normal',
                    'attempts': 0,
                    'created_at': datetime.now().isoformat()
                }
                
                result = supabase.table('applications').insert(application).execute()
                
                if result.data:
                    created_count += 1
                    print(f"✅ Application created (#{created_count})")
            
            except Exception as e:
                print(f"⚠️ Error creating application: {str(e)}")
                continue
        
        print(f"\n✅ Created {created_count} applications for {student_email}")
        return created_count
    
    except Exception as e:
        print(f"❌ Error creating applications: {str(e)}")
        return 0

def generate_applications_for_all_students():
    """Generate applications for all active students"""
    
    if not SUPABASE_AVAILABLE or supabase is None:
        print("❌ Supabase not available")
        return
    
    try:
        # Get all active students
        students = supabase.table('student_automation_settings').select('student_id, users(email)').eq('status', 'active').execute()
        
        if not students.data:
            print("ℹ️ No active students found")
            return
        
        print(f"🤖 Generating applications for {len(students.data)} students")
        print("=" * 60)
        
        total_created = 0
        
        for student in students.data:
            created = create_applications_for_student(student['student_id'], max_applications=10)
            total_created += created
        
        print("\n" + "=" * 60)
        print(f"✅ COMPLETE: Created {total_created} applications total")
    
    except Exception as e:
        print(f"❌ Error generating for all students: {str(e)}")

if __name__ == "__main__":
    print("🤖 AI Application Generator")
    print("=" * 60)
    generate_applications_for_all_students()
