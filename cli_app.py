"""
T21 RTT Pathway Validator - Command Line Interface
Works with any Python version without additional dependencies
"""

import json
from datetime import datetime
from rtt_validator import (validate_pathway, validate_clinic_letter, validate_timeline,
                           validate_patient_registration, validate_appointments, generate_comment_line)


def print_header():
    print("=" * 70)
    print("T21 RTT PATHWAY INTELLIGENCE (v1.2) - CLI")
    print("NHS Referral To Treatment Validation System")
    print("T21 Services UK | Training & Simulation Environment")
    print("=" * 70)
    print()


def print_json_result(result):
    """Pretty print JSON result"""
    print("\n" + "=" * 70)
    print("VALIDATION RESULT:")
    print("=" * 70)
    print(json.dumps(result, indent=2))
    print("=" * 70)


def tool_pathway_validator():
    """Tool 1: Pathway Validator"""
    print("\nPATHWAY VALIDATOR")
    print("-" * 70)
    
    data = {}
    data['specialty'] = input("Specialty (e.g., ENT): ") or "ENT"
    data['referral_source'] = input("Referral Source (GP/Consultant/A&E): ") or "GP"
    data['referral_date'] = input("Referral Date (DD/MM/YYYY): ") or "02/01/2025"
    data['first_appt_date'] = input("First Appointment Date (DD/MM/YYYY): ") or "10/01/2025"
    data['diagnostics_date'] = input("Diagnostics Date (DD/MM/YYYY or blank): ") or ""
    data['decision_date'] = input("Decision to Treat Date (DD/MM/YYYY or blank): ") or ""
    data['treatment_date'] = input("First Treatment Date (DD/MM/YYYY or blank): ") or ""
    data['delays_pauses'] = input("Delays/Pauses (e.g., 'Patient 4-week delay'): ") or ""
    data['active_monitoring'] = input("Active Monitoring (none/31_patient/32_clinician): ") or "none"
    data['current_rtt_event'] = input("Current RTT Event Code (10-98): ") or "20"
    
    result = validate_pathway(data)
    print_json_result(result)


def tool_clinic_letter():
    """Tool 2: Clinic Letter Interpreter"""
    print("\nCLINIC LETTER INTERPRETER")
    print("-" * 70)
    
    print("Paste clinic letter (press Enter twice when done):")
    lines = []
    while True:
        line = input()
        if line == "" and lines:
            break
        lines.append(line)
    letter_text = "\n".join(lines)
    
    pas_summary = {}
    pas_summary['followup_booked'] = input("Follow-up booked (Y/N): ") or "N"
    pas_summary['diagnostics_ordered'] = input("Diagnostics ordered (Y/N): ") or "N"
    pas_summary['waiting_list'] = input("Added to waiting list (Y/N): ") or "N"
    pas_summary['gp_informed'] = input("GP letter sent (Y/N): ") or "N"
    
    result = validate_clinic_letter(letter_text, pas_summary)
    print_json_result(result)


def tool_timeline_auditor():
    """Tool 3: Timeline Auditor"""
    print("\nTIMELINE AUDITOR")
    print("-" * 70)
    
    events = []
    print("Enter events (type 'done' when finished):")
    while True:
        date = input("Event date (DD/MM/YYYY) or 'done': ")
        if date.lower() == 'done':
            break
        description = input("Description: ")
        code = input("RTT Code (10-98): ")
        notes = input("Notes (optional): ")
        
        events.append({
            'date': date,
            'description': description,
            'code': code,
            'notes': notes
        })
    
    result = validate_timeline(events)
    print_json_result(result)


def tool_patient_registration():
    """Tool 4: Patient Registration Validator"""
    print("\nPATIENT REGISTRATION VALIDATOR")
    print("-" * 70)
    
    data = {}
    data['patient_name'] = input("Patient Name: ") or "SMITH, John"
    data['nhs_number'] = input("NHS Number (10 digits): ") or "1234567881"
    data['dob'] = input("Date of Birth (DD/MM/YYYY): ") or "15/03/1985"
    data['referral_source'] = input("Referral Source: ") or "GP"
    data['referral_date'] = input("Referral Date (DD/MM/YYYY): ") or "02/01/2025"
    data['specialty'] = input("Specialty: ") or "ENT"
    data['documents'] = input("Documents (comma-separated): ") or ""
    data['referral_accepted'] = input("Referral Accepted (Y/N): ") or "Y"
    data['check_duplicate'] = "N"
    
    result = validate_patient_registration(data)
    print_json_result(result)


def tool_appointment_checker():
    """Tool 5: Appointment & Booking Checker"""
    print("\nAPPOINTMENT & BOOKING CHECKER")
    print("-" * 70)
    
    data = {}
    data['referral_date'] = input("Referral Date (DD/MM/YYYY): ") or "02/01/2025"
    data['first_appt_date'] = input("First Appointment Date (DD/MM/YYYY): ") or "12/01/2025"
    data['dnas_cancellations'] = input("DNAs/Cancellations (text): ") or ""
    data['planned_surgery'] = input("Planned Surgery/WL details: ") or ""
    data['am_status'] = input("Active Monitoring (none/31/32/91): ") or "none"
    data['treatment_started'] = input("Treatment Started (Y/N): ") or "N"
    data['notes'] = input("Additional notes: ") or ""
    data['followup_appointments'] = ""
    data['am_start_date'] = ""
    
    result = validate_appointments(data)
    print_json_result(result)


def tool_comment_generator():
    """Tool 6: Comment Line Generator"""
    print("\nCOMMENT LINE GENERATOR")
    print("-" * 70)
    
    data = {}
    print("Event Types:")
    print("  1. First Treatment / FDT")
    print("  2. Active Monitoring Start")
    print("  3. DNA First Care")
    print("  4. Waiting List / TCI")
    print("  5. Discharge")
    print("  6. Decision to Treat")
    
    event_choice = input("Select event type (1-6): ") or "1"
    event_map = {
        "1": "First Treatment / FDT",
        "2": "Active Monitoring Start",
        "3": "DNA First Care",
        "4": "Waiting List / TCI",
        "5": "Discharge",
        "6": "Decision to Treat"
    }
    data['event'] = event_map.get(event_choice, "First Treatment / FDT")
    
    data['key_date'] = input("Key Date (DD/MM/YYYY): ") or datetime.now().strftime('%d/%m/%Y')
    data['rtt_code'] = input("RTT Code (optional): ") or ""
    data['procedure'] = input("Procedure/Outcome: ") or ""
    data['next_action'] = input("Next Action/Follow-up: ") or ""
    data['gp_letter'] = input("GP Letter Sent (Y/N): ") or "N"
    
    result = generate_comment_line(data)
    print("\n" + "=" * 70)
    print("GENERATED COMMENT LINE:")
    print("=" * 70)
    print(result['Standardised_Comment_Line'])
    print("=" * 70)


def main():
    """Main menu"""
    print_header()
    
    while True:
        print("\nSELECT TOOL:")
        print("-" * 70)
        print("1. Pathway Validator")
        print("2. Clinic Letter Interpreter")
        print("3. Timeline Auditor")
        print("4. Patient Registration Validator")
        print("5. Appointment & Booking Checker")
        print("6. Comment Line Generator")
        print("7. Exit")
        print("-" * 70)
        
        choice = input("\nEnter choice (1-7): ").strip()
        
        if choice == '1':
            tool_pathway_validator()
        elif choice == '2':
            tool_clinic_letter()
        elif choice == '3':
            tool_timeline_auditor()
        elif choice == '4':
            tool_patient_registration()
        elif choice == '5':
            tool_appointment_checker()
        elif choice == '6':
            tool_comment_generator()
        elif choice == '7':
            print("\nThank you for using T21 RTT Pathway Intelligence!")
            print("T21 Services UK | Training & Simulation Environment")
            break
        else:
            print("\n[X] Invalid choice. Please enter 1-7.")
        
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
