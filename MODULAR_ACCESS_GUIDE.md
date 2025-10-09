# 🎯 T21 MODULAR ACCESS CONTROL SYSTEM
## Complete Guide to Granular Module & Content Access

**Version:** 1.0  
**Last Updated:** October 2025

---

## 🌟 OVERVIEW

The Modular Access Control System allows you to sell and grant access to **individual pieces of content** rather than entire tools. This creates unlimited revenue opportunities and flexible user experiences.

---

## 💡 KEY CONCEPTS

### **1. Hierarchical Modules**

Modules are organized in a parent-child hierarchy:

```
RTT Training (Parent)
  ├─ Training Library (Child)
  │   ├─ Scenario 1 (Grandchild)
  │   ├─ Scenario 2 (Grandchild)
  │   └─ Scenario 3 (Grandchild)
  ├─ Interactive Learning (Child)
  └─ AI RTT Tutor (Child)
```

**Hierarchical Access Rules:**
- ✅ Access to a **parent** grants access to all **children**
- ✅ Access to "Training Library" = Access to all 40 scenarios
- ✅ Access to individual scenarios = Only that scenario

---

### **2. Module Types**

| Type | Example | Purpose |
|------|---------|---------|
| **Content Segments** | Individual training scenarios | Smallest sellable unit |
| **Features** | AI Tutor, Quiz Mode | Specific functionality |
| **Tools** | Pathway Validator | Complete tool |
| **Courses** | Individual LMS courses | Educational content |
| **Tool Groups** | All RTT Tools | Bundle of related tools |

---

### **3. Access Packages (Bundles)**

Pre-configured bundles of modules:

| Package | Price | Modules Included |
|---------|-------|------------------|
| **RTT Essentials** | £299 | 5 scenarios + basic tools |
| **RTT Professional** | £599 | All 40 scenarios + AI Tutor |
| **RTT Master** | £999 | Everything + Certification |
| **Full Platform** | £1,499 | Complete access to all modules |

---

## 🏗️ SYSTEM ARCHITECTURE

### **Module Hierarchy Definition**

Located in: `modular_access_system.py`

```python
MODULE_HIERARCHY = {
    "RTT Training": {
        "id": "rtt_training",
        "children": {
            "Training Library": {
                "id": "training_library",
                "children": {
                    "Scenario 1": {"id": "scenario_01"},
                    "Scenario 2": {"id": "scenario_02"},
                    # ...
                }
            }
        }
    }
}
```

### **Database Structure**

**File:** `user_module_access.json`

```json
{
  "user@email.com": {
    "scenario_01": {
      "granted_at": "2025-01-01T00:00:00",
      "expires_at": "2025-04-01T00:00:00",
      "status": "active"
    },
    "training_library": {
      "granted_at": "2025-01-01T00:00:00",
      "expires_at": null,
      "status": "active"
    }
  }
}
```

---

## 🎯 USE CASES

### **Use Case 1: Sell Individual Scenarios**

**Scenario:** Student wants to practice DNA scenarios

**Solution:**
```python
# Grant access to specific scenarios
grant_module_access("student@email.com", "scenario_04", expiry_days=90)
grant_module_access("student@email.com", "scenario_05", expiry_days=90)
```

**Pricing:** £29 per scenario

---

### **Use Case 2: Bundle Packages**

**Scenario:** Student wants 5 scenarios at a discount

**Solution:**
```python
# Grant RTT Essentials package
grant_package_access("student@email.com", "rtt_essentials")
```

**Includes:**
- scenario_01, scenario_02, scenario_03, scenario_04, scenario_05
- pathway_validator

**Pricing:** £99 (save £46!)

---

### **Use Case 3: Time-Limited Access**

**Scenario:** Give staff 3-month access to specific tools

**Solution:**
```python
# Grant 90-day access
grant_module_access("staff@nhs.uk", "pathway_validator", expiry_days=90)
```

**After 90 days:** Access automatically expires

---

### **Use Case 4: Hierarchical Access**

**Scenario:** Grant access to all training scenarios

**Solution:**
```python
# Grant parent module
grant_module_access("student@email.com", "training_library")
```

**Result:** Student gets access to ALL 40 scenarios automatically!

---

## 🎨 USER EXPERIENCE

### **For Students:**

#### **1. Browse Marketplace**

Navigate to: `🛒 Module Marketplace`

Features:
- 📦 View package deals
- 🗂️ Browse individual modules
- ✅ See what you own
- 🔒 See what's locked
- 🛒 Request access with 1 click

#### **2. Locked Content**

When accessing locked content:
```
🔒 This scenario is locked

Preview:
"The patient was referred on 01/01/2024 for..." [Locked]

Unlock this scenario:
- Purchase individual scenario (£29)
- Get 5 scenarios bundle (£99)
- Get full Training Library access (£299)

[📧 Request Access]
```

#### **3. Access Indicators**

Throughout the platform:
- ✅ = You have access
- 🔒 = Locked (can purchase)
- ⏰ = Access expiring soon

---

### **For Admins:**

#### **Admin Panel → 🎯 Modular Access**

**5 Tabs:**

1. **👤 User Module Access**
   - Select any user
   - View their access
   - Grant/revoke individual modules
   - Set expiry dates

2. **📦 Packages & Bundles**
   - Pre-configured packages
   - Quick grant to users
   - View what's included

3. **🗂️ Module Hierarchy**
   - Visual tree of all modules
   - See parent-child relationships

4. **💰 Module Marketplace**
   - Set pricing
   - Create promotional bundles

5. **📊 Access Analytics**
   - Most accessed modules
   - Usage statistics
   - Revenue tracking

---

## 💰 MONETIZATION STRATEGIES

### **Strategy 1: À La Carte Pricing**

Sell individual pieces:
- **Single scenario:** £29
- **Single course:** £99-£499
- **Single tool:** £49/month

**Target:** Users who need specific content

---

### **Strategy 2: Bundle Discounts**

Create attractive bundles:
- **5 scenarios:** £99 (save 30%)
- **10 scenarios:** £199 (save 40%)
- **All 40 scenarios:** £299 (save 60%)

**Target:** Value-conscious buyers

---

### **Strategy 3: Subscription Tiers**

Monthly/annual subscriptions:
- **Basic (£49/month):** 10 scenarios + 2 tools
- **Pro (£99/month):** 40 scenarios + all tools
- **Enterprise (£199/month):** Everything

**Target:** Regular users

---

### **Strategy 4: Time-Limited Access**

Rent vs. Buy:
- **7-day access:** £19
- **30-day access:** £49
- **Lifetime access:** £99

**Target:** Students studying for exams

---

### **Strategy 5: Corporate Licensing**

NHS Trust packages:
- **50 users:** £5,000/year
- **100 users:** £8,000/year
- **Unlimited:** £15,000/year

**Custom module selection per trust**

---

## 🔧 ADMIN OPERATIONS

### **Granting Access**

#### **Method 1: Individual Module**

```
Admin Panel → Modular Access → User Module Access

1. Select user: John Smith (john@email.com)
2. Select module: scenario_01
3. Set duration: 90 days
4. Click "Grant Access"
```

#### **Method 2: Package**

```
Admin Panel → Modular Access → Packages & Bundles

1. Find package: RTT Professional
2. Select user from dropdown
3. Click "Grant Package"
```

#### **Method 3: Bulk Grant (Coming Soon)**

Grant module to multiple users at once

---

### **Revoking Access**

```
Admin Panel → Modular Access → User Module Access

1. Select user
2. View current access
3. Click 🗑️ button next to module
4. Access revoked immediately
```

---

### **Checking User Access**

```python
# In code
has_access = user_has_module_access("user@email.com", "scenario_01")

# Returns: True or False
```

---

## 📊 ANALYTICS & REPORTING

### **Available Metrics:**

1. **Module Usage**
   - Most accessed modules
   - Least accessed modules
   - Access frequency

2. **Revenue Tracking**
   - Revenue per module
   - Revenue per package
   - Total module revenue

3. **User Insights**
   - Modules owned per user
   - Average modules per user
   - Most popular user journeys

4. **Expiry Tracking**
   - Upcoming expirations
   - Expired access
   - Renewal opportunities

---

## 🚀 IMPLEMENTATION EXAMPLES

### **Example 1: Student Workflow**

```
1. Student browses Training Library
   └─ Sees 40 scenarios
   └─ 5 are ✅ (owned)
   └─ 35 are 🔒 (locked)

2. Student clicks locked scenario
   └─ Sees preview (first 200 chars)
   └─ Sees pricing options
   └─ Clicks "Request Access"

3. Admin receives request
   └─ Processes payment (external)
   └─ Grants access via Admin Panel

4. Student refreshes
   └─ Scenario now ✅ (unlocked)
   └─ Can practice immediately!
```

---

### **Example 2: Package Purchase**

```
1. Student visits Marketplace
   └─ Sees "RTT Professional" for £599
   └─ Clicks "View Details"
   └─ Sees all 40 scenarios + AI Tutor included

2. Student clicks "Request Package"
   └─ Request sent to admin

3. Admin processes
   └─ Takes payment (external)
   └─ Admin Panel → Packages → Grant Package

4. Student gets instant access
   └─ All 40 scenarios unlock
   └─ AI Tutor unlocks
   └─ Dashboard shows new modules
```

---

## 🔐 SECURITY & PERMISSIONS

### **Access Validation:**

Every time content loads:
```python
# Check access before showing
if user_has_module_access(user_email, module_id):
    show_full_content()
else:
    show_preview_with_upgrade_prompt()
```

### **Expiry Handling:**

Automatic expiry checking:
```python
# Check if expired
status = get_user_module_status(user_email, module_id)

if not status['has_access']:
    show_upgrade_prompt()
```

---

## 📋 BEST PRACTICES

### **For Admins:**

1. ✅ **Always set expiry dates** for trial access
2. ✅ **Use packages** for better value proposition
3. ✅ **Monitor analytics** to optimize pricing
4. ✅ **Grant parent modules** when possible (easier management)
5. ✅ **Send reminder emails** before expiry

### **For Developers:**

1. ✅ **Always check access** before showing content
2. ✅ **Show upgrade prompts** for locked content
3. ✅ **Use hierarchical access** to simplify logic
4. ✅ **Cache access checks** for performance
5. ✅ **Log access requests** for analytics

---

## 🎓 TRAINING SCENARIOS

**All 40 scenarios support modular access:**

```
scenario_01, scenario_02, ... scenario_40
```

**Each can be:**
- Sold individually
- Bundled in packages
- Time-limited
- Gifted to users

---

## 🔮 FUTURE ENHANCEMENTS

### **Phase 2:**
- Payment integration (Stripe)
- Automatic access on payment
- Renewal reminders
- Gift vouchers

### **Phase 3:**
- Dynamic pricing
- Promotional discounts
- Referral bonuses
- Affiliate program

### **Phase 4:**
- Usage-based pricing
- Pay-per-use
- Credits system
- Module marketplace

---

## 📞 SUPPORT

**For Access Issues:**
- Email: admin@t21services.co.uk
- Support: In-app "Request Access" button

**For Pricing Questions:**
- Contact admin for custom packages
- Bulk discounts available

---

## 🏆 BENEFITS

### **For Students:**
- ✅ Pay only for what you need
- ✅ Try before buying
- ✅ Flexible access periods
- ✅ Clear pricing

### **For Admins:**
- ✅ Unlimited revenue options
- ✅ Easy to manage
- ✅ Detailed analytics
- ✅ Flexible packages

### **For Business:**
- ✅ Higher lifetime value
- ✅ More conversion points
- ✅ Better retention
- ✅ Upsell opportunities

---

**🎯 MODULAR ACCESS = MAXIMUM FLEXIBILITY + MAXIMUM REVENUE**

