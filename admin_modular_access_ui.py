"""
T21 SERVICES - MODULAR ACCESS ADMIN UI
Admin interface for managing granular module access

Features:
- View all modules in hierarchy
- Grant/revoke individual module access
- Sell packages (bundles)
- View user's module access
- Set expiry dates
- Module marketplace
"""

import streamlit as st
from modular_access_system import (
    grant_module_access, revoke_module_access,
    grant_package_access, user_has_module_access,
    get_user_accessible_modules, get_user_module_status,
    list_all_modules, get_available_packages,
    MODULE_HIERARCHY, ACCESS_PACKAGES
)
from student_auth import list_all_students


def render_modular_access_admin():
    """Render the modular access control admin interface"""
    
    st.header("🎯 Modular Access Control")
    st.markdown("**Manage granular access to individual modules and content**")
    
    st.info("""
    💡 **Modular Access System:**
    - Grant access to individual scenarios, courses, or features
    - Create custom packages for different user types
    - Set expiry dates for time-limited access
    - Hierarchical permissions (parent modules grant child access)
    """)
    
    # Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "👤 User Module Access",
        "📦 Packages & Bundles",
        "🗂️ Module Hierarchy",
        "💰 Module Marketplace",
        "📊 Access Analytics"
    ])
    
    with tab1:
        render_user_module_access()
    
    with tab2:
        render_packages_management()
    
    with tab3:
        render_module_hierarchy()
    
    with tab4:
        render_module_marketplace()
    
    with tab5:
        render_access_analytics()


def render_user_module_access():
    """Manage individual user's module access"""
    
    st.subheader("👤 Manage User Module Access")
    
    # Select user
    all_students = list_all_students()
    
    if not all_students:
        st.warning("No users found")
        return
    
    user_options = {f"{s['full_name']} ({s['email']})": s['email'] for s in all_students}
    selected_display = st.selectbox("Select User:", list(user_options.keys()))
    selected_email = user_options[selected_display]
    
    st.markdown("---")
    
    # Get user's current access
    accessible_modules = get_user_accessible_modules(selected_email)
    
    st.markdown(f"### Current Access: {len(accessible_modules)} modules")
    
    if accessible_modules:
        with st.expander("📋 View Current Access", expanded=True):
            for module_id in accessible_modules:
                status = get_user_module_status(selected_email, module_id)
                
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    st.markdown(f"**{module_id}**")
                    if status['days_remaining']:
                        st.caption(f"⏰ Expires in {status['days_remaining']} days")
                    else:
                        st.caption("♾️ Permanent access")
                
                with col2:
                    if status['has_access']:
                        st.success("✅ Active")
                    else:
                        st.error("❌ Expired")
                
                with col3:
                    if st.button("🗑️", key=f"revoke_{module_id}_{selected_email}"):
                        revoke_module_access(selected_email, module_id)
                        st.success(f"Revoked access to {module_id}")
                        st.rerun()
    else:
        st.info("User has no module-specific access. Using role-based defaults.")
    
    st.markdown("---")
    
    # Grant new access
    st.markdown("### ➕ Grant New Module Access")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Get all modules
        all_modules = list_all_modules()
        module_options = {m['name']: m['id'] for m in all_modules}
        
        selected_module_name = st.selectbox(
            "Select Module:",
            list(module_options.keys())
        )
        selected_module_id = module_options[selected_module_name]
    
    with col2:
        expiry_days = st.number_input(
            "Access Duration (days):",
            min_value=0,
            value=90,
            help="0 = Permanent access"
        )
    
    if st.button("✅ Grant Access", type="primary"):
        days = expiry_days if expiry_days > 0 else None
        grant_module_access(selected_email, selected_module_id, days)
        st.success(f"✅ Granted access to {selected_module_name}!")
        st.balloons()
        st.rerun()


def render_packages_management():
    """Manage access packages"""
    
    st.subheader("📦 Access Packages & Bundles")
    
    st.markdown("""
    **Packages** are pre-configured bundles of modules that you can sell as a unit.
    """)
    
    packages = get_available_packages()
    
    for package in packages:
        with st.expander(f"📦 {package['name']} - £{package['price']}", expanded=False):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**Description:** {package['description']}")
                st.markdown(f"**Duration:** {package['duration_days']} days")
                st.markdown(f"**Price:** £{package['price']}")
                
                st.markdown("**Included Modules:**")
                if "all" in package['modules']:
                    st.success("✅ All modules included!")
                else:
                    for module_id in package['modules']:
                        st.markdown(f"- {module_id}")
            
            with col2:
                st.markdown("**Quick Grant:**")
                
                # Select user
                all_students = list_all_students()
                if all_students:
                    user_options = {s['full_name']: s['email'] for s in all_students}
                    selected_user = st.selectbox(
                        "User:",
                        list(user_options.keys()),
                        key=f"pkg_user_{package['id']}"
                    )
                    
                    if st.button(f"📦 Grant Package", key=f"grant_pkg_{package['id']}"):
                        user_email = user_options[selected_user]
                        grant_package_access(user_email, package['id'])
                        st.success(f"✅ Granted {package['name']} to {selected_user}!")
                        st.balloons()
                        st.rerun()
    
    st.markdown("---")
    
    # Create custom package
    st.markdown("### ➕ Create Custom Package")
    
    st.info("💡 Coming soon: Create your own custom packages!")


def render_module_hierarchy():
    """Display module hierarchy"""
    
    st.subheader("🗂️ Module Hierarchy")
    
    st.markdown("""
    **Hierarchical Access:**
    - If a user has access to a parent module, they automatically get access to all child modules
    - Example: Access to "RTT Training" grants access to all scenarios
    """)
    
    st.markdown("---")
    
    def render_hierarchy(hierarchy, level=0):
        for name, data in hierarchy.items():
            indent = "　" * level
            
            if isinstance(data, dict) and "id" in data:
                if data.get("children"):
                    st.markdown(f"{indent}📂 **{name}** (`{data['id']}`)")
                    render_hierarchy(data["children"], level + 1)
                else:
                    st.markdown(f"{indent}📄 {name} (`{data['id']}`)")
    
    render_hierarchy(MODULE_HIERARCHY)


def render_module_marketplace():
    """Module marketplace for selling individual modules"""
    
    st.subheader("💰 Module Marketplace")
    
    st.markdown("""
    **Sell Individual Modules:**
    - Set prices for individual scenarios, courses, or features
    - Users can purchase à la carte
    - Create promotional bundles
    """)
    
    st.info("💡 **Coming soon:** Individual module pricing and checkout!")
    
    st.markdown("---")
    
    # Example pricing
    st.markdown("### 💡 Example Module Pricing:")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**📚 Training Scenarios**")
        st.markdown("- Individual scenario: £29")
        st.markdown("- 5 scenarios bundle: £99")
        st.markdown("- All 40 scenarios: £299")
    
    with col2:
        st.markdown("**🎓 LMS Courses**")
        st.markdown("- Single course: £99-£499")
        st.markdown("- Course bundle (3): £799")
        st.markdown("- Full catalog: £1,499")
    
    with col3:
        st.markdown("**🛠️ Tools Access**")
        st.markdown("- Single tool: £49/month")
        st.markdown("- Tool bundle (5): £199/month")
        st.markdown("- All tools: £299/month")


def render_access_analytics():
    """Analytics on module access usage"""
    
    st.subheader("📊 Access Analytics")
    
    st.markdown("### Module Usage Statistics")
    
    all_students = list_all_students()
    
    if not all_students:
        st.info("No users to analyze")
        return
    
    # Count module access
    module_usage = {}
    
    for student in all_students:
        email = student['email']
        accessible = get_user_accessible_modules(email)
        
        for module_id in accessible:
            module_usage[module_id] = module_usage.get(module_id, 0) + 1
    
    if not module_usage:
        st.info("No module-specific access granted yet")
        return
    
    # Display top modules
    sorted_modules = sorted(module_usage.items(), key=lambda x: x[1], reverse=True)
    
    st.markdown("**Most Accessed Modules:**")
    
    for module_id, count in sorted_modules[:10]:
        percentage = (count / len(all_students)) * 100
        st.markdown(f"**{module_id}:** {count} users ({percentage:.1f}%)")
        st.progress(percentage / 100)
    
    st.markdown("---")
    
    # Summary stats
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Users", len(all_students))
    
    with col2:
        st.metric("Unique Modules Granted", len(module_usage))
    
    with col3:
        total_grants = sum(module_usage.values())
        st.metric("Total Module Grants", total_grants)
