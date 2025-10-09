"""
T21 SERVICES - USER MODULE MARKETPLACE
Student-facing marketplace to browse and request access to modules

Features:
- Browse available modules
- View what you have access to
- Request access to locked modules
- View package deals
- See pricing
"""

import streamlit as st
from modular_access_system import (
    get_user_accessible_modules, get_user_module_status,
    user_has_module_access, get_available_packages,
    MODULE_HIERARCHY
)


def render_user_marketplace(user_email):
    """Render marketplace for students to browse and request modules"""
    
    st.header("🛒 Module Marketplace")
    st.markdown("**Unlock individual modules or get package deals!**")
    
    # User's current access summary
    accessible_modules = get_user_accessible_modules(user_email)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("📦 Modules You Own", len(accessible_modules))
    
    with col2:
        st.metric("🔒 Locked Modules", "Many available!")
    
    st.markdown("---")
    
    # Tabs
    tab1, tab2, tab3 = st.tabs([
        "🎁 Package Deals",
        "🗂️ Browse Modules",
        "✅ My Access"
    ])
    
    with tab1:
        render_package_deals(user_email)
    
    with tab2:
        render_browse_modules(user_email)
    
    with tab3:
        render_my_access(user_email, accessible_modules)


def render_package_deals(user_email):
    """Display available packages"""
    
    st.subheader("🎁 Package Deals - Save Money!")
    
    packages = get_available_packages()
    
    for package in packages:
        with st.container():
            # Package header
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                st.markdown(f"### 📦 {package['name']}")
                st.caption(package['description'])
            
            with col2:
                st.markdown(f"### £{package['price']}")
                st.caption(f"{package['duration_days']} days")
            
            with col3:
                if st.button("🛒 Request", key=f"req_pkg_{package['id']}", type="primary"):
                    st.success(f"✅ Request sent for {package['name']}!")
                    st.info("An admin will contact you shortly to process your purchase.")
            
            # Package contents
            with st.expander("📋 What's Included"):
                if "all" in package['modules']:
                    st.success("✅ **FULL ACCESS** to all modules!")
                else:
                    st.markdown("**Included modules:**")
                    for module_id in package['modules']:
                        # Check if user already has it
                        has_it = user_has_module_access(user_email, module_id)
                        icon = "✅" if has_it else "📦"
                        st.markdown(f"{icon} {module_id}")
            
            st.markdown("---")


def render_browse_modules(user_email):
    """Browse individual modules"""
    
    st.subheader("🗂️ Browse Individual Modules")
    
    st.info("💡 **Individual Pricing:**\n- Single scenario: £29\n- Single course: £99-£499\n- Single tool: £49/month")
    
    # RTT Training Scenarios
    st.markdown("### 📚 RTT Training Scenarios")
    
    scenarios_to_show = [
        ("scenario_01", "Scenario 1: Standard Referral", "£29"),
        ("scenario_02", "Scenario 2: Urgent Referral", "£29"),
        ("scenario_03", "Scenario 3: Two Week Wait", "£29"),
        ("scenario_04", "Scenario 4: DNA Appointment", "£29"),
        ("scenario_05", "Scenario 5: Patient Cancellation", "£29"),
    ]
    
    for module_id, name, price in scenarios_to_show:
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            has_access = user_has_module_access(user_email, module_id)
            icon = "✅" if has_access else "🔒"
            st.markdown(f"{icon} {name}")
        
        with col2:
            if has_access:
                st.success("Owned")
            else:
                st.markdown(price)
        
        with col3:
            if not has_access:
                if st.button("🛒 Buy", key=f"buy_{module_id}"):
                    st.success(f"✅ Request sent!")
                    st.info("Admin will contact you to complete purchase.")
    
    st.markdown("---")
    
    # RTT Tools
    st.markdown("### 🛠️ RTT Tools")
    
    tools_to_show = [
        ("pathway_validator", "Pathway Validator", "£49/month"),
        ("clinic_interpreter", "Clinic Letter Interpreter", "£49/month"),
        ("timeline_auditor", "Timeline Auditor", "£49/month"),
    ]
    
    for module_id, name, price in tools_to_show:
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            has_access = user_has_module_access(user_email, module_id)
            icon = "✅" if has_access else "🔒"
            st.markdown(f"{icon} {name}")
        
        with col2:
            if has_access:
                st.success("Owned")
            else:
                st.markdown(price)
        
        with col3:
            if not has_access:
                if st.button("🛒 Subscribe", key=f"sub_{module_id}"):
                    st.success(f"✅ Subscription request sent!")


def render_my_access(user_email, accessible_modules):
    """Show user's current access"""
    
    st.subheader("✅ My Module Access")
    
    if not accessible_modules:
        st.info("You don't have any module-specific access yet. Browse packages to get started!")
        return
    
    st.markdown(f"**You have access to {len(accessible_modules)} modules:**")
    
    for module_id in accessible_modules:
        status = get_user_module_status(user_email, module_id)
        
        with st.container():
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.markdown(f"✅ **{module_id}**")
            
            with col2:
                if status['days_remaining']:
                    if status['days_remaining'] < 30:
                        st.warning(f"⏰ {status['days_remaining']} days left")
                    else:
                        st.info(f"⏰ {status['days_remaining']} days")
                else:
                    st.success("♾️ Lifetime")
            
            with col3:
                if status['days_remaining'] and status['days_remaining'] < 30:
                    if st.button("🔄 Renew", key=f"renew_{module_id}"):
                        st.info("Contact admin to renew access")
            
            st.markdown("---")


def render_upgrade_prompt(module_name, module_id):
    """Show upgrade prompt when user tries to access locked content"""
    
    st.warning(f"🔒 **{module_name} is locked**")
    
    st.markdown("""
    **Unlock this module:**
    
    Choose one of these options:
    1. 💰 **Buy this module individually** - One-time purchase
    2. 📦 **Get a package deal** - Better value!
    3. 🎁 **Upgrade your account** - Full platform access
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🛒 Buy This Module", type="primary"):
            st.success("✅ Request sent to admin!")
    
    with col2:
        if st.button("📦 View Packages"):
            st.session_state.show_marketplace = True
            st.rerun()
    
    with col3:
        if st.button("💎 Upgrade Account"):
            st.info("💰 **Upgrade Options:**\n- Basic: £299 / 3 months\n- Professional: £599 / 6 months\n- Premium: £999 / 12 months")
