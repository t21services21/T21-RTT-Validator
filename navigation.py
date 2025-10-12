"""
T21 SERVICES - NAVIGATION COMPONENT
Reusable navigation for all pages
"""

import streamlit as st
import streamlit.components.v1 as components

def navigate_with_clean_url(page_name, page_path):
    """Navigate to a page with browser history support"""
    # Push to browser history and navigate
    components.html(f"""
    <script>
        if (window.parent) {{
            window.parent.history.pushState(
                {{page: '{page_name}'}}, 
                '{page_name}', 
                '{page_path}'
            );
            window.parent.location.href = window.parent.location.origin + '{page_path}';
        }}
    </script>
    """, height=0)
    st.stop()

def render_navigation(current_page="home"):
    """Render navigation bar with Streamlit buttons"""
    
    # Setup history listener for browser back/forward
    components.html("""
    <script>
        // Handle browser back/forward
        window.addEventListener('popstate', function(event) {
            if (event.state && event.state.page) {
                window.parent.location.reload();
            }
        });
        
        // Set initial state if needed
        if (!window.parent.history.state) {
            window.parent.history.replaceState(
                {page: 'current'}, 
                'Current Page', 
                window.parent.location.pathname
            );
        }
    </script>
    """, height=0)
    
    # CSS for navigation
    st.markdown("""
    <style>
        [data-testid="stSidebar"] {display: none;}
        
        /* Remove all top spacing */
        .main .block-container {
            padding-top: 0 !important;
            margin-top: 0 !important;
        }
        
        .main {
            padding-top: 0 !important;
        }
        
        header[data-testid="stHeader"] {
            display: none !important;
        }
        
        /* Navigation button styling */
        .stButton button {
            background: none;
            border: none;
            color: #1a1a1a !important;
            font-weight: 700;
            text-transform: uppercase;
            font-size: 14px;
            padding: 10px 15px;
            cursor: pointer;
        }
        
        .stButton button:hover {
            color: #d4af37 !important;
            background: none;
        }
        
        /* Primary button (HOME) styling */
        .stButton button[kind="primary"] {
            background: #d4af37 !important;
            color: white !important;
        }
        
        .stButton button[kind="primary"]:hover {
            background: #c4a030 !important;
            color: white !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Navigation bar
    st.markdown("""
    <div style='background: rgba(26, 26, 26, 0.95); padding: 15px 60px; margin: -100px -70px 30px -70px; box-shadow: 0 2px 10px rgba(0,0,0,0.3);'>
        <div style='display: flex; justify-content: space-between; align-items: center;'>
            <div style='font-size: 24px; font-weight: 800; color: #d4af37; text-transform: uppercase;'>T21 SERVICES</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation buttons
    col1, col2, col3, col4, col5, col6, col7, col8, col9 = st.columns([2, 1, 1, 1, 1, 1, 1, 1, 1])
    
    with col1:
        st.write("")  # Spacer for logo
    
    with col2:
        if st.button("ABOUT", key="nav_about", use_container_width=True):
            navigate_with_clean_url("About", "/about")
    
    with col3:
        if st.button("SERVICES", key="nav_services", use_container_width=True):
            navigate_with_clean_url("Services", "/services")
    
    with col4:
        if st.button("PRICING", key="nav_pricing", use_container_width=True):
            navigate_with_clean_url("Pricing", "/pricing")
    
    with col5:
        if st.button("CONTACT", key="nav_contact", use_container_width=True):
            navigate_with_clean_url("Contact", "/contact_us")
    
    with col6:
        if st.button("TESTIMONIALS", key="nav_testimonials", use_container_width=True):
            navigate_with_clean_url("Testimonials", "/testimonials")

    with col7:
        if st.button("PROCUREMENT", key="nav_procurement", use_container_width=True):
            navigate_with_clean_url("Procurement", "/procurement")

    with col8:
        if st.button("🏠 HOME", key="nav_home", use_container_width=True, type="primary"):
            navigate_with_clean_url("Home", "/landing_page_clean")
    
    with col9:
        if st.session_state.get("logged_in"):
            if st.button("SECURITY", key="nav_security", use_container_width=True):
                st.switch_page("pages/security_2fa.py")
        else:
            st.write("")
