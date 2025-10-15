"""
T21 PATHWAY MANAGEMENT SYSTEM
Complete pathway creation and management for RTT and Cancer pathways

HIERARCHY:
Patient → Pathway → Episodes → Appointments

Features:
- Create RTT pathways (18-week)
- Create Cancer pathways (2WW, 62-day, 31-day)
- Link episodes to pathways
- Track pathway progress
- Calculate breach dates
- Timeline view
- Close pathways

For: NHS trusts and TQUK training
"""

import json
import os
from datetime import datetime, timedelta
from typing import Optional, Dict, List

# Import Supabase
try:
    from supabase_database import supabase
    SUPABASE_ENABLED = True
except ImportError:
    SUPABASE_ENABLED = False
    print("⚠️ Supabase not available - using local storage")

# Check if pathways table exists
if SUPABASE_ENABLED:
    try:
        test = supabase.table('pathways').select('*').limit(1).execute()
    except Exception as e:
        if 'Could not find the table' in str(e):
            print("⚠️ Pathways table not found in Supabase - using local storage")
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


def generate_pathway_id(pathway_type: str) -> str:
    """Generate unique pathway ID"""
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    prefix = {
        'rtt': 'RTT',
        'cancer_2ww': 'C2W',
        'cancer_62day': 'C62',
        'cancer_31day': 'C31',
        'other': 'PTH'
    }.get(pathway_type.lower(), 'PTH')
    
    return f"{prefix}_{timestamp}"


def calculate_breach_date(start_date: str, pathway_type: str) -> Dict:
    """Calculate breach date based on pathway type"""
    start = datetime.strptime(start_date, '%Y-%m-%d')
    
    # Breach timeframes
    timeframes = {
        'rtt': 126,  # 18 weeks = 126 days
        'cancer_2ww': 14,  # 2 weeks
        'cancer_62day': 62,  # 62 days
        'cancer_31day': 31,  # 31 days
        'other': 126  # Default to 18 weeks
    }
    
    days = timeframes.get(pathway_type, 126)
    breach_date = start + timedelta(days=days)
    
    # Calculate days remaining
    today = datetime.now()
    days_elapsed = (today - start).days
    days_remaining = days - days_elapsed
    
    # Determine risk level
    if days_remaining < 0:
        risk_level = 'breached'
        status = '🔴 BREACHED'
    elif days_remaining <= 7:
        risk_level = 'critical'
        status = '🔴 CRITICAL'
    elif days_remaining <= 14:
        risk_level = 'high'
        status = '🟠 HIGH RISK'
    elif days_remaining <= 30:
        risk_level = 'medium'
        status = '🟡 MEDIUM'
    else:
        risk_level = 'low'
        status = '🟢 LOW RISK'
    
    return {
        'breach_date': breach_date.strftime('%Y-%m-%d'),
        'days_total': days,
        'days_elapsed': days_elapsed,
        'days_remaining': days_remaining,
        'risk_level': risk_level,
        'status': status
    }


# ============================================
# CREATE PATHWAY
# ============================================

def create_pathway(
    patient_id: str,
    patient_name: str,
    pathway_type: str,
    start_date: str,
    specialty: str = "",
    consultant: str = "",
    referral_source: str = "GP",
    priority: str = "Routine",
    reason: str = "",
    notes: str = ""
) -> Dict:
    """Create new pathway for patient"""
    
    user_email = get_current_user_email()
    pathway_id = generate_pathway_id(pathway_type)
    
    # Calculate breach info
    breach_info = calculate_breach_date(start_date, pathway_type)
    
    # Pathway name
    pathway_names = {
        'rtt': 'RTT 18-Week Pathway',
        'cancer_2ww': 'Cancer 2-Week Wait',
        'cancer_62day': 'Cancer 62-Day Pathway',
        'cancer_31day': 'Cancer 31-Day Pathway',
        'other': 'Other Pathway'
    }
    
    pathway_data = {
        'pathway_id': pathway_id,
        'pathway_type': pathway_type,
        'pathway_name': pathway_names.get(pathway_type, 'Other Pathway'),
        'patient_id': patient_id,
        'patient_name': patient_name,
        'start_date': start_date,
        'breach_date': breach_info['breach_date'],
        'status': 'active',
        'specialty': specialty,
        'consultant': consultant,
        'referral_source': referral_source,
        'priority': priority,
        'reason': reason,
        'notes': notes,
        'clock_status': 'running',
        'days_elapsed': breach_info['days_elapsed'],
        'days_remaining': breach_info['days_remaining'],
        'risk_level': breach_info['risk_level'],
        'created_date': datetime.now().isoformat(),
        'created_by': user_email,
        'user_email': user_email
    }
    
    if SUPABASE_ENABLED:
        try:
            result = supabase.table('pathways').insert(pathway_data).execute()
            return {
                'success': True,
                'pathway_id': pathway_id,
                'breach_date': breach_info['breach_date'],
                'message': f'Pathway created: {pathway_id}'
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    else:
        save_pathway_local(pathway_data)
        return {
            'success': True,
            'pathway_id': pathway_id,
            'breach_date': breach_info['breach_date'],
            'message': f'Pathway created: {pathway_id}'
        }


# ============================================
# QUERY PATHWAYS
# ============================================

def get_patient_pathways(patient_id: str) -> List[Dict]:
    """Get all pathways for a patient"""
    user_email = get_current_user_email()
    
    if SUPABASE_ENABLED:
        try:
            result = supabase.table('pathways')\
                .select('*')\
                .eq('user_email', user_email)\
                .eq('patient_id', patient_id)\
                .order('created_date', desc=True)\
                .execute()
            
            return result.data if result.data else []
        except Exception as e:
            print(f"Error fetching pathways: {e}")
            return []
    else:
        return get_patient_pathways_local(patient_id)


def get_all_pathways() -> List[Dict]:
    """Get all pathways for current user"""
    user_email = get_current_user_email()
    
    if SUPABASE_ENABLED:
        try:
            result = supabase.table('pathways')\
                .select('*')\
                .eq('user_email', user_email)\
                .order('created_date', desc=True)\
                .execute()
            
            return result.data if result.data else []
        except Exception as e:
            print(f"Error fetching pathways: {e}")
            return []
    else:
        return get_all_pathways_local()


def get_pathway_by_id(pathway_id: str) -> Optional[Dict]:
    """Get pathway details by ID"""
    user_email = get_current_user_email()
    
    if SUPABASE_ENABLED:
        try:
            result = supabase.table('pathways')\
                .select('*')\
                .eq('user_email', user_email)\
                .eq('pathway_id', pathway_id)\
                .execute()
            
            if result.data:
                return result.data[0]
            return None
        except Exception as e:
            print(f"Error fetching pathway: {e}")
            return None
    else:
        return get_pathway_local(pathway_id)


def update_pathway_progress(pathway_id: str) -> Dict:
    """Update pathway progress (recalculate days elapsed/remaining)"""
    pathway = get_pathway_by_id(pathway_id)
    
    if not pathway:
        return {'success': False, 'error': 'Pathway not found'}
    
    # Recalculate breach info
    breach_info = calculate_breach_date(pathway['start_date'], pathway['pathway_type'])
    
    update_data = {
        'days_elapsed': breach_info['days_elapsed'],
        'days_remaining': breach_info['days_remaining'],
        'risk_level': breach_info['risk_level']
    }
    
    if SUPABASE_ENABLED:
        try:
            result = supabase.table('pathways')\
                .update(update_data)\
                .eq('pathway_id', pathway_id)\
                .execute()
            
            return {'success': True, 'message': 'Pathway updated'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    else:
        return update_pathway_local(pathway_id, update_data)


def close_pathway(pathway_id: str, end_date: str, outcome: str = "", notes: str = "") -> Dict:
    """Close/complete pathway"""
    user_email = get_current_user_email()
    
    update_data = {
        'status': 'closed',
        'end_date': end_date,
        'clock_status': 'stopped',
        'outcome': outcome,
        'closing_notes': notes,
        'closed_date': datetime.now().isoformat()
    }
    
    if SUPABASE_ENABLED:
        try:
            result = supabase.table('pathways')\
                .update(update_data)\
                .eq('pathway_id', pathway_id)\
                .eq('user_email', user_email)\
                .execute()
            
            return {'success': True, 'message': 'Pathway closed successfully'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    else:
        return update_pathway_local(pathway_id, update_data)


# ============================================
# LOCAL STORAGE (FALLBACK)
# ============================================

def save_pathway_local(pathway_data: Dict):
    """Save pathway to local JSON file"""
    pathways_file = 'pathways.json'
    
    if os.path.exists(pathways_file):
        with open(pathways_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        data = {'pathways': []}
    
    data['pathways'].append(pathway_data)
    
    with open(pathways_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def get_patient_pathways_local(patient_id: str) -> List[Dict]:
    """Get patient pathways from local storage"""
    pathways_file = 'pathways.json'
    
    if not os.path.exists(pathways_file):
        return []
    
    with open(pathways_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    return [p for p in data.get('pathways', []) if p.get('patient_id') == patient_id]


def get_all_pathways_local() -> List[Dict]:
    """Get all pathways from local storage"""
    pathways_file = 'pathways.json'
    
    if not os.path.exists(pathways_file):
        return []
    
    with open(pathways_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    return data.get('pathways', [])


def get_pathway_local(pathway_id: str) -> Optional[Dict]:
    """Get pathway from local storage"""
    pathways_file = 'pathways.json'
    
    if not os.path.exists(pathways_file):
        return None
    
    with open(pathways_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    for pathway in data.get('pathways', []):
        if pathway.get('pathway_id') == pathway_id:
            return pathway
    
    return None


def update_pathway_local(pathway_id: str, update_data: Dict) -> Dict:
    """Update pathway in local storage"""
    pathways_file = 'pathways.json'
    
    if not os.path.exists(pathways_file):
        return {'success': False, 'error': 'Pathways file not found'}
    
    with open(pathways_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    for pathway in data['pathways']:
        if pathway.get('pathway_id') == pathway_id:
            pathway.update(update_data)
            break
    
    with open(pathways_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    return {'success': True, 'message': 'Pathway updated'}


# ============================================
# STATISTICS
# ============================================

def get_pathway_stats() -> Dict:
    """Get pathway statistics"""
    pathways = get_all_pathways()
    
    total = len(pathways)
    active = len([p for p in pathways if p.get('status') == 'active'])
    closed = len([p for p in pathways if p.get('status') == 'closed'])
    
    # By type
    rtt = len([p for p in pathways if p.get('pathway_type') == 'rtt'])
    cancer = len([p for p in pathways if 'cancer' in p.get('pathway_type', '')])
    
    # By risk
    breached = len([p for p in pathways if p.get('risk_level') == 'breached'])
    critical = len([p for p in pathways if p.get('risk_level') == 'critical'])
    high_risk = len([p for p in pathways if p.get('risk_level') == 'high'])
    
    return {
        'total_pathways': total,
        'active_pathways': active,
        'closed_pathways': closed,
        'rtt_pathways': rtt,
        'cancer_pathways': cancer,
        'breached': breached,
        'critical_risk': critical,
        'high_risk': high_risk
    }
