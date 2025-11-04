"""
LOGIN DIAGNOSTIC PAGE
Help students troubleshoot login issues
"""

import streamlit as st
import platform
from datetime import datetime

st.set_page_config(
    page_title="Login Diagnostic - T21 Services",
    page_icon="🔧",
    layout="wide"
)

st.title("🔧 Login Diagnostic Tool")
st.markdown("---")

st.info("📋 **This page helps diagnose login issues. Share the results with support.**")

# Browser Information
st.subheader("🌐 Browser Information")
col1, col2 = st.columns(2)

with col1:
    st.write("**User Agent:**")
    try:
        import streamlit.components.v1 as components
        user_agent = st.experimental_get_query_params().get('user_agent', ['Unknown'])[0]
        st.code(user_agent if user_agent != 'Unknown' else "Unable to detect")
    except:
        st.code("Unable to detect")

with col2:
    st.write("**Platform:**")
    st.code(platform.platform())
    st.write("**Python Version:**")
    st.code(platform.python_version())

# Cookie Test
st.markdown("---")
st.subheader("🍪 Cookie Test")

try:
    import extra_streamlit_components as stx
    
    st.success("✅ Cookie library installed")
    
    # Try to create cookie manager
    try:
        if '_diagnostic_cookie_manager' not in st.session_state:
            st.session_state._diagnostic_cookie_manager = stx.CookieManager(key='diagnostic_cookies')
        
        cookie_manager = st.session_state._diagnostic_cookie_manager
        
        # Test write
        if st.button("Test Cookie Write"):
            try:
                cookie_manager.set(
                    cookie='test_cookie',
                    val='test_value_' + datetime.now().isoformat(),
                    expires_at=datetime.now()
                )
                st.success("✅ Cookie write successful!")
            except Exception as e:
                st.error(f"❌ Cookie write failed: {e}")
        
        # Test read
        st.write("**Current Cookies:**")
        try:
            all_cookies = cookie_manager.get_all()
            if all_cookies:
                st.json(all_cookies)
            else:
                st.warning("⚠️ No cookies found")
        except Exception as e:
            st.error(f"❌ Cookie read failed: {e}")
            
    except Exception as e:
        st.error(f"❌ Cookie manager initialization failed: {e}")
        st.warning("**This means cookies are blocked on this browser!**")
        
except ImportError:
    st.error("❌ Cookie library not installed")
    st.code("pip install extra-streamlit-components")

# Session State Test
st.markdown("---")
st.subheader("💾 Session State Test")

if st.button("Test Session State"):
    st.session_state.test_value = datetime.now().isoformat()
    st.success(f"✅ Session state working: {st.session_state.test_value}")

if 'test_value' in st.session_state:
    st.info(f"📌 Stored value: {st.session_state.test_value}")

# Login Status
st.markdown("---")
st.subheader("🔐 Current Login Status")

if st.session_state.get('logged_in'):
    st.success("✅ You are logged in!")
    st.write(f"**Email:** {st.session_state.get('user_email', 'Unknown')}")
    st.write(f"**Session Email:** {st.session_state.get('session_email', 'Unknown')}")
else:
    st.warning("⚠️ You are NOT logged in")

# Recommendations
st.markdown("---")
st.subheader("💡 Troubleshooting Steps")

st.markdown("""
### If you're having login issues:

**1. Clear Browser Cache**
- Press `Ctrl + Shift + Delete`
- Select "All time"
- Check "Cookies" and "Cached images"
- Click "Clear data"
- Restart browser

**2. Check Browser Settings**
- Go to Settings → Privacy
- Ensure cookies are enabled
- Disable "Block third-party cookies"

**3. Try Different Browser**
- Chrome (recommended)
- Edge
- Firefox

**4. Disable Extensions**
- Ad blockers can interfere
- Privacy extensions can block cookies
- Try disabling all extensions

**5. Check Antivirus/Firewall**
- Some antivirus software blocks Streamlit
- Try temporarily disabling
- Add t21-healthcare-platform.streamlit.app to whitelist

**6. Use Incognito Mode**
- Press `Ctrl + Shift + N`
- If it works in incognito, it's a cache/extension issue

### Still not working?

Contact support with:
- Screenshot of this page
- Browser name and version
- Operating system
- Error message (if any)
""")

# Contact Info
st.markdown("---")
st.info("📧 **Support:** admin@t21services.co.uk")
