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
    
    st.subheader("📚 Select Your Optional Units")
    
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
