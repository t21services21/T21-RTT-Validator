"""
T21 SERVICES - TWO-FACTOR AUTHENTICATION SETUP
Secure your account with 2FA
"""

import streamlit as st


def render_2fa_setup():
    """Render 2FA setup page"""
    
    # Check if user is logged in
    if not st.session_state.get('logged_in'):
        st.error("⛔ Please login to access this page")
        st.stop()
    
    user_email = st.session_state.get('user_email')
    
    st.title("🔐 Two-Factor Authentication (2FA)")
    st.markdown("Add an extra layer of security to your account")
    
    # Check current 2FA status
    from supabase_database import get_user_by_email
    user_data = get_user_by_email(user_email)
    
    if not user_data:
        st.error("User data not found")
        st.stop()
    
    is_2fa_enabled = user_data.get('two_factor_enabled', False)
    
    if is_2fa_enabled:
        render_2fa_management(user_email, user_data)
    else:
        render_2fa_enable(user_email)


def render_2fa_enable(user_email):
    """Render 2FA enablement flow"""
    
    st.subheader("🛡️ Enable Two-Factor Authentication")
    
    st.info("""
    **Why enable 2FA?**
    - 🔒 Protects against 99% of account compromises
    - ✅ Required for NHS enterprise accounts
    - 🎯 Industry best practice
    - 💼 Professional security standard
    """)
    
    st.markdown("### How it works:")
    st.markdown("""
    1. Scan QR code with your authenticator app
    2. Enter the 6-digit code to verify
    3. Save your backup codes (for emergency access)
    4. Login will require your password + 6-digit code
    """)
    
    st.markdown("### Compatible authenticator apps:")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("📱 **Google Authenticator**")
    with col2:
        st.markdown("🔐 **Microsoft Authenticator**")
    with col3:
        st.markdown("🛡️ **Authy**")
    
    st.markdown("---")
    
    # Setup wizard
    if 'setup_step' not in st.session_state:
        st.session_state.setup_step = 1
    
    if st.session_state.setup_step == 1:
        st.markdown("### Step 1: Generate your QR code")
        
        if st.button("🚀 Start 2FA Setup", type="primary"):
            from two_factor_auth import enable_2fa_for_user
            
            # Generate 2FA credentials
            setup_data = enable_2fa_for_user(user_email)
            
            # Store in session for verification
            st.session_state.temp_2fa_secret = setup_data['secret']
            st.session_state.temp_backup_codes = setup_data['backup_codes']
            st.session_state.qr_base64 = setup_data['qr_base64']
            st.session_state.setup_step = 2
            st.rerun()
    
    elif st.session_state.setup_step == 2:
        st.markdown("### Step 2: Scan QR Code")
        
        st.markdown("**Scan this QR code with your authenticator app:**")
        
        # Display QR code
        qr_base64 = st.session_state.qr_base64
        st.markdown(
            f'<div style="text-align: center;"><img src="data:image/png;base64,{qr_base64}" width="300"></div>',
            unsafe_allow_html=True
        )
        
        st.markdown("**Or enter this code manually:**")
        st.code(st.session_state.temp_2fa_secret, language=None)
        
        st.markdown("---")
        st.markdown("### Step 3: Verify Setup")
        
        verification_code = st.text_input(
            "Enter the 6-digit code from your app:",
            max_chars=6,
            key="verify_code"
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("✅ Verify & Enable 2FA", type="primary"):
                if not verification_code or len(verification_code) != 6:
                    st.error("Please enter a 6-digit code")
                else:
                    from two_factor_auth import verify_2fa_code
                    
                    if verify_2fa_code(st.session_state.temp_2fa_secret, verification_code):
                        # Save to database
                        from supabase_database import enable_2fa
                        
                        if enable_2fa(
                            user_email,
                            st.session_state.temp_2fa_secret,
                            st.session_state.temp_backup_codes
                        ):
                            st.session_state.setup_step = 3
                            st.rerun()
                        else:
                            st.error("Failed to enable 2FA. Please try again.")
                    else:
                        st.error("❌ Invalid code. Please check and try again.")
        
        with col2:
            if st.button("Cancel"):
                st.session_state.setup_step = 1
                st.rerun()
    
    elif st.session_state.setup_step == 3:
        st.success("🎉 2FA Successfully Enabled!")
        
        st.markdown("### ⚠️ IMPORTANT: Save Your Backup Codes")
        st.warning("**Save these backup codes in a secure place!** You'll need them if you lose access to your authenticator app.")
        
        backup_codes = st.session_state.temp_backup_codes
        
        # Display backup codes
        st.code("\n".join(backup_codes), language=None)
        
        # Download button
        backup_text = f"""T21 SERVICES - 2FA BACKUP CODES
Account: {user_email}
Generated: {st.session_state.get('setup_date', 'Unknown')}

KEEP THESE CODES SAFE!
Each code can only be used once.

{chr(10).join(backup_codes)}
"""
        
        st.download_button(
            label="📥 Download Backup Codes",
            data=backup_text,
            file_name=f"t21_2fa_backup_codes_{user_email.split('@')[0]}.txt",
            mime="text/plain"
        )
        
        st.checkbox("✅ I have saved my backup codes in a secure location", key="confirmed_backup")
        
        if st.session_state.get('confirmed_backup'):
            if st.button("🎉 Complete Setup", type="primary"):
                # Clean up session
                del st.session_state.temp_2fa_secret
                del st.session_state.temp_backup_codes
                del st.session_state.qr_base64
                del st.session_state.setup_step
                st.success("Setup complete! 2FA is now protecting your account.")
                st.balloons()
                st.rerun()


def render_2fa_management(user_email, user_data):
    """Render 2FA management for users who already have it enabled"""
    
    st.success("✅ Two-Factor Authentication is **ENABLED**")
    
    st.markdown("### 🛡️ Your Account is Protected")
    
    st.info(f"""
    **2FA Status:** Active  
    **Enabled on:** {user_data.get('two_factor_enabled_at', 'Unknown')[:10]}  
    **Backup codes:** Available
    """)
    
    st.markdown("---")
    
    st.markdown("### ⚙️ Manage 2FA")
    
    tab1, tab2, tab3 = st.tabs(["📋 Backup Codes", "🔄 Reset 2FA", "🚫 Disable 2FA"])
    
    with tab1:
        st.markdown("#### View Backup Codes")
        st.warning("Each backup code can only be used once.")
        
        try:
            import json
            backup_codes = json.loads(user_data.get('two_factor_backup_codes', '[]'))
            
            if backup_codes:
                st.code("\n".join(backup_codes), language=None)
                st.markdown(f"**{len(backup_codes)} backup codes remaining**")
                
                if len(backup_codes) < 3:
                    st.error("⚠️ Running low on backup codes! Consider resetting 2FA to generate new codes.")
            else:
                st.info("No backup codes available. Reset 2FA to generate new codes.")
        
        except:
            st.error("Error loading backup codes")
    
    with tab2:
        st.markdown("#### Reset 2FA")
        st.info("This will generate a new QR code and new backup codes.")
        
        st.warning("**Warning:** Your current authenticator setup will stop working.")
        
        if st.button("🔄 Reset 2FA", type="secondary"):
            # Disable current 2FA
            from supabase_database import disable_2fa
            disable_2fa(user_email)
            
            # Clear session and reload
            st.session_state.setup_step = 1
            st.success("2FA has been reset. Please set it up again.")
            st.rerun()
    
    with tab3:
        st.markdown("#### Disable 2FA")
        st.error("**Not Recommended:** Disabling 2FA makes your account less secure.")
        
        st.warning("You will no longer need a 6-digit code to login.")
        
        confirm_disable = st.checkbox("I understand the security risks")
        
        if confirm_disable:
            if st.button("🚫 Disable 2FA", type="secondary"):
                from supabase_database import disable_2fa
                
                if disable_2fa(user_email):
                    st.success("2FA has been disabled")
                    st.rerun()
                else:
                    st.error("Failed to disable 2FA")


# Run the app
if __name__ == "__main__" or "streamlit" in str(globals()):
    render_2fa_setup()
