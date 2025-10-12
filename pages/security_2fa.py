"""
T21 SERVICES - ACCOUNT SECURITY (2FA SETUP)
"""

import streamlit as st
from navigation import render_navigation


render_navigation(current_page="security")

st.title("🔐 Account Security – Two‑Factor Authentication")

if not st.session_state.get("user_email"):
    st.warning("Please log in first to manage 2FA.")
    st.stop()

email = st.session_state.get("user_email")

st.markdown("---")

# Show current 2FA status from Supabase
status_msg = "Unknown"
try:
    from supabase_database import get_user_by_email
    u = get_user_by_email(email)
    if u:
        status_msg = "Enabled" if u.get("two_factor_enabled") else "Disabled"
except Exception:
    status_msg = "Supabase not reachable"

st.markdown(f"**Current 2FA status:** {status_msg}")

colA, colB = st.columns(2)

with colA:
    st.subheader("Enable 2FA")
    st.markdown("If you haven't enabled 2FA, generate your QR code and backup codes below.")
    if st.button("Generate 2FA Setup", type="primary"):
        from two_factor_auth import enable_2fa_for_user
        setup = enable_2fa_for_user(email)
        st.session_state["_2fa_setup"] = setup
        st.success("Setup generated. Scan the QR code with Google/Microsoft Authenticator.")
    setup = st.session_state.get("_2fa_setup")
    if setup:
        st.markdown("**Scan this QR code with your authenticator app:**")
        st.markdown(
            f'<div style="text-align: center;"><img src="data:image/png;base64,{setup["qr_base64"]}" width="300"></div>',
            unsafe_allow_html=True
        )
        st.markdown("**Or enter this secret manually:**")
        st.code(setup["secret"], language=None)
        st.markdown("**Backup Codes (save these securely):**")
        st.code("\n".join(setup["backup_codes"]))
        
        # Download button for backup codes
        backup_text = f"""T21 SERVICES - 2FA BACKUP CODES
Account: {email}
Generated: {st.session_state.get('setup_date', 'Now')}

KEEP THESE CODES SAFE!
Each code can only be used once.

{chr(10).join(setup["backup_codes"])}
"""
        st.download_button(
            label="📥 Download Backup Codes",
            data=backup_text,
            file_name=f"t21_2fa_backup_{email.split('@')[0]}.txt",
            mime="text/plain"
        )
        
        if st.button("✅ Save to Supabase (Enable 2FA)", type="primary"):
            try:
                from supabase_database import enable_2fa
                ok = enable_2fa(email, setup["secret"], setup["backup_codes"])
                if ok:
                    st.success("✅ 2FA enabled successfully! Test verification below.")
                    del st.session_state["_2fa_setup"]
                    st.rerun()
                else:
                    st.error("Failed to save 2FA to Supabase. Check logs/secrets.")
            except Exception as e:
                st.error(f"Error enabling 2FA: {e}")

    st.markdown("### Verify 2FA")
    code = st.text_input("Enter 6‑digit code from your authenticator:", max_chars=6)
    if st.button("Verify Code"):
        try:
            from two_factor_auth import verify_2fa_code
            # fetch latest secret from Supabase
            from supabase_database import get_user_by_email
            user = get_user_by_email(email)
            secret = user.get("two_factor_secret") if user else None
            if secret and code and len(code) == 6 and verify_2fa_code(secret, code):
                st.success("2FA verification successful.")
            else:
                st.error("Invalid code.")
        except Exception as e:
            st.error(f"Verification error: {e}")

with colB:
    st.subheader("Disable 2FA")
    st.warning("Only use this if you lose access to your authenticator and have no backup codes.")
    if st.button("Disable 2FA", type="secondary"):
        try:
            from supabase_database import disable_2fa
            ok = disable_2fa(email)
            if ok:
                st.success("2FA disabled for your account in Supabase.")
            else:
                st.error("Could not disable 2FA.")
        except Exception as e:
            st.error(f"Error disabling 2FA: {e}")

st.markdown("---")

st.caption("Use the Security page to manage your 2FA. Keep backup codes safe.")
