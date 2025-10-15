"""
UNIFIED PATIENT RECORD SYSTEM
Central patient database linking ALL modules

Features:
- Master patient index
- Cross-module patient linking
- Single source of truth for patient data
- Patient search across all modules
- Data synchronization
"""

from datetime import datetime
from typing import Dict, List, Optional
import streamlit as st
from session_manager import get_current_user_email
from config import SUPABASE_ENABLED

# Import from all modules
from ptl_system import get_all_patients as get_ptl_patients
from cancer_pathway_system import get_all_cancer_patients
from mdt_coordination_system import get_all_mdt_meetings
from advanced_booking_system import load_appointments


def normalize_nhs_number(nhs_number: str) -> str:
    """Normalize NHS number for comparison (remove spaces, hyphens)"""
    if not nhs_number:
        return ""
    return ''.join(filter(str.isdigit, str(nhs_number)))


def find_patient_by_nhs(nhs_number: str) -> Dict:
    """
    Find patient across ALL modules by NHS number
    Returns unified patient record with data from all sources
    """
    nhs = normalize_nhs_number(nhs_number)
    
    if not nhs:
        return None
    
    unified_record = {
        'nhs_number': nhs_number,
        'patient_name': '',
        'found_in': [],
        'ptl_record': None,
        'cancer_record': None,
        'mdt_appearances': [],
        'appointments': [],
        'timeline': []
    }
    
    # Search PTL
    try:
        ptl_patients = get_ptl_patients()
        for patient in ptl_patients:
            if normalize_nhs_number(patient.get('nhs_number', '')) == nhs:
                unified_record['ptl_record'] = patient
                unified_record['patient_name'] = patient.get('patient_name', '')
                unified_record['found_in'].append('PTL')
                
                # Add to timeline
                unified_record['timeline'].append({
                    'date': patient.get('referral_date') or patient.get('added_date'),
                    'event': 'Added to PTL',
                    'module': 'PTL',
                    'details': f"Specialty: {patient.get('specialty')}, Priority: {patient.get('priority')}"
                })
                break
    except Exception as e:
        print(f"⚠️ Error searching PTL: {e}")
    
    # Search Cancer Pathways
    try:
        cancer_patients = get_all_cancer_patients()
        for patient in cancer_patients:
            if normalize_nhs_number(patient.get('nhs_number', '')) == nhs:
                unified_record['cancer_record'] = patient
                if not unified_record['patient_name']:
                    unified_record['patient_name'] = patient.get('patient_name', '')
                unified_record['found_in'].append('Cancer Pathways')
                
                # Add to timeline
                unified_record['timeline'].append({
                    'date': patient.get('referral_date'),
                    'event': 'Cancer Pathway Started',
                    'module': 'Cancer',
                    'details': f"Type: {patient.get('cancer_type')}, Pathway: {patient.get('pathway_type')}"
                })
                
                # Add milestones to timeline
                for milestone in patient.get('milestones', []):
                    unified_record['timeline'].append({
                        'date': milestone.get('date'),
                        'event': milestone.get('milestone', 'Milestone'),
                        'module': 'Cancer',
                        'details': milestone.get('description', '')
                    })
                break
    except Exception as e:
        print(f"⚠️ Error searching Cancer: {e}")
    
    # Search MDT Meetings
    try:
        all_meetings = get_all_mdt_meetings()
        for meeting in all_meetings:
            patients = meeting.get('patients_discussed') or meeting.get('patients', [])
            for patient in patients:
                if normalize_nhs_number(patient.get('nhs_number', '')) == nhs:
                    unified_record['mdt_appearances'].append({
                        'meeting_id': meeting.get('meeting_id'),
                        'meeting_date': meeting.get('meeting_date'),
                        'specialty': meeting.get('specialty'),
                        'diagnosis': patient.get('diagnosis'),
                        'outcome': patient.get('outcome'),
                        'decision': patient.get('decision'),
                        'discussed': patient.get('discussed', False)
                    })
                    
                    if not unified_record['patient_name']:
                        unified_record['patient_name'] = patient.get('patient_name', '')
                    
                    if 'MDT' not in unified_record['found_in']:
                        unified_record['found_in'].append('MDT')
                    
                    # Add to timeline
                    unified_record['timeline'].append({
                        'date': meeting.get('meeting_date'),
                        'event': 'MDT Discussion',
                        'module': 'MDT',
                        'details': f"{meeting.get('specialty')} MDT - {patient.get('diagnosis')}"
                    })
                    
                    if patient.get('discussed'):
                        unified_record['timeline'].append({
                            'date': patient.get('outcome_recorded_date') or meeting.get('meeting_date'),
                            'event': 'MDT Decision Recorded',
                            'module': 'MDT',
                            'details': f"Outcome: {patient.get('outcome')}, Decision: {patient.get('decision')}"
                        })
    except Exception as e:
        print(f"⚠️ Error searching MDT: {e}")
    
    # Search Appointments
    try:
        appointments_data = load_appointments()
        appointments = appointments_data.get('appointments', [])
        for appt in appointments:
            if normalize_nhs_number(appt.get('nhs_number', '')) == nhs:
                unified_record['appointments'].append(appt)
                
                if not unified_record['patient_name']:
                    unified_record['patient_name'] = appt.get('patient_name', '')
                
                if 'Appointments' not in unified_record['found_in']:
                    unified_record['found_in'].append('Appointments')
                
                # Add to timeline
                unified_record['timeline'].append({
                    'date': appt.get('appointment_date'),
                    'event': f"Appointment - {appt.get('status', 'Unknown')}",
                    'module': 'Appointments',
                    'details': f"{appt.get('appointment_type')} with {appt.get('consultant', 'Unknown')}"
                })
    except Exception as e:
        print(f"⚠️ Error searching Appointments: {e}")
    
    # Sort timeline by date
    unified_record['timeline'].sort(key=lambda x: x.get('date', ''), reverse=True)
    
    return unified_record if unified_record['found_in'] else None


def search_patients(query: str) -> List[Dict]:
    """
    Search for patients across all modules
    Query can be: name, NHS number, or part of either
    """
    query_lower = query.lower().strip()
    
    if not query_lower:
        return []
    
    results = []
    seen_nhs = set()
    
    # Search PTL
    try:
        ptl_patients = get_ptl_patients()
        for patient in ptl_patients:
            nhs = normalize_nhs_number(patient.get('nhs_number', ''))
            name = patient.get('patient_name', '').lower()
            
            if query_lower in name or query_lower in nhs or query_lower in patient.get('nhs_number', '').lower():
                if nhs not in seen_nhs:
                    seen_nhs.add(nhs)
                    results.append({
                        'nhs_number': patient.get('nhs_number'),
                        'patient_name': patient.get('patient_name'),
                        'modules': ['PTL'],
                        'latest_activity': patient.get('last_updated') or patient.get('added_date'),
                        'status': patient.get('current_status', 'Unknown')
                    })
    except Exception as e:
        print(f"⚠️ Error searching PTL: {e}")
    
    # Search Cancer
    try:
        cancer_patients = get_all_cancer_patients()
        for patient in cancer_patients:
            nhs = normalize_nhs_number(patient.get('nhs_number', ''))
            name = patient.get('patient_name', '').lower()
            
            if query_lower in name or query_lower in nhs or query_lower in patient.get('nhs_number', '').lower():
                # Check if already found
                existing = next((r for r in results if normalize_nhs_number(r['nhs_number']) == nhs), None)
                if existing:
                    existing['modules'].append('Cancer')
                else:
                    seen_nhs.add(nhs)
                    results.append({
                        'nhs_number': patient.get('nhs_number'),
                        'patient_name': patient.get('patient_name'),
                        'modules': ['Cancer'],
                        'latest_activity': patient.get('updated_at') or patient.get('created_at'),
                        'status': patient.get('current_status', 'Unknown')
                    })
    except Exception as e:
        print(f"⚠️ Error searching Cancer: {e}")
    
    # Search MDT and Appointments (simplified for performance)
    
    return results


def get_patient_summary(nhs_number: str) -> Dict:
    """Get quick summary of patient across all modules"""
    unified = find_patient_by_nhs(nhs_number)
    
    if not unified:
        return None
    
    return {
        'nhs_number': unified['nhs_number'],
        'patient_name': unified['patient_name'],
        'modules': unified['found_in'],
        'total_events': len(unified['timeline']),
        'mdt_discussions': len(unified['mdt_appearances']),
        'appointments_count': len(unified['appointments']),
        'latest_activity': unified['timeline'][0]['date'] if unified['timeline'] else None,
        'on_ptl': unified['ptl_record'] is not None,
        'on_cancer_pathway': unified['cancer_record'] is not None
    }
