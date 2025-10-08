"""
Quick test for discharge letter detection
"""

from rtt_validator import validate_clinic_letter

# Your discharge letter
discharge_letter = """
Consultant Lead,
Cardiology Department
Royal Oak NHS Hospital

Date: 24th August 2023

Mr. John Doe

Re: Results from Your Recent Investigations

I am pleased to inform you that the results from both the Coronary Angiography and the Echocardiogram were performed appropriately and have returned as normal.

Based on these findings, I do not believe that any medical intervention is needed at this point. Your heart and its associated structures appear to be functioning well.

Should you have any questions, please contact our department.

Yours sincerely,
Dr. Alex Turner
"""

pas_summary = {
    'validator_initials': 'VLD',
    'clock_status': 'Yes',
    'outcome': 'Discharged',
    'followup_booked': 'N',
    'diagnostics_ordered': 'N',
    'waiting_list': 'N',
    'gp_informed': 'N',
    'am_recorded': 'N',
    'treatment_started': 'N'
}

result = validate_clinic_letter(discharge_letter, pas_summary)

print("=" * 70)
print("DISCHARGE LETTER TEST")
print("=" * 70)
print(f"\nRTT Code: {result['RTT_Code']}")
print(f"RTT Action: {result['RTT_Action']}")
print(f"Clock Status: {result['Clock_Status']}")
print(f"Explanation: {result['Explanation']}")
print(f"\nActions Required: {len(result['Action_Compliance']['Actions_Required'])}")
print(f"Gaps Found: {len(result['Action_Compliance']['Gaps'])}")

print("\n" + "=" * 70)
if result['RTT_Code'] == '34':
    print("✅ SUCCESS! Correctly detected as Code 34 (Discharge)")
else:
    print(f"❌ FAILED! Detected as Code {result['RTT_Code']} instead of 34")
print("=" * 70)
