"""
Mobile Responsive CSS - Makes T21 Platform Perfect on All Devices
Add this to the top of your app.py or landing page
"""

import streamlit as st

def apply_mobile_responsive_css():
    """
    Apply mobile-responsive CSS to make the platform work perfectly on:
    - Mobile phones (portrait & landscape)
    - Tablets
    - Desktop computers
    - Large screens
    """
    
    st.markdown("""
    <style>
        /* ========================================
           UNIVERSAL RESPONSIVE FIXES
           ======================================== */
        
        /* Ensure everything can wrap and doesn't overflow */
        * {
            word-wrap: break-word !important;
            overflow-wrap: break-word !important;
            box-sizing: border-box !important;
        }
        
        /* Fix container max-widths */
        .main, .block-container {
            max-width: 100% !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
        
        /* Fix text elements */
        h1, h2, h3, h4, h5, h6, p, div, span, li {
            max-width: 100% !important;
            white-space: normal !important;
        }
        
        /* ========================================
           MOBILE PHONES (up to 768px)
           ======================================== */
        
        @media (max-width: 768px) {
            /* Reduce heading sizes for mobile */
            h1 {
                font-size: 1.8rem !important;
                line-height: 1.3 !important;
                margin-bottom: 1rem !important;
            }
            
            h2 {
                font-size: 1.5rem !important;
                line-height: 1.3 !important;
                margin-bottom: 0.8rem !important;
            }
            
            h3 {
                font-size: 1.3rem !important;
                line-height: 1.3 !important;
            }
            
            /* Paragraph text */
            p, div, span {
                font-size: 0.95rem !important;
                line-height: 1.6 !important;
            }
            
            /* Fix buttons on mobile */
            .stButton button {
                width: 100% !important;
                white-space: normal !important;
                height: auto !important;
                padding: 12px 16px !important;
                min-height: 44px !important;
                font-size: 1rem !important;
            }
            
            /* Stack columns vertically on mobile */
            .row-widget {
                flex-direction: column !important;
            }
            
            [data-testid="column"] {
                width: 100% !important;
                margin-bottom: 1rem !important;
            }
            
            /* Fix tables on mobile */
            .dataframe {
                font-size: 0.85rem !important;
                overflow-x: auto !important;
            }
            
            /* Fix text inputs */
            .stTextInput input,
            .stTextArea textarea,
            .stSelectbox select {
                font-size: 16px !important; /* Prevents zoom on iOS */
                width: 100% !important;
            }
            
            /* Fix metrics */
            [data-testid="stMetricValue"] {
                font-size: 1.5rem !important;
            }
            
            /* Reduce padding everywhere */
            .element-container {
                padding: 0.5rem 0 !important;
            }
            
            /* Fix expander */
            .streamlit-expanderHeader {
                font-size: 1rem !important;
            }
            
            /* Fix tabs */
            .stTabs [data-baseweb="tab-list"] {
                flex-wrap: wrap !important;
            }
            
            .stTabs [data-baseweb="tab"] {
                white-space: normal !important;
                font-size: 0.9rem !important;
                padding: 8px 12px !important;
            }
            
            /* Fix code blocks */
            pre, code {
                font-size: 0.85rem !important;
                overflow-x: auto !important;
            }
            
            /* Fix images */
            img {
                max-width: 100% !important;
                height: auto !important;
            }
        }
        
        /* ========================================
           TABLETS (769px to 1024px)
           ======================================== */
        
        @media (min-width: 769px) and (max-width: 1024px) {
            h1 {
                font-size: 2.2rem !important;
            }
            
            h2 {
                font-size: 1.8rem !important;
            }
            
            h3 {
                font-size: 1.5rem !important;
            }
            
            .main, .block-container {
                padding-left: 2rem !important;
                padding-right: 2rem !important;
            }
        }
        
        /* ========================================
           DESKTOP (1025px and up)
           ======================================== */
        
        @media (min-width: 1025px) {
            .main, .block-container {
                max-width: 1200px !important;
                margin: 0 auto !important;
            }
        }
        
        /* ========================================
           SPECIFIC FIXES FOR COMMON ISSUES
           ======================================== */
        
        /* Fix long URLs */
        a {
            word-break: break-all !important;
        }
        
        /* Fix dataframes */
        .dataframe-container {
            overflow-x: auto !important;
        }
        
        /* Fix sidebar on mobile */
        @media (max-width: 768px) {
            [data-testid="stSidebar"] {
                width: 80% !important;
                max-width: 300px !important;
            }
        }
        
        /* Fix file uploader */
        .uploadedFile {
            max-width: 100% !important;
        }
        
        /* Fix markdown containers */
        .stMarkdown {
            max-width: 100% !important;
        }
        
        /* Fix plotly charts on mobile */
        @media (max-width: 768px) {
            .js-plotly-plot {
                width: 100% !important;
            }
        }
        
        /* Prevent horizontal scroll */
        body {
            overflow-x: hidden !important;
        }
        
        /* Fix navigation menu on mobile */
        @media (max-width: 768px) {
            header[data-testid="stHeader"] {
                background-color: transparent !important;
            }
            
            /* Fix login/register buttons */
            .stButton > button {
                margin-bottom: 0.5rem !important;
            }
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Also add viewport meta tag
    st.markdown("""
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes">
    """, unsafe_allow_html=True)


# Simple usage function
def make_mobile_friendly():
    """
    Call this function at the start of any Streamlit page to make it mobile-friendly
    """
    apply_mobile_responsive_css()
