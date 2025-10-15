"""
T21 PATIENT REGISTRATION SYSTEM
Complete patient registration and demographic management

DUAL PURPOSE:
1. TRAINING: Students learn full patient registration workflow
2. PRODUCTION: Standalone system for small clinics or integration with PAS

Features:
- Patient demographic registration
- NHS number validation and assignment
- Temporary ID generation for unregistered patients
- Identity verification tracking
- GP and next of kin management
- Episode tracking (consultant, treatment, diagnostic)
- Integration ready for external PAS systems

For: All NHS staff dealing with patient administration
"""

import json
import os
from datetime import datetime, date
from typing import Optional, Dict, List
import re

# Import Supabase for permanent storage
try:
    from supabase_database import supabase
    SUPABASE_ENABLED = True
except ImportError:
    SUPABASE_ENABLED = False
    print("⚠️ Supabase not available - using local storage")

# Check if patients table exists
if SUPABASE_ENABLED:
    try:
        # Test if patients table exists
        test = supabase.table('patients').select('*').limit(1).execute()
    except Exception as e:
        if 'Could not find the table' in str(e):
            print("⚠️ Patients table not found in Supabase - using local storage")
            SUPABASE_ENABLED = False
        else:
            print(f"⚠️ Supabase connection issue - using local storage: {e}")
            SUPABASE_ENABLED = False


def get_current_user_email():
    """Get current logged-in user's email"""
    try:
        import streamlit as st
        return st.session_state.get('user_email', 'demo@t21services.co.uk')
    except:
        return 'demo@t21services.co.uk'


# ============================================
# NHS NUMBER VALIDATION
# ============================================

def validate_nhs_number(nhs_number: str) -> Dict:
    """
    Validate NHS number format and checksum
    NHS number format: 10 digits with valid checksum (Modulus 11)
    
    Example: 943 476 5919
    """
    # Remove spaces and dashes
    nhs_clean = re.sub(r'[^0-9]', '', nhs_number)
    
    if len(nhs_clean) != 10:
        return {
            'valid': False,
            'error': 'NHS number must be 10 digits',
            'formatted': nhs_number
        }
    
    # Validate checksum (Modulus 11 algorithm)
    try:
        digits = [int(d) for d in nhs_clean]
        
        # Multiply first 9 digits by weights 10-2
        total = sum(digit * (11 - i) for i, digit in enumerate(digits[:9]))
        
        # Calculate checksum
        remainder = total % 11
        check_digit = 11 - remainder
        
        # Check digit of 11 becomes 0
        if check_digit == 11:
            check_digit = 0
        
        # Check digit of 10 is invalid
        if check_digit == 10:
            return {
                'valid': False,
                'error': 'Invalid NHS number checksum',
                'formatted': format_nhs_number(nhs_clean)
            }
        
        # Compare with actual check digit
        if check_digit != digits[9]:
            return {
                'valid': False,
                'error': 'NHS number checksum does not match',
                'formatted': format_nhs_number(nhs_clean)
            }
        
        return {
            'valid': True,
            'formatted': format_nhs_number(nhs_clean),
            'raw': nhs_clean
        }
        
    except Exception as e:
        return {
            'valid': False,
            'error': f'Validation error: {str(e)}',
            'formatted': nhs_number
        }


def format_nhs_number(nhs_number: str) -> str:
    """Format NHS number as XXX XXX XXXX"""
    nhs_clean = re.sub(r'[^0-9]', '', nhs_number)
    if len(nhs_clean) == 10:
        return f"{nhs_clean[:3]} {nhs_clean[3:6]} {nhs_clean[6:]}"
    return nhs_number


def generate_temporary_id() -> str:
    """Generate temporary patient ID for unregistered patients"""
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    return f"TEMP_{timestamp}"


# ============================================
# PATIENT REGISTRATION
# ============================================

def register_patient(
    title: str,
    first_name: str,
    surname: str,
    date_of_birth: str,
    gender: str,
    nhs_number: Optional[str] = None,
    address_line1: str = "",
    address_line2: str = "",
    city: str = "",
    postcode: str = "",
    phone_home: str = "",
    phone_mobile: str = "",
    email: str = "",
    gp_name: str = "",
    gp_practice: str = "",
    gp_address: str = "",
    next_of_kin_name: str = "",
    next_of_kin_relationship: str = "",
    next_of_kin_phone: str = "",
    emergency_contact_name: str = "",
    emergency_contact_phone: str = "",
    ethnicity: str = "",
    language: str = "English",
    interpreter_required: bool = False,
    religion: str = "",
    marital_status: str = "",
    occupation: str = "",
    notes: str = ""
) -> Dict:
    """Register new patient with complete demographics"""
    
    user_email = get_current_user_email()
    
    # Validate or generate patient ID
    if nhs_number:
        validation = validate_nhs_number(nhs_number)
        if validation['valid']:
            patient_id = validation['raw']
            nhs_status = 'verified'
        else:
            # Use temporary ID if NHS number invalid
            patient_id = generate_temporary_id()
            nhs_status = 'invalid'
            nhs_number = None
    else:
        # Generate temporary ID
        patient_id = generate_temporary_id()
        nhs_status = 'pending'
    
    # Create patient record
    patient_data = {
        'patient_id': patient_id,
        'nhs_number': nhs_number,
        'nhs_status': nhs_status,
        'title': title,
        'first_name': first_name,
        'surname': surname,
        'full_name': f"{title} {first_name} {surname}",
        'date_of_birth': date_of_birth,
        'gender': gender,
        'address_line1': address_line1,
        'address_line2': address_line2,
        'city': city,
        'postcode': postcode,
        'phone_home': phone_home,
        'phone_mobile': phone_mobile,
        'email': email,
        'gp_name': gp_name,
        'gp_practice': gp_practice,
        'gp_address': gp_address,
        'next_of_kin_name': next_of_kin_name,
        'next_of_kin_relationship': next_of_kin_relationship,
        'next_of_kin_phone': next_of_kin_phone,
        'emergency_contact_name': emergency_contact_name,
        'emergency_contact_phone': emergency_contact_phone,
        'ethnicity': ethnicity,
        'language': language,
        'interpreter_required': interpreter_required,
        'religion': religion,
        'marital_status': marital_status,
        'occupation': occupation,
        'notes': notes,
        'registration_date': datetime.now().isoformat(),
        'registered_by': user_email,
        'user_email': user_email,
        'status': 'active'
    }
    
    # Save to database
    if SUPABASE_ENABLED:
        try:
            result = supabase.table('patients').insert(patient_data).execute()
            return {
                'success': True,
                'patient_id': patient_id,
                'nhs_status': nhs_status,
                'message': f'Patient registered successfully! ID: {patient_id}'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    else:
        # Fallback to local storage
        save_patient_local(patient_data)
        return {
            'success': True,
            'patient_id': patient_id,
            'nhs_status': nhs_status,
            'message': f'Patient registered successfully! ID: {patient_id}'
        }


def save_patient_local(patient_data: Dict):
    """Save patient to local JSON file (fallback)"""
    patients_file = 'patients_registered.json'
    
    if os.path.exists(patients_file):
        with open(patients_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        data = {'patients': []}
    
    data['patients'].append(patient_data)
    
    with open(patients_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def get_patient_by_id(patient_id: str) -> Optional[Dict]:
    """Get patient details by ID or NHS number"""
    user_email = get_current_user_email()
    
    if SUPABASE_ENABLED:
        try:
            # Try by patient_id first
            result = supabase.table('patients')\
                .select('*')\
                .eq('user_email', user_email)\
                .eq('patient_id', patient_id)\
                .execute()
            
            if result.data:
                return result.data[0]
            
            # Try by NHS number
            result = supabase.table('patients')\
                .select('*')\
                .eq('user_email', user_email)\
                .eq('nhs_number', patient_id)\
                .execute()
            
            if result.data:
                return result.data[0]
            
            return None
        except Exception as e:
            print(f"Error fetching patient: {e}")
            return None
    else:
        # Fallback to local storage
        return get_patient_local(patient_id)


def get_patient_local(patient_id: str) -> Optional[Dict]:
    """Get patient from local storage"""
    patients_file = 'patients_registered.json'
    
    if not os.path.exists(patients_file):
        return None
    
    with open(patients_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    for patient in data.get('patients', []):
        if patient.get('patient_id') == patient_id or patient.get('nhs_number') == patient_id:
            return patient
    
    return None


def search_patients(query: str) -> List[Dict]:
    """Search patients by name, NHS number, or ID"""
    user_email = get_current_user_email()
    
    if SUPABASE_ENABLED:
        try:
            # Try multiple search strategies
            results = []
            
            # Strategy 1: Search by full_name
            result = supabase.table('patients')\
                .select('*')\
                .eq('user_email', user_email)\
                .ilike('full_name', f'%{query}%')\
                .execute()
            
            if result.data:
                results.extend(result.data)
            
            # Strategy 2: Search by first_name
            result = supabase.table('patients')\
                .select('*')\
                .eq('user_email', user_email)\
                .ilike('first_name', f'%{query}%')\
                .execute()
            
            if result.data:
                for patient in result.data:
                    if patient not in results:
                        results.append(patient)
            
            # Strategy 3: Search by surname
            result = supabase.table('patients')\
                .select('*')\
                .eq('user_email', user_email)\
                .ilike('surname', f'%{query}%')\
                .execute()
            
            if result.data:
                for patient in result.data:
                    if patient not in results:
                        results.append(patient)
            
            # Strategy 4: Search by patient_id
            result = supabase.table('patients')\
                .select('*')\
                .eq('user_email', user_email)\
                .ilike('patient_id', f'%{query}%')\
                .execute()
            
            if result.data:
                for patient in result.data:
                    if patient not in results:
                        results.append(patient)
            
            # Strategy 5: Search by NHS number (if not None)
            if query:
                result = supabase.table('patients')\
                    .select('*')\
                    .eq('user_email', user_email)\
                    .ilike('nhs_number', f'%{query}%')\
                    .execute()
                
                if result.data:
                    for patient in result.data:
                        if patient not in results:
                            results.append(patient)
            
            print(f"🔍 Search for '{query}' found {len(results)} patients")
            return results
            
        except Exception as e:
            print(f"❌ Error searching patients: {e}")
            # Fallback: Get all patients and filter locally
            try:
                all_result = supabase.table('patients')\
                    .select('*')\
                    .eq('user_email', user_email)\
                    .execute()
                
                if all_result.data:
                    query_lower = query.lower()
                    filtered = [
                        p for p in all_result.data
                        if query_lower in p.get('full_name', '').lower() or
                           query_lower in p.get('first_name', '').lower() or
                           query_lower in p.get('surname', '').lower() or
                           query_lower in p.get('patient_id', '').lower() or
                           query_lower in (p.get('nhs_number') or '').lower()
                    ]
                    print(f"🔍 Fallback search found {len(filtered)} patients")
                    return filtered
            except Exception as e2:
                print(f"❌ Fallback search failed: {e2}")
            
            return []
    else:
        # Fallback to local storage
        return search_patients_local(query)


def search_patients_local(query: str) -> List[Dict]:
    """Search patients in local storage"""
    patients_file = 'patients_registered.json'
    
    if not os.path.exists(patients_file):
        return []
    
    with open(patients_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    query_lower = query.lower()
    results = []
    
    for patient in data.get('patients', []):
        if (query_lower in patient.get('full_name', '').lower() or
            query_lower in patient.get('nhs_number', '').lower() or
            query_lower in patient.get('patient_id', '').lower()):
            results.append(patient)
    
    return results


def get_all_patients() -> List[Dict]:
    """Get all registered patients for current user"""
    user_email = get_current_user_email()
    
    if SUPABASE_ENABLED:
        try:
            result = supabase.table('patients')\
                .select('*')\
                .eq('user_email', user_email)\
                .order('registration_date', desc=True)\
                .execute()
            
            return result.data if result.data else []
        except Exception as e:
            print(f"Error fetching patients: {e}")
            return []
    else:
        # Fallback to local storage
        return get_all_patients_local()


def get_all_patients_local() -> List[Dict]:
    """Get all patients from local storage"""
    patients_file = 'patients_registered.json'
    
    if not os.path.exists(patients_file):
        return []
    
    with open(patients_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    return data.get('patients', [])


# ============================================
# STATISTICS
# ============================================

def get_registration_stats() -> Dict:
    """Get patient registration statistics"""
    patients = get_all_patients()
    
    total = len(patients)
    with_nhs = len([p for p in patients if p.get('nhs_status') == 'verified'])
    pending_nhs = len([p for p in patients if p.get('nhs_status') == 'pending'])
    temp_ids = len([p for p in patients if p.get('patient_id', '').startswith('TEMP_')])
    
    # Registrations today
    today = datetime.now().date().isoformat()
    today_count = len([p for p in patients if p.get('registration_date', '').startswith(today)])
    
    return {
        'total_patients': total,
        'with_nhs_number': with_nhs,
        'pending_nhs_number': pending_nhs,
        'temporary_ids': temp_ids,
        'registered_today': today_count,
        'nhs_verified_rate': (with_nhs / total * 100) if total > 0 else 0
    }
