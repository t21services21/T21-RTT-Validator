"""
T21 SERVICES - PROFESSIONAL NAVIGATION BAR
Clean corporate design like big companies (Oryx Align, Oodles)
"""

import streamlit as st


def render_navigation_bar():
    """Render professional navigation bar at top of page"""
    
    st.markdown("""
    <style>
        /* Remove default Streamlit padding */
        .block-container {
            padding-top: 0 !important;
            max-width: 100% !important;
        }
        
        /* Professional Navigation Bar */
        .top-nav {
            background: white;
            padding: 15px 50px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin: -1rem -1rem 2rem -1rem;
        }
        
        .nav-logo {
            display: flex;
            align-items: center;
            gap: 12px;
        }
        
        .nav-logo-text {
            font-size: 20px;
            font-weight: 700;
            color: #2c3e50;
            margin: 0;
        }
        
        .nav-subtitle {
            font-size: 11px;
            color: #7f8c8d;
            margin: 0;
        }
        
        .nav-right {
            display: flex;
            gap: 15px;
            align-items: center;
        }
        
        .company-reg {
            font-size: 11px;
            color: #95a5a6;
        }
    </style>
    
    <div class="top-nav">
        <div class="nav-logo">
            <img src="app/static/logo.png" width="50" onerror="this.style.display='none'">
            <div>
                <div class="nav-logo-text">T21 Services Limited</div>
                <div class="nav-subtitle">Healthcare Intelligence Platform</div>
            </div>
        </div>
        <div class="nav-right">
            <span class="company-reg">Co. No: 13091053 | Liverpool, UK 🇬🇧</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
