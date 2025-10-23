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
    
    # AUTO-SCROLL TO TOP
    st.markdown("""
    <script>
        window.scrollTo({top: 0, behavior: 'smooth'});
    </script>
    """, unsafe_allow_html=True)
    
    # HUGE FIXED POSITION OVERLAY (IMPOSSIBLE TO MISS!)
    st.markdown(f"""
    <div id="success-overlay" style="
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.8);
        z-index: 9999;
        display: flex;
        align-items: center;
        justify-content: center;
        animation: fadeIn 0.3s;
    ">
        <div style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 60px;
            border-radius: 30px;
            text-align: center;
            max-width: 600px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.5);
            animation: bounceIn 0.5s;
        ">
            <h1 style="color: white; font-size: 72px; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">✅ SUCCESS!</h1>
            <h2 style="color: white; font-size: 42px; margin: 20px 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">{title}</h2>
            {f'<p style="color: white; font-size: 24px; margin: 10px 0;">{subtitle}</p>' if subtitle else ''}
            <p style="color: white; font-size: 16px; margin-top: 30px; opacity: 0.9;">This message will disappear in 3 seconds...</p>
        </div>
    </div>
    
    <style>
    @keyframes fadeIn {{
        from {{ opacity: 0; }}
        to {{ opacity: 1; }}
    }}
    
    @keyframes bounceIn {{
        0% {{ transform: scale(0.3); opacity: 0; }}
        50% {{ transform: scale(1.05); }}
        70% {{ transform: scale(0.9); }}
        100% {{ transform: scale(1); opacity: 1; }}
    }}
    
    @keyframes pulse {{
        0%, 100% {{ transform: scale(1); }}
        50% {{ transform: scale(1.05); }}
    }}
    </style>
    
    <script>
        // Auto-hide after 3 seconds
        setTimeout(function() {{
            var overlay = document.getElementById('success-overlay');
            if (overlay) {{
                overlay.style.animation = 'fadeOut 0.5s';
                overlay.style.opacity = '0';
                setTimeout(function() {{
                    overlay.style.display = 'none';
                }}, 500);
            }}
        }}, 3000);
    </script>
    """, unsafe_allow_html=True)
    
    # ALSO show normal banner below (for after overlay disappears)
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
