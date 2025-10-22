"""
SIMPLE Mobile Fix for T21 Platform
This is a lightweight fix that actually works
"""

import streamlit as st

def mobile_friendly():
    """
    Simple mobile-friendly CSS that doesn't break anything
    """
    st.markdown("""
    <style>
        /* Just fix the text wrapping - nothing else */
        @media (max-width: 768px) {
            /* Make text wrap on mobile */
            .main .block-container {
                padding-left: 1rem;
                padding-right: 1rem;
                max-width: 100%;
            }
            
            /* Fix long text */
            p, div, span, h1, h2, h3 {
                word-wrap: break-word;
                overflow-wrap: break-word;
                hyphens: auto;
            }
            
            /* Make buttons full width */
            .stButton > button {
                width: 100%;
            }
            
            /* Smaller font on mobile */
            body {
                font-size: 14px;
            }
        }
    </style>
    """, unsafe_allow_html=True)
