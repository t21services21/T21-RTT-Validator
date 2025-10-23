"""
TQUK OPTIONAL UNITS SELECTION SYSTEM
Allows students to select optional units to reach required credits
"""

import streamlit as st
from datetime import datetime

# Import Supabase client
try:
    from supabase_client import get_supabase_client
except ImportError:
    def get_supabase_client():
        try:
            from supabase_database import supabase
            return supabase
        except:
            return None


def get_available_optional_units(course_id):
    """Get all available optional units for a course"""
    supabase = get_supabase_client()
    if not supabase:
        return []
    
    try:
        response = supabase.table('tquk_optional_units').select('*').eq('course_id', course_id).execute()
        return response.data if response.data else []
    except Exception as e:
        st.error(f"Error loading optional units: {str(e)}")
        return []


def get_student_selected_units(learner_email, course_id):
    """Get units selected by a student"""
    supabase = get_supabase_client()
    if not supabase:
        return []
    
    try:
        response = supabase.table('tquk_student_optional_units').select('*').eq('learner_email', learner_email).eq('course_id', course_id).execute()
        return response.data if response.data else []
    except Exception as e:
        st.error(f"Error loading selected units: {str(e)}")
        return []


def select_optional_unit(learner_email, course_id, unit_number, unit_name, credits):
    """Student selects an optional unit"""
    supabase = get_supabase_client()
    if not supabase:
        return False
    
    try:
        data = {
            'learner_email': learner_email,
            'course_id': course_id,
            'unit_number': unit_number,
            'unit_name': unit_name,
            'credits': credits,
            'selected_date': datetime.now().isoformat(),
            'status': 'selected'
        }
        
        response = supabase.table('tquk_student_optional_units').insert(data).execute()
        return True
    except Exception as e:
        st.error(f"Error selecting unit: {str(e)}")
        return False


def remove_optional_unit(learner_email, course_id, unit_number):
    """Student removes an optional unit"""
    supabase = get_supabase_client()
    if not supabase:
        return False
    
    try:
        response = supabase.table('tquk_student_optional_units').delete().eq('learner_email', learner_email).eq('course_id', course_id).eq('unit_number', unit_number).execute()
        return True
    except Exception as e:
        st.error(f"Error removing unit: {str(e)}")
        return False


def calculate_total_credits(learner_email, course_id, mandatory_credits=24):
    """Calculate total credits (mandatory + optional)"""
    selected_units = get_student_selected_units(learner_email, course_id)
    optional_credits = sum(unit['credits'] for unit in selected_units)
    return mandatory_credits + optional_credits


def render_optional_units_selector(learner_email, course_id, required_credits=58, mandatory_credits=24):
    """Render the optional units selection interface"""
    
    st.subheader("🎯 Step 1: Choose Your Optional Units")
    
    st.info("""
    **📋 How to Complete This Qualification:**
    - ✅ You've already completed 7 mandatory units (24 credits)
    - 🎯 Now choose **34 credits** from the optional units below
    - 📚 Study the materials for your chosen units
    - 📝 Submit evidence for each unit
    - 🎓 Get your certificate when complete!
    """)
    
    # Calculate current credits
    selected_units = get_student_selected_units(learner_email, course_id)
    total_credits = calculate_total_credits(learner_email, course_id, mandatory_credits)
    credits_needed = required_credits - total_credits
    
    # Progress bar
    progress = min(total_credits / required_credits, 1.0)
    st.progress(progress, text=f"Credits: {total_credits}/{required_credits}")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Mandatory Credits", mandatory_credits)
    with col2:
        st.metric("Optional Credits", total_credits - mandatory_credits)
    with col3:
        if credits_needed > 0:
            st.metric("Credits Needed", credits_needed, delta=f"-{credits_needed}")
        else:
            st.metric("Credits Complete", "✅", delta="Ready!")
    
    st.markdown("---")
    
    # Show selected units
    if selected_units:
        st.success(f"✅ **You've selected {len(selected_units)} optional units:**")
        
        for unit in selected_units:
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.write(f"**Unit {unit['unit_number']}: {unit['unit_name']}**")
            with col2:
                st.write(f"{unit['credits']} credits")
            with col3:
                if st.button("Remove", key=f"remove_{unit['unit_number']}"):
                    if remove_optional_unit(learner_email, course_id, unit['unit_number']):
                        st.success("Unit removed!")
                        st.rerun()
        
        st.markdown("---")
    
    # Show available units
    if credits_needed > 0:
        st.info(f"💡 **Select {credits_needed} more credits to complete your qualification**")
        
        available_units = get_available_optional_units(course_id)
        selected_unit_numbers = [u['unit_number'] for u in selected_units]
        
        # Filter out already selected units
        available_units = [u for u in available_units if u['unit_number'] not in selected_unit_numbers]
        
        if available_units:
            # Group by category
            categories = {}
            for unit in available_units:
                cat = unit.get('category', 'other')
                if cat not in categories:
                    categories[cat] = []
                categories[cat].append(unit)
            
            # Display by category
            for category, units in categories.items():
                with st.expander(f"📂 {category.replace('_', ' ').title()} ({len(units)} units)"):
                    for unit in units:
                        col1, col2, col3 = st.columns([3, 1, 1])
                        with col1:
                            st.write(f"**Unit {unit['unit_number']}: {unit['unit_name']}**")
                            if unit.get('description'):
                                st.caption(unit['description'])
                        with col2:
                            st.write(f"{unit['credits']} credits")
                            st.caption(f"{unit.get('learning_outcomes', 0)} outcomes")
                        with col3:
                            if st.button("Select", key=f"select_{unit['unit_number']}", type="primary"):
                                if select_optional_unit(learner_email, course_id, unit['unit_number'], unit['unit_name'], unit['credits']):
                                    st.success(f"✅ Added {unit['unit_name']}!")
                                    st.rerun()
    else:
        st.success("🎉 **You've selected enough credits! You can now complete your qualification.**")
        st.info("You can still add more optional units if you want to expand your knowledge.")


def render_optional_units_content(learner_email, course_id, UNITS):
    """Render learning materials for selected optional units"""
    from tquk_pdf_converter import create_unit_pdf
    
    st.markdown("---")
    st.markdown("---")
    
    st.subheader("📖 Step 2: Study Your Selected Units")
    
    # Get selected units
    selected_units = get_student_selected_units(learner_email, course_id)
    
    if not selected_units:
        st.info("👆 **First, select your optional units above!**")
        st.write("""
        **How it works:**
        1. ✅ Choose units from the list above
        2. 📚 Come back here to study them
        3. 📝 Submit evidence in the Assessments tab
        """)
        return
    
    st.success(f"🎓 **You have {len(selected_units)} units ready to study!**")
    st.write("Select any unit below to view full learning materials, activities, and assessment guidance.")
    st.markdown("---")
    
    # Dropdown to select which unit to view
    unit_options = {unit['unit_number']: f"Unit {unit['unit_number']}: {unit['unit_name']} ({unit['credits']} credits)" 
                    for unit in selected_units}
    
    selected_unit_num = st.selectbox(
        "Select Unit to View:",
        options=list(unit_options.keys()),
        format_func=lambda x: unit_options[x],
        key="view_optional_unit"
    )
    
    if selected_unit_num and selected_unit_num in UNITS:
        unit_data = UNITS[selected_unit_num]
        
        # Unit header
        st.markdown(f"## 🎯 Unit {selected_unit_num}: {unit_data['name']}")
        st.caption(f"Optional Unit • {unit_data.get('credits', 3)} Credits")
        
        # Unit info cards
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Learning Outcomes", unit_data['learning_outcomes'])
        with col2:
            st.metric("Activities", unit_data['activities'])
        with col3:
            st.metric("Credits", unit_data.get('credits', 3))
        
        st.markdown("---")
        
        # Load and display content
        try:
            # Load markdown file
            def load_markdown_file(filename):
                try:
                    with open(filename, 'r', encoding='utf-8') as f:
                        return f.read()
                except Exception as e:
                    return f"Error loading file: {str(e)}"
            
            content = load_markdown_file(unit_data['file'])
            
            if content and not content.startswith("Error"):
                with st.container():
                    st.markdown(content, unsafe_allow_html=True)
                
                st.markdown("---")
                
                # Interactive elements
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button(f"✅ Mark Unit {selected_unit_num} Complete", key=f"complete_opt_{selected_unit_num}", type="primary"):
                        st.success(f"✅ Unit {selected_unit_num} marked as complete!")
                
                with col2:
                    if st.button(f"📝 Go to Assessment", key=f"assess_opt_{selected_unit_num}"):
                        st.info("Switch to the 'Assessments' tab to submit your evidence!")
                
                # Download option
                try:
                    pdf_buffer = create_unit_pdf(selected_unit_num, unit_data['name'], content)
                    st.download_button(
                        label=f"📥 Download Unit {selected_unit_num} as PDF",
                        data=pdf_buffer,
                        file_name=f"Level3_Unit{selected_unit_num}_{unit_data['name'].replace(' ', '_')}.pdf",
                        mime="application/pdf",
                        help="Download professional PDF document",
                        key=f"download_opt_{selected_unit_num}",
                        type="primary"
                    )
                except Exception as e:
                    st.error(f"PDF generation error: {str(e)}")
                    st.download_button(
                        label=f"📥 Download Unit {selected_unit_num} (Markdown)",
                        data=content,
                        file_name=f"Level3_Unit{selected_unit_num}_{unit_data['name'].replace(' ', '_')}.md",
                        mime="text/markdown",
                        key=f"download_md_opt_{selected_unit_num}"
                    )
            else:
                st.warning(f"⚠️ Materials for Unit {selected_unit_num} are being prepared.")
                st.info("""
                **What's included in this unit:**
                - Learning outcomes and assessment criteria
                - Real-world scenarios and case studies
                - Activities and reflective exercises
                - Assessment guidance
                
                Full materials will be available soon!
                """)
        except Exception as e:
            st.error(f"Error loading materials: {str(e)}")
            st.info("Please contact your teacher if this persists.")
