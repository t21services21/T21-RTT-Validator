"""
Quick utility to check if SendGrid is configured in Streamlit Cloud
Run this to verify email system configuration
"""

import streamlit as st

st.title("🔍 SendGrid Configuration Checker")

st.info("This page checks if SendGrid is properly configured for email sending.")

# Check 1: SendGrid package
st.subheader("1. SendGrid Package")
try:
    from sendgrid import SendGridAPIClient
    st.success("✅ SendGrid package is installed")
except ImportError:
    st.error("❌ SendGrid package NOT installed")
    st.code("pip install sendgrid")

# Check 2: API Key in secrets
st.subheader("2. SendGrid API Key")
try:
    api_key = st.secrets.get("SENDGRID_API_KEY")
    if api_key:
        # Don't show full key for security
        masked_key = api_key[:10] + "..." + api_key[-4:] if len(api_key) > 14 else "***"
        st.success(f"✅ SendGrid API Key is configured: `{masked_key}`")
    else:
        st.error("❌ SENDGRID_API_KEY not found in secrets")
        st.warning("""
        **How to add:**
        1. Go to Streamlit Cloud dashboard
        2. Click on your app
        3. Settings → Secrets
        4. Add: `SENDGRID_API_KEY = "your-key-here"`
        """)
except Exception as e:
    st.error(f"❌ Error accessing secrets: {e}")

# Check 3: From Email
st.subheader("3. From Email Address")
try:
    from_email = st.secrets.get("FROM_EMAIL", "admin@t21services.co.uk")
    st.success(f"✅ From Email: `{from_email}`")
except:
    st.warning("⚠️ FROM_EMAIL not set, using default: admin@t21services.co.uk")

# Check 4: Test email function
st.subheader("4. Test Email Function")
if st.button("🧪 Test Email Function"):
    try:
        from email_service import send_email
        
        test_email = st.text_input("Enter test email address:", "test@example.com")
        
        if test_email:
            with st.spinner("Sending test email..."):
                html = """
                <html>
                <body>
                    <h1>Test Email from T21 Platform</h1>
                    <p>If you received this, SendGrid is configured correctly! ✅</p>
                </body>
                </html>
                """
                
                success = send_email(test_email, "🧪 T21 SendGrid Test", html)
                
                if success:
                    st.success(f"✅ Test email sent successfully to {test_email}!")
                    st.balloons()
                else:
                    st.error("❌ Email sending failed. Check configuration.")
    except Exception as e:
        st.error(f"❌ Error: {e}")

# Summary
st.markdown("---")
st.subheader("📋 Configuration Summary")

config_items = []

# Check all items
try:
    from sendgrid import SendGridAPIClient
    config_items.append(("SendGrid Package", "✅ Installed"))
except:
    config_items.append(("SendGrid Package", "❌ Missing"))

try:
    if st.secrets.get("SENDGRID_API_KEY"):
        config_items.append(("API Key", "✅ Configured"))
    else:
        config_items.append(("API Key", "❌ Missing"))
except:
    config_items.append(("API Key", "❌ Error"))

try:
    from_email = st.secrets.get("FROM_EMAIL")
    config_items.append(("From Email", f"✅ {from_email if from_email else 'Using default'}"))
except:
    config_items.append(("From Email", "⚠️ Using default"))

# Display table
for item, status in config_items:
    col1, col2 = st.columns([1, 2])
    with col1:
        st.write(f"**{item}:**")
    with col2:
        st.write(status)

# Final verdict
st.markdown("---")
all_ok = all("✅" in status for _, status in config_items[:2])  # Package + API key

if all_ok:
    st.success("### ✅ SendGrid is FULLY CONFIGURED and ready to send emails!")
else:
    st.error("### ❌ SendGrid is NOT fully configured")
    st.warning("""
    **To enable email sending:**
    
    1. Sign up at https://sendgrid.com (FREE account)
    2. Get your API key
    3. Add to Streamlit Cloud secrets:
       ```
       SENDGRID_API_KEY = "your-api-key"
       FROM_EMAIL = "admin@t21services.co.uk"
       ```
    4. Restart your app
    5. Come back to this page to verify
    """)
