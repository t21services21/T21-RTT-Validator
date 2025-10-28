"""
TQUK EVIDENCE REQUIREMENTS GUIDE
Clear guidance for students on what evidence they need to submit for each unit
"""

import streamlit as st

# Evidence requirements by unit type
EVIDENCE_REQUIREMENTS = {
    "knowledge_unit": {
        "description": "Knowledge-based units require evidence that you understand the theory",
        "required_evidence": [
            {
                "type": "Reflective Account",
                "quantity": "1-2 per unit",
                "description": "Written reflection showing your understanding of key concepts",
                "example": "A 500-word reflection on duty of care principles and how they apply in your workplace"
            },
            {
                "type": "Professional Discussion",
                "quantity": "1 per unit",
                "description": "Recorded discussion with your assessor about the unit topics",
                "example": "15-minute discussion about equality and diversity practices"
            },
            {
                "type": "Written Assignment",
                "quantity": "Optional",
                "description": "Formal written work answering specific questions",
                "example": "Essay on safeguarding policies and procedures"
            }
        ],
        "minimum": "At least 2 pieces of evidence covering all learning outcomes"
    },
    "competence_unit": {
        "description": "Competence units require evidence that you can DO the tasks in practice",
        "required_evidence": [
            {
                "type": "Observation",
                "quantity": "2-3 per unit",
                "description": "Your assessor watches you perform tasks and completes observation records",
                "example": "Assessor observes you providing person-centred care to a service user"
            },
            {
                "type": "Witness Statement",
                "quantity": "1-2 per unit",
                "description": "Your supervisor/colleague confirms your competence in writing",
                "example": "Your manager confirms you communicate effectively with service users"
            },
            {
                "type": "Product Evidence",
                "quantity": "As needed",
                "description": "Documents you've created as part of your work",
                "example": "Care plan you've written, risk assessment you've completed"
            },
            {
                "type": "Reflective Account",
                "quantity": "1-2 per unit",
                "description": "Written reflection on your practice",
                "example": "Reflection on how you handled a challenging situation"
            }
        ],
        "minimum": "At least 3-4 pieces of evidence including observations"
    },
    "mixed_unit": {
        "description": "Mixed units require both knowledge AND competence evidence",
        "required_evidence": [
            {
                "type": "Observation",
                "quantity": "1-2 per unit",
                "description": "Assessor observes you performing tasks",
                "example": "Observation of medication administration"
            },
            {
                "type": "Reflective Account",
                "quantity": "1-2 per unit",
                "description": "Written reflection on theory and practice",
                "example": "Reflection on medication policies and your practice"
            },
            {
                "type": "Professional Discussion",
                "quantity": "1 per unit",
                "description": "Discussion covering knowledge and practice",
                "example": "Discussion about medication management procedures"
            },
            {
                "type": "Witness Statement OR Product Evidence",
                "quantity": "1 per unit",
                "description": "Supporting evidence from workplace",
                "example": "Witness statement or medication records"
            }
        ],
        "minimum": "At least 3 pieces of evidence covering knowledge and practice"
    }
}

# Unit classifications for ALL TQUK COURSES
UNIT_CLASSIFICATIONS = {
    # ============================================
    # LEVEL 3 DIPLOMA IN ADULT CARE
    # ============================================
    "level3_adult_care": {
        1: {"name": "Duty of Care", "type": "knowledge_unit"},
        2: {"name": "Equality, Diversity & Inclusion", "type": "knowledge_unit"},
        3: {"name": "Person-Centred Care", "type": "mixed_unit"},
        4: {"name": "Safeguarding in Care Settings", "type": "mixed_unit"},
        5: {"name": "Effective Communication", "type": "mixed_unit"},
        6: {"name": "Health & Wellbeing", "type": "mixed_unit"},
        7: {"name": "Continuous Professional Development", "type": "knowledge_unit"},
        8: {"name": "Dementia Care", "type": "competence_unit"},
        9: {"name": "Mental Health Awareness", "type": "knowledge_unit"},
        10: {"name": "End of Life Care", "type": "competence_unit"},
        11: {"name": "Medication Management", "type": "competence_unit"},
        12: {"name": "Moving and Handling", "type": "competence_unit"},
    },
    
    # ============================================
    # LEVEL 2 IT USER SKILLS
    # ============================================
    "level2_it_skills": {
        1: {"name": "IT User Fundamentals", "type": "mixed_unit"},
        2: {"name": "Using Email", "type": "competence_unit"},
        3: {"name": "Using the Internet", "type": "competence_unit"},
        4: {"name": "Word Processing Software", "type": "competence_unit"},
        5: {"name": "Spreadsheet Software", "type": "competence_unit"},
        6: {"name": "Database Software", "type": "competence_unit"},
        7: {"name": "Presentation Software", "type": "competence_unit"},
        8: {"name": "IT Security for Users", "type": "knowledge_unit"},
    },
    
    # ============================================
    # LEVEL 2 CUSTOMER SERVICE
    # ============================================
    "level2_customer_service": {
        1: {"name": "Customer Service Principles", "type": "knowledge_unit"},
        2: {"name": "Delivering Customer Service", "type": "competence_unit"},
        3: {"name": "Customer Communication", "type": "mixed_unit"},
        4: {"name": "Handling Customer Complaints", "type": "competence_unit"},
        5: {"name": "Teamwork in Customer Service", "type": "mixed_unit"},
        6: {"name": "Understanding the Organisation", "type": "knowledge_unit"},
    },
    
    # ============================================
    # LEVEL 2 BUSINESS ADMINISTRATION
    # ============================================
    "level2_business_admin": {
        1: {"name": "Business Communication", "type": "mixed_unit"},
        2: {"name": "Principles of Business", "type": "knowledge_unit"},
        3: {"name": "Principles of Administration", "type": "knowledge_unit"},
        4: {"name": "Document Production", "type": "competence_unit"},
        5: {"name": "Manage Diary Systems", "type": "competence_unit"},
        6: {"name": "Produce Business Documents", "type": "competence_unit"},
        7: {"name": "Handle Mail", "type": "competence_unit"},
        8: {"name": "Store and Retrieve Information", "type": "competence_unit"},
    },
    
    # ============================================
    # LEVEL 2 ADULT SOCIAL CARE
    # ============================================
    "level2_adult_social_care": {
        1: {"name": "Introduction to Care", "type": "knowledge_unit"},
        2: {"name": "Duty of Care", "type": "knowledge_unit"},
        3: {"name": "Equality and Inclusion", "type": "knowledge_unit"},
        4: {"name": "Safeguarding", "type": "mixed_unit"},
        5: {"name": "Communication", "type": "mixed_unit"},
        6: {"name": "Personal Development", "type": "knowledge_unit"},
        7: {"name": "Health and Safety", "type": "mixed_unit"},
        8: {"name": "Person-Centred Support", "type": "competence_unit"},
    },
    
    # ============================================
    # LEVEL 3 TEACHING & LEARNING
    # ============================================
    "level3_teaching_learning": {
        1: {"name": "Understanding Roles in Education", "type": "knowledge_unit"},
        2: {"name": "Communication in Education", "type": "mixed_unit"},
        3: {"name": "Equality, Diversity & Inclusion", "type": "knowledge_unit"},
        4: {"name": "Safeguarding in Education", "type": "mixed_unit"},
        5: {"name": "Supporting Learning Activities", "type": "competence_unit"},
        6: {"name": "Assessment for Learning", "type": "mixed_unit"},
        7: {"name": "Professional Development", "type": "knowledge_unit"},
    },
    
    # ============================================
    # FUNCTIONAL SKILLS ENGLISH
    # ============================================
    "functional_skills_english": {
        1: {"name": "Reading Skills", "type": "competence_unit"},
        2: {"name": "Writing Skills", "type": "competence_unit"},
        3: {"name": "Speaking, Listening & Communication", "type": "competence_unit"},
    },
    
    # ============================================
    # FUNCTIONAL SKILLS MATHS
    # ============================================
    "functional_skills_maths": {
        1: {"name": "Number and the Number System", "type": "competence_unit"},
        2: {"name": "Common Measures, Shape and Space", "type": "competence_unit"},
        3: {"name": "Handling Information and Data", "type": "competence_unit"},
    },
}


def render_evidence_requirements_guide(unit_number=None):
    """Render comprehensive evidence requirements guide"""
    
    st.markdown("## 📋 Evidence Requirements Guide")
    st.markdown("### What evidence do I need to submit to pass each unit?")
    
    st.markdown("---")
    
    # If specific unit selected, show detailed requirements
    if unit_number and unit_number in UNIT_CLASSIFICATIONS:
        render_unit_specific_requirements(unit_number)
    else:
        # Show general overview
        render_general_requirements_overview()


def render_unit_specific_requirements(unit_number, course_id="level3_adult_care"):
    """Show detailed requirements for a specific unit"""
    
    # Get course-specific units
    if course_id not in UNIT_CLASSIFICATIONS:
        course_id = "level3_adult_care"  # Default fallback
    
    course_units = UNIT_CLASSIFICATIONS[course_id]
    
    if unit_number not in course_units:
        st.warning(f"Unit {unit_number} not found for this course")
        return
    
    unit_info = course_units[unit_number]
    unit_name = unit_info['name']
    unit_type = unit_info['type']
    requirements = EVIDENCE_REQUIREMENTS[unit_type]
    
    st.markdown(f"### Unit {unit_number}: {unit_name}")
    
    # Unit type badge
    type_badges = {
        "knowledge_unit": "🧠 Knowledge Unit",
        "competence_unit": "⚡ Competence Unit",
        "mixed_unit": "🔄 Mixed Unit (Knowledge + Competence)"
    }
    st.info(f"**Unit Type:** {type_badges[unit_type]}")
    
    st.markdown(requirements['description'])
    
    st.markdown("---")
    
    # Required evidence
    st.markdown("### ✅ Required Evidence:")
    
    for i, evidence in enumerate(requirements['required_evidence'], 1):
        with st.expander(f"📎 {i}. {evidence['type']} - {evidence['quantity']}", expanded=True):
            st.markdown(f"**What is it?**")
            st.write(evidence['description'])
            
            st.markdown(f"**Example:**")
            st.success(evidence['example'])
            
            st.markdown(f"**How many?**")
            st.write(f"➡️ {evidence['quantity']}")
    
    st.markdown("---")
    
    # Minimum requirements
    st.warning(f"**⚠️ Minimum Requirement:** {requirements['minimum']}")
    
    # Tips
    st.markdown("### 💡 Top Tips:")
    st.markdown("""
    1. **Quality over quantity** - One excellent piece of evidence is better than multiple weak ones
    2. **Cross-reference** - One piece of evidence can cover multiple learning outcomes
    3. **Be specific** - Clearly explain which learning outcomes your evidence addresses
    4. **Get feedback** - Ask your assessor if you're unsure about evidence quality
    5. **Keep originals** - Always keep copies of your evidence
    """)


def render_general_requirements_overview():
    """Show overview of all evidence types"""
    
    st.markdown("### 📚 Understanding Evidence Types")
    
    st.info("""
    **There are 6 main types of evidence you can submit:**
    
    Each unit requires different combinations depending on whether it's:
    - 🧠 **Knowledge Unit** (theory-based)
    - ⚡ **Competence Unit** (practical skills)
    - 🔄 **Mixed Unit** (both theory and practice)
    """)
    
    # Evidence types explained
    st.markdown("### 📎 Evidence Types Explained:")
    
    evidence_types = [
        {
            "name": "1. Observation",
            "icon": "👁️",
            "description": "Your assessor watches you work and completes an observation record",
            "when_used": "Competence and mixed units",
            "example": "Assessor observes you providing personal care to a service user",
            "typical_quantity": "2-3 per competence unit"
        },
        {
            "name": "2. Witness Statement",
            "icon": "✍️",
            "description": "Your supervisor or colleague writes a statement confirming your competence",
            "when_used": "Competence and mixed units",
            "example": "Your manager confirms you follow safeguarding procedures correctly",
            "typical_quantity": "1-2 per unit"
        },
        {
            "name": "3. Reflective Account",
            "icon": "💭",
            "description": "You write about your practice, what you learned, and how you'll improve",
            "when_used": "All unit types",
            "example": "500-word reflection on a challenging situation and how you handled it",
            "typical_quantity": "1-2 per unit"
        },
        {
            "name": "4. Product Evidence",
            "icon": "📄",
            "description": "Documents you've created as part of your work",
            "when_used": "Competence and mixed units",
            "example": "Care plan, risk assessment, communication record you've completed",
            "typical_quantity": "As needed"
        },
        {
            "name": "5. Professional Discussion",
            "icon": "💬",
            "description": "Recorded discussion with your assessor about the unit topics",
            "when_used": "Knowledge and mixed units",
            "example": "15-minute discussion about equality and diversity practices",
            "typical_quantity": "1 per knowledge unit"
        },
        {
            "name": "6. Case Study",
            "icon": "📋",
            "description": "Detailed analysis of a care situation you've been involved in",
            "when_used": "All unit types (optional)",
            "example": "Case study of supporting someone with dementia",
            "typical_quantity": "Optional"
        }
    ]
    
    for evidence in evidence_types:
        with st.expander(f"{evidence['icon']} {evidence['name']}", expanded=False):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**What is it?**")
                st.write(evidence['description'])
                
                st.markdown(f"**Example:**")
                st.success(evidence['example'])
            
            with col2:
                st.markdown(f"**When used:**")
                st.info(evidence['when_used'])
                
                st.markdown(f"**How many:**")
                st.warning(evidence['typical_quantity'])
    
    st.markdown("---")
    
    # Quick reference table
    st.markdown("### 📊 Quick Reference: Evidence by Unit Type")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 🧠 Knowledge Units")
        st.markdown("""
        **Examples:** Unit 1, 2, 7
        
        **Required:**
        - ✅ Reflective Account (1-2)
        - ✅ Professional Discussion (1)
        - ✅ Optional: Written work
        
        **Minimum:** 2 pieces
        """)
    
    with col2:
        st.markdown("#### ⚡ Competence Units")
        st.markdown("""
        **Examples:** Unit 8, 10, 11
        
        **Required:**
        - ✅ Observations (2-3)
        - ✅ Witness Statement (1-2)
        - ✅ Product Evidence
        - ✅ Reflective Account (1-2)
        
        **Minimum:** 3-4 pieces
        """)
    
    with col3:
        st.markdown("#### 🔄 Mixed Units")
        st.markdown("""
        **Examples:** Unit 3, 4, 5, 6
        
        **Required:**
        - ✅ Observations (1-2)
        - ✅ Reflective Account (1-2)
        - ✅ Professional Discussion (1)
        - ✅ Witness/Product (1)
        
        **Minimum:** 3 pieces
        """)
    
    st.markdown("---")
    
    # Common questions
    st.markdown("### ❓ Common Questions:")
    
    with st.expander("Can one piece of evidence cover multiple units?"):
        st.write("""
        **Yes!** One piece of evidence can cover multiple units if it demonstrates learning outcomes from both.
        
        **Example:** An observation of you providing personal care could cover:
        - Unit 3: Person-Centred Care
        - Unit 5: Effective Communication
        - Unit 6: Health & Wellbeing
        
        Just make sure to clearly state which learning outcomes it covers for each unit.
        """)
    
    with st.expander("How long should a reflective account be?"):
        st.write("""
        **Typical length:** 500-1000 words
        
        **Quality matters more than length!**
        
        A good reflective account should:
        - Describe the situation
        - Explain what you did
        - Reflect on what you learned
        - Identify how you'll improve
        - Link to theory/policies
        """)
    
    with st.expander("What if I can't get observations at work?"):
        st.write("""
        **Options:**
        1. **Witness Statements** - Ask your supervisor to write about your competence
        2. **Product Evidence** - Use documents you've created
        3. **Professional Discussion** - Discuss scenarios with your assessor
        4. **Simulated Activities** - Your assessor may arrange practice scenarios
        
        **Important:** Speak to your assessor about alternative evidence options.
        """)
    
    with st.expander("How do I know if my evidence is good enough?"):
        st.write("""
        **Good evidence is:**
        - ✅ **Valid** - It demonstrates what it claims to
        - ✅ **Authentic** - It's your own work
        - ✅ **Current** - Recent (within last 2 years)
        - ✅ **Sufficient** - Covers all learning outcomes
        
        **Ask yourself:**
        - Does it clearly show I can do/understand this?
        - Have I explained which learning outcomes it covers?
        - Is it detailed and specific?
        - Does it show real workplace practice?
        """)


def render_unit_evidence_checklist(unit_number):
    """Render a checklist for a specific unit"""
    
    if unit_number not in UNIT_CLASSIFICATIONS:
        return
    
    unit_info = UNIT_CLASSIFICATIONS[unit_number]
    unit_type = unit_info['type']
    requirements = EVIDENCE_REQUIREMENTS[unit_type]
    
    st.markdown(f"### ✅ Evidence Checklist for Unit {unit_number}")
    
    st.markdown("**Track your evidence submission:**")
    
    for evidence in requirements['required_evidence']:
        st.checkbox(
            f"{evidence['type']} - {evidence['quantity']}",
            key=f"checklist_{unit_number}_{evidence['type']}",
            help=evidence['description']
        )
    
    st.markdown("---")
    st.info(f"**Minimum required:** {requirements['minimum']}")


# Quick helper function
def get_unit_evidence_summary(unit_number, course_id="level3_adult_care"):
    """Get a quick summary of evidence requirements for a unit"""
    
    # Get course-specific units
    if course_id not in UNIT_CLASSIFICATIONS:
        course_id = "level3_adult_care"  # Default fallback
    
    course_units = UNIT_CLASSIFICATIONS[course_id]
    
    if unit_number not in course_units:
        return f"Unit {unit_number} not found for this course"
    
    unit_info = course_units[unit_number]
    unit_type = unit_info['type']
    requirements = EVIDENCE_REQUIREMENTS[unit_type]
    
    evidence_list = [f"• {e['type']} ({e['quantity']})" for e in requirements['required_evidence']]
    
    return f"""
**Unit {unit_number}: {unit_info['name']}**

{requirements['description']}

**Required Evidence:**
{chr(10).join(evidence_list)}

**Minimum:** {requirements['minimum']}
"""
