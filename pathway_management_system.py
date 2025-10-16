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
    
    # Standard pathway prefixes
    standard_prefixes = {
        'rtt': 'RTT',
        'cancer_2ww': 'C2W',
        'cancer_62day': 'C62',
        'cancer_31day': 'C31',
        'other': 'PTH'
    }
    
    # Check if it's a standard pathway type
    if pathway_type.lower() in standard_prefixes:
        prefix = standard_prefixes[pathway_type.lower()]
    else:
        # For custom pathway types, create prefix from first 3 letters (uppercase)
        # e.g., "Diagnostic" -> "DIA_", "Screening" -> "SCR_"
        prefix = pathway_type[:3].upper().replace(' ', '')
        if len(prefix) < 3:
            prefix = 'PTH'  # Fallback if name too short
    
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
    notes: str = "",
    # NEW NHS Workflow fields
    referral_method: str = "",
    referral_received_date: str = "",
    clock_start_date: str = "",
    earliest_reasonable_offer_date: str = "",
    presenting_complaint: str = "",
    suspected_diagnosis: str = "",
    gp_name: str = "",
    gp_practice: str = "",
    patient_informed: bool = True,
    interpreter_required: bool = False,
    language_needed: str = "",
    additional_needs: str = ""
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
        'user_email': user_email,
        # NEW NHS Workflow fields
        'referral_method': referral_method,
        'referral_received_date': referral_received_date,
        'clock_start_date': clock_start_date or start_date,
        'earliest_reasonable_offer_date': earliest_reasonable_offer_date,
        'presenting_complaint': presenting_complaint,
        'suspected_diagnosis': suspected_diagnosis,
        'gp_name': gp_name,
        'gp_practice': gp_practice,
        'patient_informed': patient_informed,
        'interpreter_required': interpreter_required,
        'language_needed': language_needed,
        'additional_needs': additional_needs
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


# ============================================
# RTT CLOCK PAUSE/RESUME
# ============================================

def pause_pathway_clock(pathway_id: str, pause_reason: str, pause_start_date: str) -> Dict:
    """Pause RTT clock for pathway"""
    user_email = get_current_user_email()
    
    # Get current pathway to add to history
    pathway = get_pathway_by_id(pathway_id)
    if not pathway:
        return {'success': False, 'error': 'Pathway not found'}
    
    # Add to pause history
    pause_history = pathway.get('pause_history', [])
    pause_entry = {
        'pause_start': pause_start_date,
        'pause_reason': pause_reason,
        'paused_by': user_email,
        'paused_at': datetime.now().isoformat()
    }
    pause_history.append(pause_entry)
    
    update_data = {
        'clock_paused': True,
        'clock_status': 'paused',
        'pause_reason': pause_reason,
        'pause_start_date': pause_start_date,
        'pause_history': pause_history
    }
    
    if SUPABASE_ENABLED:
        try:
            result = supabase.table('pathways')\
                .update(update_data)\
                .eq('pathway_id', pathway_id)\
                .eq('user_email', user_email)\
                .execute()
            
            return {'success': True, 'message': 'RTT clock paused successfully'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    else:
        return update_pathway_local(pathway_id, update_data)


def resume_pathway_clock(pathway_id: str, resume_date: str) -> Dict:
    """Resume RTT clock for pathway"""
    user_email = get_current_user_email()
    
    # Get current pathway
    pathway = get_pathway_by_id(pathway_id)
    if not pathway:
        return {'success': False, 'error': 'Pathway not found'}
    
    if not pathway.get('clock_paused'):
        return {'success': False, 'error': 'Clock is not paused'}
    
    # Calculate pause duration
    pause_start = datetime.strptime(pathway.get('pause_start_date'), '%Y-%m-%d')
    resume_dt = datetime.strptime(resume_date, '%Y-%m-%d')
    pause_days = (resume_dt - pause_start).days
    
    # Update pause history
    pause_history = pathway.get('pause_history', [])
    if pause_history:
        pause_history[-1]['pause_end'] = resume_date
        pause_history[-1]['pause_days'] = pause_days
        pause_history[-1]['resumed_by'] = user_email
        pause_history[-1]['resumed_at'] = datetime.now().isoformat()
    
    # Calculate new totals
    total_pause_days = pathway.get('total_pause_days', 0) + pause_days
    
    # Recalculate breach date with pause days added
    original_breach_date = datetime.strptime(pathway.get('breach_date'), '%Y-%m-%d')
    new_breach_date = original_breach_date + timedelta(days=pause_days)
    
    # Recalculate days remaining
    today = datetime.now()
    days_remaining = (new_breach_date - today).days
    
    update_data = {
        'clock_paused': False,
        'clock_status': 'running',
        'pause_reason': None,
        'pause_start_date': None,
        'pause_end_date': resume_date,
        'total_pause_days': total_pause_days,
        'pause_history': pause_history,
        'breach_date': new_breach_date.strftime('%Y-%m-%d'),
        'days_remaining': days_remaining
    }
    
    if SUPABASE_ENABLED:
        try:
            result = supabase.table('pathways')\
                .update(update_data)\
                .eq('pathway_id', pathway_id)\
                .eq('user_email', user_email)\
                .execute()
            
            return {
                'success': True,
                'message': f'Clock resumed. {pause_days} days added to pathway.',
                'pause_days': pause_days,
                'new_breach_date': new_breach_date.strftime('%Y-%m-%d')
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    else:
        result = update_pathway_local(pathway_id, update_data)
        result['pause_days'] = pause_days
        result['new_breach_date'] = new_breach_date.strftime('%Y-%m-%d')
        return result


# ============================================
# MILESTONE DATE TRACKING
# ============================================

def record_milestone(pathway_id: str, milestone_type: str, milestone_date: str, **kwargs) -> Dict:
    """Record key NHS milestone date"""
    user_email = get_current_user_email()
    
    # Get pathway
    pathway = get_pathway_by_id(pathway_id)
    if not pathway:
        return {'success': False, 'error': 'Pathway not found'}
    
    # Calculate days from clock start
    clock_start = datetime.strptime(pathway.get('clock_start_date') or pathway.get('start_date'), '%Y-%m-%d')
    milestone_dt = datetime.strptime(milestone_date, '%Y-%m-%d')
    days_to_milestone = (milestone_dt - clock_start).days
    
    update_data = {}
    
    if milestone_type == 'first_appointment':
        update_data = {
            'first_appointment_date': milestone_date,
            'days_to_first_appointment': days_to_milestone,
            'first_appointment_attended': kwargs.get('attended', True)
        }
    
    elif milestone_type == 'decision_to_treat':
        update_data = {
            'decision_to_treat_date': milestone_date,
            'days_to_decision_to_treat': days_to_milestone
        }
    
    elif milestone_type == 'treatment':
        update_data = {
            'treatment_start_date': milestone_date,
            'days_to_treatment': days_to_milestone,
            'treatment_received': True
        }
    
    elif milestone_type == 'admission':
        update_data = {
            'admission_date': milestone_date
        }
    
    elif milestone_type == 'surgery':
        update_data = {
            'surgery_date': milestone_date
        }
    
    elif milestone_type == 'discharge':
        update_data = {
            'discharge_date': milestone_date,
            'days_to_discharge': days_to_milestone,
            'discharge_reason': kwargs.get('reason', ''),
            'discharge_destination': kwargs.get('destination', ''),
            'treatment_outcome': kwargs.get('outcome', ''),
            'follow_up_required': kwargs.get('follow_up_required', False),
            'follow_up_date': kwargs.get('follow_up_date', None)
        }
    
    if SUPABASE_ENABLED:
        try:
            result = supabase.table('pathways')\
                .update(update_data)\
                .eq('pathway_id', pathway_id)\
                .eq('user_email', user_email)\
                .execute()
            
            return {'success': True, 'message': f'{milestone_type.replace("_", " ").title()} recorded successfully'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    else:
        return update_pathway_local(pathway_id, update_data)


# ============================================
# RTT STATUS MANAGEMENT
# ============================================

def update_rtt_status(pathway_id: str, new_status: str) -> Dict:
    """Update RTT pathway status"""
    user_email = get_current_user_email()
    
    valid_statuses = [
        'active',
        'paused',
        'active_monitoring',
        'suspended',
        'completed',
        'removed_died',
        'removed_moved',
        'removed_declined',
        'cancelled'
    ]
    
    if new_status not in valid_statuses:
        return {'success': False, 'error': f'Invalid status. Must be one of: {valid_statuses}'}
    
    update_data = {
        'rtt_status': new_status
    }
    
    # Adjust clock status based on RTT status
    if new_status == 'paused':
        update_data['clock_status'] = 'paused'
    elif new_status in ['completed', 'removed_died', 'removed_moved', 'removed_declined', 'cancelled']:
        update_data['clock_status'] = 'stopped'
        update_data['status'] = 'closed'
    else:
        update_data['clock_status'] = 'running'
    
    if SUPABASE_ENABLED:
        try:
            result = supabase.table('pathways')\
                .update(update_data)\
                .eq('pathway_id', pathway_id)\
                .eq('user_email', user_email)\
                .execute()
            
            return {'success': True, 'message': f'RTT status updated to: {new_status}'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    else:
        return update_pathway_local(pathway_id, update_data)
