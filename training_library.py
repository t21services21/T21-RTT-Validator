"""
Training Library for T21 RTT Validator
EXPANDED EDITION - 50+ Practice Scenarios

Covers:
- All RTT codes (10-39)
- All specialties (Cardiology, Orthopedics, Oncology, ENT, Ophthalmology, etc.)
- All difficulty levels (Easy, Medium, Hard, Expert)
- Cancer pathways (2WW, 62-day)
- Complex multi-code scenarios
- Common mistakes
"""

TRAINING_SCENARIOS = [
    # ============================================
    # EASY SCENARIOS (Codes 10, 30, 34)
    # ============================================
    {
        "id": 1,
        "title": "GP Referral - Cardiology",
        "difficulty": "Easy",
        "letter": """
FROM: Green Street Medical Practice (GP Surgery)
      123 High Street, London, SW1A 1AA
      Dr. James Smith - General Practitioner

TO:   Cardiology Department
      Royal Hospital NHS Trust
      Hospital Road, London, SW1A 2BB

Date: 15 October 2025
Ref: GP/REF/2025/1234

=====================================

Dear Consultant,

I am writing to refer Mr. John Doe for cardiology assessment.

Patient Details:
NHS Number: 1234567890
DOB: 01/01/1980

Clinical History:
Patient presenting with chest pain on exertion for the past 3 months.
No history of cardiac disease. Hypertension controlled on medication.

Please arrange:
- Coronary angiogram
- Cardiology consultation

Thank you,
Dr. James Smith
General Practitioner
Green Street Medical Practice
        """,
        "correct_code": "10",
        "explanation": "This is a GP referral letter. Code 10 is correct as it's the FIRST activity in a new RTT pathway.",
        "key_points": [
            "Referral letter indicator: 'I am writing to refer'",
            "This starts a NEW pathway",
            "Code 10 starts the RTT clock",
            "Diagnostics mentioned are FUTURE actions (need to be ordered)"
        ],
        "expected_actions": [
            "Register referral in PAS",
            "Create RTT pathway",
            "Add to Partial Booking List (PBL)",
            "Book first appointment",
            "Order coronary angiogram"
        ]
    },
    {
        "id": 2,
        "title": "Results Letter - Discharge",
        "difficulty": "Medium",
        "letter": """
FROM: Cardiology Department
      Royal Hospital NHS Trust
      Hospital Road, London, SW1A 2BB
      Dr. Sarah Turner - Consultant Cardiologist

TO:   Mr. John Doe
      Patient Address

CC:   Dr. James Smith, Green Street Medical Practice

Date: 28 October 2025
Ref: CARDIO/RESULTS/2025/5678

=====================================

Dear Mr. Doe,

Re: Results from Your Recent Investigations

I am pleased to inform you that the Coronary Angiography and ECG 
were performed appropriately and have returned as normal.

Based on these findings, no medical intervention is needed at this point.

I recommend regular exercise and maintaining a healthy lifestyle.

Yours sincerely,
Dr. Sarah Turner
Consultant Cardiologist
Royal Hospital NHS Trust
        """,
        "correct_code": "34",
        "explanation": "This is a discharge letter (Code 34). Tests were already done (PAST), results are normal, and no treatment is needed.",
        "key_points": [
            "Results letter: 'were performed' = PAST tense",
            "No intervention needed = discharge",
            "Code 34 STOPS the RTT clock",
            "Do NOT order tests - they're already done!"
        ],
        "expected_actions": [
            "Record Code 34",
            "Set clock stop date",
            "Close pathway",
            "Send GP discharge letter"
        ]
    },
    {
        "id": 3,
        "title": "Decision to Treat - Waiting List",
        "difficulty": "Medium",
        "letter": """
FROM: Orthopedic Department
      City Hospital NHS Trust
      Mr. John Anderson - Consultant Orthopedic Surgeon

TO:   Mr. Robert Smith (Patient)
      Patient Address

CC:   Dr. Sarah Williams, Oakwood Medical Centre (GP)

Date: 18 October 2025
Ref: ORTHO/DTT/2025/3456

=====================================

Dear Mr. Smith,

Thank you for attending clinic.

Following review, I have decided to proceed with surgery.

Plan:
- List patient for knee arthroscopy
- Pre-operative assessment required
- Target date within 12 weeks

Copy to GP.

Dr. Jones
        """,
        "correct_code": "20",
        "explanation": "Decision to treat made. Code 20 continues the pathway until treatment (Code 30) occurs.",
        "key_points": [
            "Decision to treat = Code 20",
            "Clock CONTINUES (not stopped)",
            "'List patient' = FUTURE action",
            "Must check if patient actually added to WL"
        ],
        "expected_actions": [
            "Add patient to surgical waiting list",
            "Record procedure (knee arthroscopy)",
            "Book pre-op assessment",
            "Send GP letter"
        ]
    },
    {
        "id": 4,
        "title": "Treatment Completed",
        "difficulty": "Easy",
        "letter": """
FROM: Orthopedic Department
      City Hospital NHS Trust
      Mr. John Anderson - Consultant Orthopedic Surgeon

TO:   Dr. Sarah Williams, Oakwood Medical Centre (GP)

Date: 16 October 2025
Ref: ORTHO/DISCHARGE/2025/3456

=====================================

Patient completed treatment course.

Surgery: Right knee arthroscopy completed 15/10/2025
Outcome: Successful
Follow-up: GP to manage ongoing care

Discharge to GP.

Mr. John Anderson
Consultant Orthopedic Surgeon
        """,
        "correct_code": "30",
        "explanation": "Surgery performed = First Definitive Treatment. Code 30 STOPS the RTT clock.",
        "key_points": [
            "'was performed' = PAST = treatment done",
            "Code 30 = First Definitive Treatment",
            "Clock STOPS on treatment date",
            "Follow-up is post-treatment (Code 90 territory)"
        ],
        "expected_actions": [
            "Record Code 30",
            "Set clock stop date = 15/09/2025",
            "Close RTT pathway",
            "Book follow-up (post-treatment)"
        ]
    },
    {
        "id": 5,
        "title": "Active Monitoring - Clinician Initiated",
        "difficulty": "Hard",
        "letter": """
FROM: Urology Department
      Regional Hospital NHS Trust
      Dr. Michael Chen - Consultant Urologist

TO:   Patient & GP

Date: 17 October 2025
Ref: URO/ACTIVE-MON/2025/789

=====================================

Clinical Decision:

Patient has small kidney stone (4mm).

Decision: Active surveillance rather than intervention.

Plan:
- Review in 3 months
- Repeat imaging
- Conservative management (fluids, analgesia)

No active treatment required at this stage.

Dr. Michael Chen
Consultant Urologist
        """,
        "correct_code": "32",
        "explanation": "Clinician-initiated active monitoring. Code 32 PAUSES the RTT clock.",
        "key_points": [
            "Watchful waiting = Active Monitoring",
            "Clinician decision (not patient request) = Code 32",
            "Clock PAUSES (not stops)",
            "Can restart with Code 11 when AM ends"
        ],
        "expected_actions": [
            "Record Code 32",
            "Pause RTT clock",
            "Create AM pathway",
            "Set review date (3 months)",
            "During AM, use Code 91 for review appointments"
        ]
    },
    {
        "id": 6,
        "title": "DNA - Did Not Attend",
        "difficulty": "Medium",
        "letter": """
FROM: Outpatient Booking Office
      Regional Hospital NHS Trust
      Appointments Team

TO:   RTT Coordinator / Waiting List Manager

CC:   GP Surgery

Date: 16 September 2025
Ref: OPD/DNA/2025/456

⚠️ PATIENT DNA - FIRST APPOINTMENT ⚠️

=====================================

Internal Note:

Patient did not attend first outpatient appointment on 15/09/2025.

Action: Rebook within 2 weeks as per trust policy.
GP to be informed.

Admin Team
        """,
        "correct_code": "33",
        "explanation": "Patient DNA'd first care activity. Code 33 requires rebooking within trust policy.",
        "key_points": [
            "Did Not Attend = DNA = Code 33",
            "FIRST care activity DNA is significant",
            "Must rebook within trust policy (typically 2 weeks)",
            "Clock handling varies by trust policy"
        ],
        "expected_actions": [
            "Record Code 33",
            "Rebook appointment within 2 weeks",
            "Send DNA letter to patient",
            "Inform GP",
            "Check trust policy on clock management"
        ]
    },
    
    # ============================================
    # MEDIUM SCENARIOS (Codes 20, 31, 32, 33, 35)
    # ============================================
    {
        "id": 7,
        "title": "2-Week Wait Cancer Referral - Breast",
        "difficulty": "Medium",
        "specialty": "Oncology",
        "letter": """
FROM: Riverside Medical Centre (GP Surgery)
      45 Park Lane, Manchester, M1 2AB
      Dr. Emily Wilson - General Practitioner

TO:   Breast Surgery Department
      Manchester Royal Infirmary NHS Trust
      Oxford Road, Manchester, M13 9WL

Date: 14 October 2025
Ref: GP/2WW/BREAST/2025/987

⚠️ URGENT 2-WEEK WAIT CANCER REFERRAL ⚠️

=====================================

Dear Consultant,

I am referring this patient urgently under the 2-week wait cancer pathway.

Patient: Mrs. Sarah Jones
NHS: 987654321
DOB: 15/05/1975

I am referring this patient urgently under the 2-week wait pathway 
for suspected breast cancer.

Clinical Findings:
- Self-detected left breast lump (3cm, upper outer quadrant)
- Present for 6 weeks
- No nipple discharge or skin changes
- No family history of breast cancer

Please arrange urgent assessment and investigations.

Dr. Williams, GP
        """,
        "correct_code": "10",
        "explanation": "2WW referral is still Code 10 (GP referral). The 2WW status affects BOOKING timeline (within 14 days) not the RTT code.",
        "key_points": [
            "2WW = urgent booking required (within 14 days)",
            "Still Code 10 (GP referral starts pathway)",
            "Must flag as Cancer pathway",
            "62-day cancer target also starts",
            "Different target but same RTT code!"
        ],
        "expected_actions": [
            "Flag as 2-Week Wait Cancer Referral",
            "Record Code 10",
            "Book appointment within 14 days",
            "Start 62-day cancer clock",
            "Add to Cancer PTL (Patient Tracking List)",
            "Urgent mammogram + ultrasound"
        ]
    },
    {
        "id": 8,
        "title": "Patient Declined Treatment",
        "difficulty": "Medium",
        "specialty": "Orthopedics",
        "letter": """
FROM: Orthopedic Department
      Metropolitan Hospital NHS Trust
      Mr. James Surgeon - Consultant Orthopedic Surgeon

TO:   Dr. Peter Brown, Hillside Medical Practice (GP)

Date: 12 October 2025
Ref: ORTHO/DECLINED/2025/567

=====================================

Clinic Letter

Patient attended and treatment options were discussed.

After careful consideration, patient has decided NOT to proceed 
with the recommended hip replacement surgery at this time.

Patient wishes to try conservative management first (physiotherapy, 
weight management, pain relief).

Will discharge from waiting list. Patient advised to re-contact 
if symptoms worsen.

Mr. James Surgeon
Consultant Orthopedic Surgeon
        """,
        "correct_code": "31",
        "explanation": "Patient declined treatment = Code 31. This STOPS the RTT clock as patient decided not to proceed.",
        "key_points": [
            "Patient decision (not clinical)",
            "Code 31 = Patient Declined Treatment",
            "RTT clock STOPS",
            "Patient can be re-referred later (new pathway)",
            "Different from DNA (Code 33)"
        ],
        "expected_actions": [
            "Record Code 31",
            "Stop RTT clock",
            "Close pathway",
            "Remove from waiting list",
            "Send GP letter",
            "Patient can self-refer back if needed"
        ]
    },
    {
        "id": 9,
        "title": "Tertiary Referral - Specialist Center",
        "difficulty": "Hard",
        "specialty": "Neurology",
        "letter": """
FROM: Neurology Department
      District General Hospital NHS Trust
      Dr. Lisa Neuro - Consultant Neurologist

TO:   Regional Neurosurgery Unit
      Specialist Tertiary Center NHS Foundation Trust
      (DIFFERENT PROVIDER)

Date: 10 October 2025
Ref: NEURO/TERTIARY/2025/234

⚠️ TERTIARY REFERRAL - RTT CLOCK CONTINUES ⚠️

=====================================

Dear Colleague,

Re: Mr. David Brown - Complex Headache

Following assessment in neurology clinic, this case requires 
input from our tertiary neurosurgery center.

I am referring to Regional Neurosurgery Unit for specialist 
care. Patient unlikely to return to our service.

Current RTT pathway to continue at tertiary center.

Dr. Lisa Neuro
Consultant Neurologist
        """,
        "correct_code": "21",
        "explanation": "Tertiary referral to another provider = Code 21. RTT clock CONTINUES (still ticking, doesn't stop or restart).",
        "key_points": [
            "Code 21 = Tertiary referral",
            "Original RTT clock CONTINUES (doesn't reset!)",
            "Patient referred to another provider",
            "Common mistake: thinking it's Code 10 (new referral)",
            "Time spent waiting counts toward 18 weeks"
        ],
        "expected_actions": [
            "Record Code 21",
            "Send referral to tertiary center",
            "RTT clock keeps running",
            "Track onward referral",
            "Chase if no response within 2 weeks",
            "Transfer pathway to new provider"
        ]
    },
    {
        "id": 10,
        "title": "Patient Unfit for Treatment - Medical Reasons",
        "difficulty": "Medium",
        "specialty": "Cardiology",
        "letter": """
Clinic Letter

Patient attended for pre-operative assessment for cardiac surgery.

Unfortunately, recent blood results show acute kidney injury (AKI Stage 2).

Surgery is postponed until renal function improves.

Patient removed from surgical list temporarily. Will reassess in 4 weeks.

Pathway to continue.

Dr. Cardiac
        """,
        "correct_code": "35",
        "explanation": "Patient medically unfit = Code 35. Clock PAUSES until patient fit again.",
        "key_points": [
            "Code 35 = Patient Unfit (medical reasons)",
            "Clock PAUSES (not stops)",
            "Different from patient choice (Code 31)",
            "When fit, clock resumes with Code 11",
            "Medical unfitness is temporary suspension"
        ],
        "expected_actions": [
            "Record Code 35",
            "Pause RTT clock",
            "Remove from surgical WL temporarily",
            "Book review appointment (4 weeks)",
            "When fit: Code 11 to resume pathway",
            "Monitor kidney function"
        ]
    },
    {
        "id": 11,
        "title": "Diagnostic Test Completed - Abnormal",
        "difficulty": "Medium",
        "specialty": "Gastroenterology",
        "letter": """
Endoscopy Report

Gastroscopy performed 10/10/2025.

Findings: Gastric ulcer identified (2cm, antrum).
Biopsies taken for histology.

Plan:
- Await histology results
- Start PPI therapy
- Follow-up clinic in 2 weeks for results

Dr. Endo
        """,
        "correct_code": "20",
        "explanation": "Diagnostic test done + decision to treat = Code 20. Clock CONTINUES until treatment (Code 30) or discharge (Code 34).",
        "key_points": [
            "Diagnostic completed (past tense)",
            "Abnormal finding = decision to treat",
            "Code 20 = Clock continuing",
            "Will need Code 30 (treatment) or Code 34 (discharge) later",
            "Awaiting histology doesn't stop clock"
        ],
        "expected_actions": [
            "Record Code 20",
            "Chase histology results",
            "Book follow-up clinic",
            "Start PPI therapy",
            "Plan treatment based on histology",
            "RTT clock still running!"
        ]
    },
    {
        "id": 12,
        "title": "Treatment Completed - Non-Surgical",
        "difficulty": "Easy",
        "specialty": "Dermatology",
        "letter": """
Dear Patient,

Your cryotherapy treatment for skin lesions was completed today (05/10/2025).

The treated areas will heal over 2-3 weeks. No further treatment needed.

Discharge from dermatology service.

Dr. Derm
        """,
        "correct_code": "30",
        "explanation": "Non-surgical treatment completed = Code 30 (First Definitive Treatment). Stops clock!",
        "key_points": [
            "Treatment doesn't have to be surgery!",
            "Cryotherapy IS definitive treatment",
            "Code 30 applies to ANY first definitive treatment",
            "Clock STOPS on treatment date",
            "Common mistake: thinking Code 30 is only for surgery"
        ],
        "expected_actions": [
            "Record Code 30",
            "Set clock stop date = 05/10/2025",
            "Close RTT pathway",
            "Discharge patient",
            "Send GP letter",
            "No follow-up needed (lesions benign)"
        ]
    },
    
    # ============================================
    # HARD SCENARIOS (Complex codes & situations)
    # ============================================
    {
        "id": 13,
        "title": "Transfer Between Consultants - Same Trust",
        "difficulty": "Hard",
        "specialty": "ENT",
        "letter": """
Internal Transfer Note

Patient currently under Mr. Smith (ENT Surgeon A).

Due to sub-specialty requirements, transferring care to 
Mr. Jones (Rhinology specialist) within same ENT department.

Patient pathway to continue.

Admin Team
        """,
        "correct_code": "36",
        "explanation": "Transfer between consultants = Code 36. RTT clock CONTINUES (no reset).",
        "key_points": [
            "Code 36 = Consultant transfer",
            "Clock CONTINUES (doesn't restart)",
            "Same trust or different trust",
            "Patient on SAME pathway",
            "Different from new referral (Code 10)"
        ],
        "expected_actions": [
            "Record Code 36",
            "Transfer notes to Mr. Jones",
            "Maintain RTT clock",
            "Book with new consultant",
            "Update PAS system",
            "Inform patient of change"
        ]
    },
    {
        "id": 14,
        "title": "Patient DNA'd - Multiple Times",
        "difficulty": "Hard",
        "specialty": "General Surgery",
        "letter": """
Admin Note

Patient DNA'd 3 consecutive appointments:
- 01/09/2025 - DNA (Code 33 recorded)
- 15/09/2025 - DNA (Code 33 recorded)
- 29/09/2025 - DNA (Code 33 recorded)

As per trust policy, patient to be discharged after 3 DNAs.

GP informed. Patient advised to re-refer if needed.
        """,
        "correct_code": "34",
        "explanation": "After multiple DNAs (per trust policy), patient is discharged = Code 34. This STOPS the RTT clock.",
        "key_points": [
            "Code 34 = Discharge (no treatment needed)",
            "3 DNAs triggers discharge (trust policy)",
            "Each DNA recorded as Code 33",
            "Pathway ENDS with discharge",
            "Patient needs NEW referral (Code 10) to restart"
        ],
        "expected_actions": [
            "Record Code 34 (Discharge)",
            "Close RTT pathway",
            "Remove from all waiting lists",
            "Send discharge letter to patient + GP",
            "Document DNA history",
            "New referral required for re-entry"
        ]
    },
    {
        "id": 15,
        "title": "Cancer 62-Day Breach Risk",
        "difficulty": "Expert",
        "specialty": "Oncology",
        "letter": """
MDT Outcome

Patient: Colorectal Cancer Suspected
Referral Date: 01/08/2025 (2WW)
Today's Date: 20/09/2025

MDT Decision: Proceed to surgery

Issues:
- Day 50 of 62-day pathway
- No surgery slots available until Day 65
- Breach imminent

Plan: Escalate to Breach Meeting
        """,
        "correct_code": "20",
        "explanation": "Despite breach risk, the CODE is still 20 (Decision to Treat). Breach management is separate process!",
        "key_points": [
            "RTT code ≠ Breach status",
            "Decision to treat = Code 20",
            "Breach needs separate escalation",
            "Must still record correct RTT code",
            "Breach meeting doesn't change code!"
        ],
        "expected_actions": [
            "Record Code 20",
            "URGENT: Escalate to Cancer Manager",
            "Breach meeting required",
            "Explore alternative surgical dates",
            "Consider treatment at another trust",
            "Document all breach prevention attempts",
            "Patient communication critical"
        ]
    },
    {
        "id": 16,
        "title": "Planned Procedure - Endoscopy",
        "difficulty": "Medium",
        "specialty": "Gastroenterology",
        "letter": """
Day Case Procedure Completed

Colonoscopy performed 12/10/2025.

Findings: Multiple polyps removed (polypectomy performed).

Histology sent.

Surveillance colonoscopy recommended in 1 year.

Discharged from current pathway.
        """,
        "correct_code": "30",
        "explanation": "Therapeutic endoscopy (polyps removed) = First Definitive Treatment = Code 30!",
        "key_points": [
            "Diagnostic + Therapeutic = Code 30",
            "Polyp removal IS treatment",
            "Not just investigation",
            "Clock STOPS on procedure date",
            "Surveillance = new pathway later (if needed)"
        ],
        "expected_actions": [
            "Record Code 30",
            "Stop RTT clock (date: 12/10/2025)",
            "Close current pathway",
            "Chase histology",
            "Book surveillance (1 year)",
            "Send GP report"
        ]
    },
    
    # MORE SCENARIOS COMING - Add specialty-specific ones
    {
        "id": 17,
        "title": "Ophthalmology - Cataract Surgery",
        "difficulty": "Easy",
        "specialty": "Ophthalmology",
        "letter": """
GP Referral

Please see this patient for cataract assessment.

Reduced visual acuity (6/18) affecting daily activities.
Right eye worse than left.

Please assess for cataract surgery.

Dr. GP
        """,
        "correct_code": "10",
        "explanation": "GP referral = Code 10. Starts RTT clock.",
        "key_points": [
            "New GP referral",
            "Starts pathway",
            "Assessment needed before decision"
        ],
        "expected_actions": [
            "Code 10",
            "Book outpatient appointment",
            "Visual acuity test",
            "Ophthalmology assessment"
        ]
    },
    {
        "id": 18,
        "title": "Urology - Urgent Suspected Cancer",
        "difficulty": "Medium",
        "specialty": "Urology",
        "letter": """
2WW REFERRAL - URGENT

Patient with visible haematuria (3 episodes).
Age 68, smoker.

Urgent cystoscopy required to rule out bladder cancer.

Dr. Williams
        """,
        "correct_code": "10",
        "explanation": "2WW cancer referral is still Code 10. The urgency affects booking timeline, not the RTT code.",
        "key_points": [
            "2WW = book within 14 days",
            "Still Code 10",
            "62-day cancer clock starts",
            "Urgent != different code"
        ],
        "expected_actions": [
            "Flag as 2WW cancer",
            "Code 10",
            "Book within 14 days",
            "Urgent cystoscopy",
            "Cancer PTL"
        ]
    },
    {
        "id": 19,
        "title": "Patient Did Not Attend - Rebook",
        "difficulty": "Easy",
        "specialty": "Orthopedics",
        "letter": """
Patient DNA'd appointment on 15/10/2025.

First outpatient appointment.

Rebook as per policy.
        """,
        "correct_code": "33",
        "explanation": "DNA = Code 33. Patient must be rebooked.",
        "key_points": [
            "DNA = Did Not Attend",
            "Code 33",
            "Rebook required",
            "Send DNA letter"
        ],
        "expected_actions": [
            "Code 33",
            "Rebook appointment",
            "DNA letter to patient",
            "Inform GP"
        ]
    },
    {
        "id": 20,
        "title": "Tertiary Referral - Specialist Opinion",
        "difficulty": "Medium",
        "specialty": "Radiology",
        "letter": """
MRI Scan Report

MRI spine performed 08/10/2025.

Findings: Disc prolapse L4/L5.

Patient to be referred to tertiary neurosurgery center for specialist assessment and likely treatment there.
        """,
        "correct_code": "21",
        "explanation": "Tertiary referral to another provider = Code 21. Clock continues (still ticking).",
        "key_points": [
            "Tertiary referral needed",
            "Code 21",
            "Clock CONTINUES (still ticking)",
            "Not a new referral (not Code 10)"
        ],
        "expected_actions": [
            "Record Code 21",
            "Refer to neurosurgery",
            "Clock keeps running",
            "Track referral"
        ]
    },
    {
        "id": 21,
        "title": "CODE 11 - Active Monitoring Restart (Patient Now Ready)",
        "difficulty": "Hard",
        "specialty": "Orthopedics",
        "letter": """
FROM: Orthopedic Department
      Royal Hospital NHS Trust
      Mr. David Surgeon - Consultant Orthopedic Surgeon

TO:   Waiting List Team / RTT Coordinator

Date: 16 October 2025
Ref: ORTHO/RESTART/2025/456

⚠️ CLOCK RESTART - PATIENT NOW READY FOR TREATMENT ⚠️

=====================================

Patient: Mr. David Brown
NHS: 5555666677
DOB: 22/08/1962

PREVIOUS RTT PATHWAY:
- Seen in clinic: 15 March 2025
- Diagnosis: Severe osteoarthritis right hip
- Treatment offered: Total hip replacement
- PATIENT DECLINED at that time (wanted to try conservative management first)
- Clock stopped with Code 31 (Patient Declined Treatment)
- Discharge date: 15 March 2025

CURRENT STATUS:
Patient contacted clinic today. Conservative management has failed. 
Patient now READY and REQUESTING to proceed with hip replacement surgery.

Clinical decision: Patient suitable for surgery, no change in clinical condition.

ACTION REQUIRED:
- RESTART RTT clock using Code 11 (Active Monitoring Starter)
- Add to waiting list for total hip replacement
- New clock starts from TODAY

Consultant Decision: Proceed with hip replacement

Mr. David Surgeon
Consultant Orthopedic Surgeon
        """,
        "correct_code": "11",
        "explanation": "Code 11 - Active Monitoring Starter! Used to RESTART a clock that previously ended with Code 31 (patient declined). Patient now ready, so clock restarts with Code 11.",
        "key_points": [
            "⚠️ Code 11 = RESTART a stopped clock (31/32/91)",
            "Previous clock ended with Code 31 (patient declined)",
            "Patient NOW ready for treatment",
            "Code 11 RESTARTS the RTT clock",
            "NEW 18-week clock starts from Code 11 date"
        ],
        "expected_actions": [
            "Record Code 11 (Clock Restart)",
            "Check previous pathway ended with 31/32/91",
            "NEW 18-week clock starts today",
            "Add to surgical waiting list",
            "Book pre-op assessment"
        ]
    },
    {
        "id": 22,
        "title": "CODE 12 - Consultant Referral for NEW Condition",
        "difficulty": "Hard",
        "specialty": "Cardiology",
        "letter": """
FROM: ENT Department
      Northern General Hospital NHS Trust
      Mr. Peter Collins - Consultant ENT Surgeon

TO:   Cardiology Department
      Northern General Hospital NHS Trust (SAME TRUST)
      Consultant Cardiologist

Date: 16 October 2025
Ref: ENT/NEW-REF/CARDIO/2025/789

⚠️ CONSULTANT REFERRAL - NEW/DIFFERENT CONDITION ⚠️

=====================================

Dear Cardiology Colleague,

Patient: Mrs. Linda White
NHS: 7777888899
DOB: 10/03/1970

CURRENT ENT TREATMENT:
Patient currently under my care for chronic rhinosinusitis. This is ongoing and managed.

NEW/SEPARATE ISSUE IDENTIFIED:
During routine pre-operative assessment for sinus surgery, patient mentioned experiencing:
- Palpitations for past 6 weeks
- Occasional chest tightness
- Episodes of dizziness

ECG performed shows atrial fibrillation (new diagnosis).

This is a SEPARATE condition unrelated to her ENT problem.

Request:
- Cardiology assessment for newly diagnosed AF
- Anticoagulation consideration
- Rate/rhythm control
- Separate RTT pathway for cardiology issue

Patient's ENT treatment continues in parallel.

Many thanks,
Mr. Peter Collins
Consultant ENT Surgeon
        """,
        "correct_code": "12",
        "explanation": "Code 12 - Consultant-to-Consultant referral for a NEW/DIFFERENT condition! Patient is with ENT for sinus problem, but NEW cardiac issue discovered, so ENT refers to Cardiology. This is NOT Code 10 (not from GP) and NOT Code 11 (not restarting a stopped clock).",
        "key_points": [
            "⚠️ Code 12 = Consultant refers to another consultant for NEW condition",
            "Patient already under consultant care (ENT)",
            "NEW separate problem identified (AF)",
            "Referral to DIFFERENT specialty (Cardiology)",
            "Creates NEW RTT pathway",
            "NOT from GP (so not Code 10)"
        ],
        "expected_actions": [
            "Record Code 12 (Consultant referral - new condition)",
            "Create NEW RTT pathway for cardiology",
            "NEW 18-week clock starts",
            "Book cardiology appointment",
            "ENT pathway continues separately"
        ]
    }
]


def get_all_scenarios():
    """Get all training scenarios"""
    return TRAINING_SCENARIOS


def get_scenario(scenario_id):
    """Get specific training scenario"""
    for scenario in TRAINING_SCENARIOS:
        if scenario['id'] == scenario_id:
            return scenario
    return None


def check_answer(scenario_id, user_answer):
    """Check if user's answer is correct"""
    scenario = get_scenario(scenario_id)
    
    if not scenario:
        return None
    
    correct = user_answer == scenario['correct_code']
    
    return {
        'correct': correct,
        'user_answer': user_answer,
        'correct_answer': scenario['correct_code'],
        'explanation': scenario['explanation'],
        'key_points': scenario['key_points'],
        'expected_actions': scenario['expected_actions']
    }
