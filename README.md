# 🏥 T21 RTT Pathway Intelligence (v1.2)

**NHS Referral To Treatment (RTT) Simulation and Validation System**  
*Developed for T21 Services UK*

---

## 📋 Overview

T21 RTT Pathway Intelligence is an advanced training and validation tool for NHS administrative staff, RTT validators, pathway coordinators, and data quality officers. It helps users correctly interpret, validate, and manage referral-to-treatment pathways within the NHS framework.

### 🎯 Key Features

- **✅ Pathway Validator** - Validate complete RTT pathways (0-52 weeks) with breach detection
- **📝 Clinic Letter Interpreter** - Interpret clinic letters and verify action compliance in PAS
- **📅 Timeline Auditor** - Audit chronological event sequences for coding accuracy
- **👤 Patient Registration Validator** - Validate patient demographics and registration data with NHS number checksum
- **📆 Appointment & Booking Checker** - Review booking history for DNAs, cancellations, and RTT impact
- **💬 Comment Line Generator** - Generate standardised T21 PAS comment lines for any RTT event
- **📚 RTT Rules Reference** - Quick reference guide for NHS RTT coding rules

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.8 or higher** ([Download Python](https://www.python.org/downloads/))
- **pip** (comes with Python)

### Installation Steps

1. **Open PowerShell or Command Prompt**

2. **Navigate to the project folder:**
   ```powershell
   cd C:\Users\User\CascadeProjects\T21-RTT-Validator
   ```

3. **Install required packages:**
   ```powershell
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```powershell
   streamlit run app.py
   ```

5. **Your browser will automatically open** to `http://localhost:8501`

   If it doesn't, manually open your browser and go to that address.

---

## 🖥️ Using the Application

### 1️⃣ Pathway Validator

**Purpose:** Validate a complete RTT pathway from referral to treatment

**How to use:**
1. Select "📊 Pathway Validator" from the sidebar
2. Fill in pathway details (specialty, dates, delays)
3. Click "🔍 Validate Pathway"
4. Review the JSON output with:
   - Clock status and weeks elapsed
   - Breach flags (18/26/52 weeks)
   - Recommended actions
   - PAS update instructions

**Example scenario:**
- Referral Date: 02/01/2025
- First Appointment: 10/01/2025
- Treatment Date: 20/02/2025
- Result: 7 weeks, no breach, code 30 (FDT started)

---

### 2️⃣ Clinic Letter Interpreter

**Purpose:** Interpret clinic letters and check if required actions are completed in PAS

**How to use:**
1. Select "📝 Clinic Letter Interpreter"
2. Paste the clinic letter text in the left panel
3. Fill in the PAS summary (what's already recorded) in the right panel
4. Click "🔍 Interpret Letter"
5. Review:
   - Correct RTT code for the outcome
   - Action compliance (what's required vs. what's done)
   - Gaps and PAS updates needed

**Example scenario:**
- Letter says: "List for septoplasty, review in 6 weeks, copy to GP"
- PAS shows: Patient on waiting list, but follow-up not booked
- Result: Code 20, gaps identified, specific PAS fixes provided

---

### 3️⃣ Timeline Auditor

**Purpose:** Audit a chronological sequence of RTT events for coding accuracy

**How to use:**
1. Select "📅 Timeline Auditor"
2. Enter events chronologically (date, description, code)
3. Use "➕ Add Event" to add more events
4. Click "🔍 Audit Timeline"
5. Review:
   - Duplicate code issues
   - Critical/moderate issues
   - Recode suggestions
   - Breach status

**Example scenario:**
- Timeline: 10 → 20 → 20 → 30
- Issue detected: Code 20 used after 30
- Recommendation: Recode post-treatment event to 90

---

### 4️⃣ Patient Registration Validator

**Purpose:** Validate patient registration details before starting RTT pathway

**How to use:**
1. Select "👤 Patient Registration Validator"
2. Fill in patient demographics (name, NHS number, DOB)
3. Enter referral details (source, date, specialty)
4. List uploaded documents
5. Click "✅ Validate Registration"
6. Review:
   - NHS number validation (modulus 11 checksum)
   - Mandatory field completion
   - Date consistency checks
   - Document naming conventions

**Example scenario:**
- NHS Number: 1234567881 → Validation passed
- DOB: 15/03/1985 (age 40) → Consistent
- Missing referral date → Issue flagged
- Result: Warning - fix missing fields before proceeding

---

### 5️⃣ Appointment & Booking Checker

**Purpose:** Review booking history and identify RTT impact of DNAs/cancellations

**How to use:**
1. Select "📆 Appointment & Booking Checker"
2. Enter referral and first appointment dates
3. Document follow-ups, DNAs, and cancellations
4. Specify if surgery is planned
5. Indicate active monitoring status
6. Click "🔍 Check Appointments"
7. Review:
   - RTT impact determination
   - Issues with timing or cancellations
   - Required PAS updates

**Example scenario:**
- First appointment 25 days after referral → Flagged (>3 weeks)
- Hospital cancelled appointment → Issue: clock does NOT pause
- Patient cancelled with personal reason → Clock CAN pause
- Result: Specific guidance on how to code each event

---

### 6️⃣ Comment Line Generator

**Purpose:** Generate standardised PAS comment lines in T21 style

**How to use:**
1. Select "💬 Comment Line Generator"
2. Choose event type (FDT, AM Start, DNA, etc.)
3. Enter key date and RTT code
4. Add procedure name and next actions
5. Indicate if GP letter sent
6. Click "✨ Generate Comment Line"
7. Copy the generated comment into PAS

**Example outputs:**
- FDT: `CS20/02/2025/30 – FDT STARTED (SEPTOPLASTY). PATHWAY CLOSED. GP LETTER SENT.`
- AM: `AM32/10/01/2025 – UNDER REVIEW 12W. FU BOOKED 10/04/2025.`
- DNA: `DNA33/15/01/2025 – FIRST CARE DNA. REBOOK 2W. GP COPY PENDING.`

---

## 📚 RTT Code Reference

| Code | Description | Clock Impact |
|------|-------------|--------------|
| **10** | First activity in pathway | Start |
| **11** | First activity after Active Monitoring/Watchful Wait ends | Restart |
| **12** | First activity following Consultant/AHP referral for NEW condition | Start |
| **20** | Subsequent activity | Continue |
| **21** | Tertiary referral | Transfer responsibility |
| **30** | First definitive treatment | Stop |
| **31** | Active monitoring (patient-initiated) | Pause |
| **32** | Active monitoring (clinician-initiated) | Pause |
| **33** | DNA first care | Special |
| **34** | Decision not to treat | Stop |
| **35** | Patient declined | Stop |
| **36** | Patient died | Stop |
| **90** | FDT occurred previously | Non-RTT |
| **91** | Activity during AM | During AM |
| **92** | Diagnostics only | Non-RTT |

---

## 🔧 Troubleshooting

### Issue: "streamlit is not recognized"
**Solution:** Make sure Python and pip are in your PATH. Try:
```powershell
python -m pip install streamlit
python -m streamlit run app.py
```

### Issue: Port 8501 already in use
**Solution:** Stop the existing Streamlit process or use a different port:
```powershell
streamlit run app.py --server.port 8502
```

### Issue: Module not found errors
**Solution:** Reinstall requirements:
```powershell
pip install --upgrade -r requirements.txt
```

---

## 🎓 Training Notes

### This is a SIMULATION ENVIRONMENT:
- ✅ Use for training and learning
- ✅ Practice RTT validation skills
- ✅ Test different scenarios
- ❌ **DO NOT enter real patient data**
- ❌ **Not for production clinical use**

### Breach Thresholds:
- **18 weeks:** Standard RTT target
- **26 weeks:** Serious wait breach
- **52 weeks:** Critical breach (escalation required)

### Clock Rules:
- **Starts:** Referral received or decision to treat
- **Pauses:** Patient-initiated delays only
- **Stops:** Treatment starts, discharge, patient declines, transfer out

---

## 📞 Support

For issues or questions about the T21 RTT Pathway Intelligence system:
- Review the "ℹ️ About RTT Rules" section in the app
- Check NHS England RTT Guidance v17.0
- Contact T21 Services UK training team

---

## 📄 File Structure

```
T21-RTT-Validator/
│
├── app.py                  # Main Streamlit application
├── rtt_validator.py        # Core validation logic
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

---

## 🔄 Updates & Versions

**Current Version:** 1.2  
**Last Updated:** 2025-10-08

### Version History:
- **v1.2** (2025-10-08): Added Patient Registration Validator, Appointment Checker, and Comment Line Generator
- **v1.1** (2025-10-08): Full web application with Streamlit UI (3 core tools)
- **v1.0** (2025): Initial validation logic and JSON outputs

---

## ⚖️ License & Usage

**Developed for T21 Services UK**  
For NHS training and simulation purposes only.  
No real patient data. Training environment.

---

## 🎯 Next Steps

1. ✅ Install Python and dependencies
2. ✅ Run the application (double-click `RUN_APP.bat`)
3. ✅ Start with **Pathway Validator** for basic scenarios
4. ✅ Try **Clinic Letter Interpreter** with the example letters in `EXAMPLE_SCENARIOS.md`
5. ✅ Use **Timeline Auditor** to check code sequences
6. ✅ Practice **Patient Registration** with NHS number validation
7. ✅ Test **Appointment Checker** for DNA/cancellation scenarios
8. ✅ Generate professional **Comment Lines** for PAS notes
9. ✅ Review the RTT rules reference when needed

**Ready to start? Run:** `streamlit run app.py`

---

*T21 Services UK | NHS RTT Training & Validation | Simulation Environment*
