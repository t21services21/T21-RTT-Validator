"""
DEBUG: Check if TQUK Document Library appears in accessible modules
"""

import streamlit as st

st.title("🔍 Debug: Document Library Check")

# Get user info
user_role = st.session_state.get('user_role', 'Not set')
user_email = st.session_state.get('user_email', 'Not set')

st.write(f"**Your Role:** {user_role}")
st.write(f"**Your Email:** {user_email}")

# Check what modules you should see
if user_role == 'super_admin' or 'admin@t21services' in user_email.lower():
    accessible_modules = [
        "🏥 Patient Administration Hub",
        "🎓 Learning Portal",
        "👨‍🏫 Teaching & Assessment",
        "📚 TQUK Document Library",  # THIS ONE!
        "🏥 Clinical Workflows",
        "✅ Task Management",
        "🤖 AI & Automation",
        "📊 Reports & Analytics",
        "🎓 Training & Certification",
        "📚 Level 3 Adult Care",
        "💻 IT User Skills",
        "🤝 Customer Service",
        "📊 Business Administration",
        "🔒 Information Governance",
        "💼 Career Development",
        "📄 CV Builder",
        "⚙️ Administration",
        "ℹ️ Help & Information",
        "📧 Contact & Support"
    ]
elif user_role == 'admin':
    accessible_modules = [
        "🏥 Patient Administration Hub",
        "🎓 Learning Portal",
        "👨‍🏫 Teaching & Assessment",
        "📚 TQUK Document Library",  # THIS ONE!
        "🏥 Clinical Workflows",
        "✅ Task Management",
        "🤖 AI & Automation",
        "📊 Reports & Analytics",
        "🎓 Training & Certification",
        "📚 Level 3 Adult Care",
        "💻 IT User Skills",
        "🤝 Customer Service",
        "📊 Business Administration",
        "🔒 Information Governance",
        "💼 Career Development",
        "📄 CV Builder",
        "⚙️ Administration",
        "ℹ️ Help & Information",
        "📧 Contact & Support"
    ]
else:
    accessible_modules = ["Not admin - limited access"]

st.subheader("📋 Your Accessible Modules:")
st.write(f"**Total modules:** {len(accessible_modules)}")

# Check if TQUK Document Library is in the list
if "📚 TQUK Document Library" in accessible_modules:
    st.success("✅ TQUK Document Library IS in your accessible modules!")
    
    # Find its position
    position = accessible_modules.index("📚 TQUK Document Library") + 1
    st.info(f"📍 Position in list: #{position} out of {len(accessible_modules)}")
else:
    st.error("❌ TQUK Document Library NOT in your accessible modules!")

st.subheader("📜 Full Module List:")
for i, module in enumerate(accessible_modules, 1):
    if "TQUK Document Library" in module:
        st.markdown(f"**{i}. {module}** ← 🎯 THIS IS IT!")
    else:
        st.write(f"{i}. {module}")

st.markdown("---")
st.info("""
**If you see it in this list but not in your sidebar:**
1. The sidebar might be scrollable - scroll down!
2. Try refreshing with Ctrl+F5
3. Check if you're on mobile (sidebar might be collapsed)
4. Browser cache issue - clear cache
""")
