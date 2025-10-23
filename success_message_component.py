"""
REUSABLE SUCCESS MESSAGE COMPONENT
Huge, animated, impossible-to-miss success messages for all modules
"""

import streamlit as st


def show_huge_success(title, subtitle="", details=None, next_steps=None):
    """
    Display a HUGE, impossible-to-miss success message
    
    Args:
        title: Main success message (e.g., "PATIENT REGISTERED")
        subtitle: Optional subtitle
        details: Dict of details to display (e.g., {"Patient ID": "P123", "Name": "John"})
        next_steps: Optional next steps message
    """
    
    # Balloons animation
    st.balloons()
    
    # HUGE animated banner
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 40px;
        border-radius: 20px;
        text-align: center;
        margin: 30px 0;
        box-shadow: 0 10px 40px rgba(0,0,0,0.3);
        animation: pulse 2s infinite;
    ">
        <h1 style="color: white; font-size: 48px; margin: 0;">✅ SUCCESS!</h1>
        <h2 style="color: white; font-size: 32px; margin: 20px 0;">{title}</h2>
        {f'<p style="color: white; font-size: 20px; margin: 10px 0;">{subtitle}</p>' if subtitle else ''}
    </div>
    
    <style>
    @keyframes pulse {{
        0%, 100% {{ transform: scale(1); }}
        50% {{ transform: scale(1.05); }}
    }}
    </style>
    """, unsafe_allow_html=True)
    
    # Details in a prominent box
    if details:
        details_text = "\n".join([f"**{key}:** `{value}`" for key, value in details.items()])
        st.success(f"""
        ## 📋 DETAILS
        
        {details_text}
        
        ✔️ **Operation completed successfully!**
        """)
    
    # Next steps
    if next_steps:
        st.info(f"💡 **Next Steps:** {next_steps}")


def show_huge_error(title, error_message, suggestions=None):
    """
    Display a HUGE, impossible-to-miss error message
    
    Args:
        title: Main error title (e.g., "REGISTRATION FAILED")
        error_message: Detailed error message
        suggestions: Optional list of suggestions to fix the error
    """
    
    # HUGE error banner
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 40px;
        border-radius: 20px;
        text-align: center;
        margin: 30px 0;
        box-shadow: 0 10px 40px rgba(0,0,0,0.3);
        animation: shake 0.5s;
    ">
        <h1 style="color: white; font-size: 48px; margin: 0;">❌ ERROR!</h1>
        <h2 style="color: white; font-size: 32px; margin: 20px 0;">{title}</h2>
    </div>
    
    <style>
    @keyframes shake {{
        0%, 100% {{ transform: translateX(0); }}
        25% {{ transform: translateX(-10px); }}
        75% {{ transform: translateX(10px); }}
    }}
    </style>
    """, unsafe_allow_html=True)
    
    # Error details
    st.error(f"""
    ## ⚠️ ERROR DETAILS
    
    {error_message}
    """)
    
    # Suggestions
    if suggestions:
        st.warning(f"""
        ## 💡 SUGGESTIONS TO FIX
        
        {chr(10).join([f"- {suggestion}" for suggestion in suggestions])}
        """)


def show_huge_warning(title, warning_message, action_required=None):
    """
    Display a HUGE, impossible-to-miss warning message
    
    Args:
        title: Main warning title
        warning_message: Detailed warning message
        action_required: Optional action required message
    """
    
    # HUGE warning banner
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #f6d365 0%, #fda085 100%);
        padding: 40px;
        border-radius: 20px;
        text-align: center;
        margin: 30px 0;
        box-shadow: 0 10px 40px rgba(0,0,0,0.3);
        animation: pulse 2s infinite;
    ">
        <h1 style="color: white; font-size: 48px; margin: 0;">⚠️ WARNING!</h1>
        <h2 style="color: white; font-size: 32px; margin: 20px 0;">{title}</h2>
    </div>
    
    <style>
    @keyframes pulse {{
        0%, 100% {{ transform: scale(1); }}
        50% {{ transform: scale(1.05); }}
    }}
    </style>
    """, unsafe_allow_html=True)
    
    # Warning details
    st.warning(f"""
    ## ⚠️ WARNING DETAILS
    
    {warning_message}
    """)
    
    # Action required
    if action_required:
        st.info(f"""
        ## 🎯 ACTION REQUIRED
        
        {action_required}
        """)
