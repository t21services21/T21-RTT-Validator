"""
T21 SERVICES - ADMIN MODULE ACCESS UI
User-friendly interface for admins to control module access

Features:
- Visual table showing all modules and roles
- Easy checkboxes to toggle access
- Save/reset functionality
- Clear visual feedback
"""

import streamlit as st
import pandas as pd
from module_access_control import (
    load_module_access, 
    save_module_access, 
    get_all_modules, 
    get_all_roles,
    reset_to_defaults,
    grant_user_access,
    revoke_user_access,
    get_user_specific_access,
    can_access_module
)
from student_auth import list_all_students


def render_module_access_admin():
    """Render the module access control admin interface"""
    
    st.header("🔐 Module Access Control")
    st.markdown("**Control which modules each user role can access**")
    
    st.info("💡 **Tip:** Uncheck a box to BLOCK that role from accessing that module.")
    
    # Load current settings
    settings = load_module_access()
    
    # Create tabs for different views
    tab1, tab2, tab3 = st.tabs(["📊 Role-Based Access", "👤 User-Specific Access", "⚙️ Quick Actions"])
    
    with tab1:
        st.subheader("Module Access Matrix")
        st.markdown("*Check/uncheck boxes to grant/revoke access*")
        
        # Create columns for each role
        roles = get_all_roles()
        role_labels = {
            "trial": "48hr Trial",
            "basic": "Basic (£299)",
            "professional": "Pro (£599)",
            "ultimate": "Ultimate (£999)",
            "admin": "Admin",
            "staff": "Staff",
            "nhs_trust": "NHS Trust"
        }
        
        # Initialize session state for changes
        if 'module_access_changes' not in st.session_state:
            st.session_state.module_access_changes = settings.copy()
        
        # Display each module with checkboxes
        modules = get_all_modules()
        
        for module in modules:
            st.markdown(f"**{module}**")
            
            cols = st.columns(len(roles))
            
            for idx, role in enumerate(roles):
                with cols[idx]:
                    current_access = st.session_state.module_access_changes[module].get(role, False)
                    
                    new_access = st.checkbox(
                        role_labels[role],
                        value=current_access,
                        key=f"{module}_{role}"
                    )
                    
                    # Update session state
                    st.session_state.module_access_changes[module][role] = new_access
            
            st.markdown("---")
        
        # Save button
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            if st.button("💾 Save Changes", type="primary"):
                save_module_access(st.session_state.module_access_changes)
                st.success("✅ Module access settings saved!")
                st.balloons()
        
        with col2:
            if st.button("🔄 Reset to Defaults"):
                reset_to_defaults()
                st.session_state.module_access_changes = load_module_access()
                st.success("✅ Reset to default settings!")
                st.rerun()
        
        with col3:
            if st.button("↩️ Reload"):
                st.session_state.module_access_changes = load_module_access()
                st.rerun()
    
    with tab2:
        st.subheader("👤 User-Specific Access Control")
        st.markdown("**Grant or revoke access for individual users (overrides role-based access)**")
        
        st.info("💡 **Use this to:** Give specific users access to modules their role normally can't access, or block specific users from modules.")
        
        # Get all students
        try:
            all_students = list_all_students()
            
            if not all_students:
                st.warning("No students found in database.")
            else:
                # Select user
                user_options = [f"{s['email']} ({s['full_name']}) - {s['role'].title()}" for s in all_students]
                selected_user_display = st.selectbox(
                    "Select User:",
                    user_options,
                    key="selected_user_access"
                )
                
                # Extract email from selection
                selected_email = selected_user_display.split(" ")[0]
                
                # Find selected student details
                selected_student = next((s for s in all_students if s['email'] == selected_email), None)
                
                if selected_student:
                    st.markdown(f"**Managing access for:** {selected_student['full_name']} ({selected_student['email']})")
                    st.markdown(f"**Current Role:** {selected_student['role'].title()} ({selected_student['status']})")
                    
                    st.markdown("---")
                    
                    # Get user's current access (including role-based)
                    user_role = selected_student['role']
                    user_specific = get_user_specific_access(selected_email)
                    
                    st.markdown("### Module Access:")
                    st.caption("✅ = Has Access | ❌ = No Access | 🔹 = Custom Override")
                    
                    # Show all modules with checkboxes
                    modules = get_all_modules()
                    
                    col1, col2 = st.columns([3, 1])
                    
                    for module in modules:
                        with col1:
                            # Check current access
                            has_role_access = can_access_module(module, user_role, None)  # Role-based only
                            has_override = module in user_specific
                            has_access = can_access_module(module, user_role, selected_email)  # Total access
                            
                            # Show module name with status indicator
                            status_icon = "🔹" if has_override else ("✅" if has_role_access else "❌")
                            access_label = f"{status_icon} {module}"
                            
                            if has_override:
                                access_label += f" (Override: {'✅ Granted' if user_specific[module] else '❌ Blocked'})"
                            else:
                                access_label += f" (Role Default: {'✅ Yes' if has_role_access else '❌ No'})"
                            
                            st.markdown(f"**{access_label}**")
                        
                        with col2:
                            # Action buttons
                            if has_override:
                                if st.button("🔄 Reset", key=f"reset_{module}_{selected_email}"):
                                    # Remove override
                                    user_settings = get_user_specific_access(selected_email)
                                    if module in user_settings:
                                        del user_settings[module]
                                    from module_access_control import load_user_specific_access, save_user_specific_access
                                    all_user_settings = load_user_specific_access()
                                    all_user_settings[selected_email] = user_settings
                                    save_user_specific_access(all_user_settings)
                                    st.success(f"Reset {module} to role default!")
                                    st.rerun()
                            else:
                                if has_role_access:
                                    if st.button("❌ Block", key=f"block_{module}_{selected_email}"):
                                        revoke_user_access(selected_email, module)
                                        st.success(f"Blocked {module}!")
                                        st.rerun()
                                else:
                                    if st.button("✅ Grant", key=f"grant_{module}_{selected_email}"):
                                        grant_user_access(selected_email, module)
                                        st.success(f"Granted {module}!")
                                        st.rerun()
                        
                        st.markdown("")
                    
                    st.markdown("---")
                    
                    # Quick actions for this user
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        if st.button("✅ Grant All Modules", key="grant_all"):
                            for m in modules:
                                grant_user_access(selected_email, m)
                            st.success("Granted all modules!")
                            st.rerun()
                    
                    with col2:
                        if st.button("❌ Block All Modules", key="block_all"):
                            for m in modules:
                                revoke_user_access(selected_email, m)
                            st.success("Blocked all modules!")
                            st.rerun()
                    
                    with col3:
                        if st.button("🔄 Reset All to Role Default", key="reset_all"):
                            from module_access_control import load_user_specific_access, save_user_specific_access
                            all_settings = load_user_specific_access()
                            if selected_email in all_settings:
                                del all_settings[selected_email]
                            save_user_specific_access(all_settings)
                            st.success("Reset all to role defaults!")
                            st.rerun()
        
        except Exception as e:
            st.error(f"Error loading students: {e}")
    
    with tab3:
        st.subheader("⚡ Quick Access Presets")
        st.markdown("*Apply common access patterns instantly*")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🔓 Grant Access")
            
            if st.button("✅ Give Trial Users Full Access"):
                for module in get_all_modules():
                    st.session_state.module_access_changes[module]["trial"] = True
                st.success("Trial users now have full access!")
            
            if st.button("✅ Give Basic Users Full Access"):
                for module in get_all_modules():
                    st.session_state.module_access_changes[module]["basic"] = True
                st.success("Basic users now have full access!")
            
            if st.button("✅ Give Staff Full Access"):
                for module in get_all_modules():
                    st.session_state.module_access_changes[module]["staff"] = True
                st.success("Staff now have full access!")
        
        with col2:
            st.markdown("### 🔒 Restrict Access")
            
            if st.button("❌ Block Trial from Career Tools"):
                career_tools = ["💼 Job Interview Prep", "📄 CV Builder"]
                for module in career_tools:
                    st.session_state.module_access_changes[module]["trial"] = False
                st.success("Career tools blocked for trial users!")
            
            if st.button("❌ Block Basic from Advanced Tools"):
                advanced_tools = ["📊 Interactive Reports", "🎓 Certification Exam"]
                for module in advanced_tools:
                    st.session_state.module_access_changes[module]["basic"] = False
                st.success("Advanced tools blocked for basic users!")
            
            if st.button("❌ Block Staff from Student Tools"):
                student_tools = ["💼 Job Interview Prep", "📄 CV Builder", "🎮 Interactive Learning Center"]
                for module in student_tools:
                    st.session_state.module_access_changes[module]["staff"] = False
                st.success("Student tools blocked for staff!")
        
        st.markdown("---")
        st.info("⚠️ **Remember to click 'Save Changes' in the Access Matrix tab to apply these presets!**")
    
    # Summary statistics
    st.markdown("---")
    st.subheader("📊 Access Summary")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        trial_count = sum(1 for m in get_all_modules() if st.session_state.module_access_changes[m].get("trial", False))
        st.metric("Trial Access", f"{trial_count}/20 modules")
    
    with col2:
        basic_count = sum(1 for m in get_all_modules() if st.session_state.module_access_changes[m].get("basic", False))
        st.metric("Basic Access", f"{basic_count}/20 modules")
    
    with col3:
        pro_count = sum(1 for m in get_all_modules() if st.session_state.module_access_changes[m].get("professional", False))
        st.metric("Professional Access", f"{pro_count}/20 modules")
