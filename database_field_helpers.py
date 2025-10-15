"""
DATABASE FIELD COMPATIBILITY HELPERS
Handles field name differences between old code and new SQL schema
"""

def get_patient_id(record: dict) -> str:
    """Get patient/pathway ID - handles both old and new field names"""
    return record.get('pathway_id') or record.get('patient_id') or ''


def get_patients_list(meeting: dict) -> list:
    """Get patients list from MDT meeting - handles both old and new field names"""
    return meeting.get('patients_discussed') or meeting.get('patients', [])


def get_chair_person(meeting: dict) -> str:
    """Get chair person from MDT meeting - handles both old and new field names"""
    return meeting.get('chair_person') or meeting.get('chair', 'N/A')


def get_pathway_start_date(patient: dict) -> str:
    """Get pathway start date - handles multiple field names"""
    return (patient.get('clock_start_date') or 
            patient.get('pathway_start_date') or 
            patient.get('referral_date') or 
            '')


def get_updated_timestamp(record: dict) -> str:
    """Get last updated timestamp - handles both old and new field names"""
    return record.get('updated_at') or record.get('last_updated') or ''


def get_created_timestamp(record: dict) -> str:
    """Get created timestamp - handles both old and new field names"""
    return record.get('created_at') or record.get('created_date') or record.get('added_date') or ''


def get_decisions(meeting: dict) -> list:
    """Get decisions from MDT meeting - handles both old and new field names"""
    return meeting.get('decisions') or meeting.get('outcomes', [])


def get_milestones(patient: dict) -> list:
    """Get milestones - handles field existence"""
    return patient.get('milestones', [])


def get_treatments(patient: dict) -> list:
    """Get treatments - handles field existence"""
    return patient.get('treatments', [])
