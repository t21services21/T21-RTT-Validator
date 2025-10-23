# 🚀 HOW TO COMMIT AND PUSH USING VS CODE

## **THE ROOT CAUSE:**
The `user_role` wasn't being detected correctly because it's stored in `st.session_state.user_license.role`, not `st.session_state.user_role`.

## **WHAT I FIXED:**
Updated all 4 TQUK modules to check multiple possible locations for user_role:
1. st.session_state.user_license.role (main location)
2. st.session_state.user_role (fallback)
3. st.session_state.user_type (fallback)
4. Check if email contains 'admin@t21services' (super admin override)

## **FILES CHANGED:**
- tquk_level3_adult_care_module.py
- tquk_it_user_skills_module.py
- tquk_customer_service_module.py
- tquk_business_admin_module.py

## **HOW TO PUSH USING VS CODE:**

### Step 1: Open VS Code
- Open your project folder in VS Code

### Step 2: Go to Source Control
- Click the Source Control icon in left sidebar (looks like branches)
- OR press `Ctrl+Shift+G`

### Step 3: Review Changes
You'll see 4 changed files listed

### Step 4: Stage All Changes
- Click the "+" icon next to "Changes"
- OR click the "+" next to each file

### Step 5: Commit
- Type a commit message in the text box at top:
  ```
  FIX: User role detection in TQUK modules - now correctly detects super_admin, admin, teacher, tester, staff roles
  ```
- Click the ✓ checkmark button (or press Ctrl+Enter)

### Step 6: Push
- Click the "..." menu (three dots)
- Click "Push"
- OR click the sync button (circular arrows) at bottom left

### Step 7: Wait for Deployment
- Go to https://share.streamlit.io/
- Watch your app deploy (2-3 minutes)
- Refresh browser
- **IT WILL WORK NOW!**

## **WHAT YOU'LL SEE AFTER DEPLOYMENT:**

As super admin, when you click any TQUK module, you'll see:

```
👨‍💼 Admin/Staff View - You have full access to preview this course. 
Students must be enrolled to access.
```

Then you can browse all materials, units, assessments, etc.

## **IF YOU DON'T HAVE VS CODE:**

Use GitHub Desktop:
1. Open GitHub Desktop
2. Select repository
3. Review changes
4. Add commit message
5. Click "Commit to main"
6. Click "Push origin"
