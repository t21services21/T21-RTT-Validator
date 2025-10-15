"""
T21 EPISODE MANAGEMENT SYSTEM
Manage consultant, treatment, and diagnostic episodes

Episode Types:
1. Consultant Episodes - Patient under consultant care
2. Treatment Episodes - Patient receiving treatment
3. Diagnostic Episodes - Patient undergoing investigations

For: RTT pathway tracking and clinical management
"""

import json
import os
from datetime import datetime
from typing import Optional, Dict, List

# Import Supabase
try:
    from supabase_database import supabase
    SUPABASE_ENABLED = True
except ImportError:
    SUPABASE_ENABLED = False
    print("⚠️ Supabase not available - using local storage")


def get_current_user_email():
    """Get current logged-in user's email"""
    try:
        import streamlit as st
        return st.session_state.get('user_email', 'demo@t21services.co.uk')
    except:
        return 'demo@t21services.co.uk'


def generate_episode_id(episode_type: str) -> str:
    """Generate unique episode ID"""
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    prefix = {
        'consultant': 'CE',
        'treatment': 'TE',
        'diagnostic': 'DE'
    }.get(episode_type.lower(), 'EP')
    
    return f"{prefix}_{timestamp}"


# ============================================
# CONSULTANT EPISODES
# ============================================

def add_consultant_episode(
    patient_id: str,
    patient_name: str,
    consultant_name: str,
    specialty: str,
    start_date: str,
    reason: str,
    expected_duration_weeks: int = 12,
    priority: str = "Routine",
    referral_source: str = "GP",
    pathway_id: Optional[str] = None,
    notes: str = ""
) -> Dict:
    """Add new consultant episode"""
    
    user_email = get_current_user_email()
    episode_id = generate_episode_id('consultant')
    
    episode_data = {
        'episode_id': episode_id,
        'episode_type': 'consultant',
        'patient_id': patient_id,
        'patient_name': patient_name,
        'consultant_name': consultant_name,
        'specialty': specialty,
        'start_date': start_date,
        'end_date': None,
        'status': 'active',
        'reason': reason,
        'expected_duration_weeks': expected_duration_weeks,
        'priority': priority,
        'referral_source': referral_source,
        'pathway_id': pathway_id,
        'notes': notes,
        'created_date': datetime.now().isoformat(),
        'created_by': user_email,
        'user_email': user_email
    }
    
    if SUPABASE_ENABLED:
        try:
            result = supabase.table('episodes').insert(episode_data).execute()
            return {
                'success': True,
                'episode_id': episode_id,
                'message': f'Consultant episode created: {episode_id}'
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    else:
        save_episode_local(episode_data)
        return {
            'success': True,
            'episode_id': episode_id,
            'message': f'Consultant episode created: {episode_id}'
        }


# ============================================
# TREATMENT EPISODES
# ============================================

def add_treatment_episode(
    patient_id: str,
    patient_name: str,
    treatment_type: str,
    treatment_date: str,
    location: str,
    provider: str,
    consultant_episode_id: Optional[str] = None,
    pathway_id: Optional[str] = None,
    outcome: str = "",
    complications: str = "",
    notes: str = ""
) -> Dict:
    """Add new treatment episode"""
    
    user_email = get_current_user_email()
    episode_id = generate_episode_id('treatment')
    
    episode_data = {
        'episode_id': episode_id,
        'episode_type': 'treatment',
        'patient_id': patient_id,
        'patient_name': patient_name,
        'treatment_type': treatment_type,
        'treatment_date': treatment_date,
        'location': location,
        'provider': provider,
        'consultant_episode_id': consultant_episode_id,
        'pathway_id': pathway_id,
        'outcome': outcome,
        'complications': complications,
        'status': 'completed' if outcome else 'scheduled',
        'notes': notes,
        'created_date': datetime.now().isoformat(),
        'created_by': user_email,
        'user_email': user_email
    }
    
    if SUPABASE_ENABLED:
        try:
            result = supabase.table('episodes').insert(episode_data).execute()
            return {
                'success': True,
                'episode_id': episode_id,
                'message': f'Treatment episode created: {episode_id}'
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    else:
        save_episode_local(episode_data)
        return {
            'success': True,
            'episode_id': episode_id,
            'message': f'Treatment episode created: {episode_id}'
        }


# ============================================
# DIAGNOSTIC EPISODES
# ============================================

def add_diagnostic_episode(
    patient_id: str,
    patient_name: str,
    investigation_type: str,
    request_date: str,
    requested_by: str,
    performed_date: Optional[str] = None,
    results: str = "",
    consultant_episode_id: Optional[str] = None,
    pathway_id: Optional[str] = None,
    urgency: str = "Routine",
    location: str = "",
    notes: str = ""
) -> Dict:
    """Add new diagnostic episode"""
    
    user_email = get_current_user_email()
    episode_id = generate_episode_id('diagnostic')
    
    status = 'completed' if performed_date else 'requested'
    
    episode_data = {
        'episode_id': episode_id,
        'episode_type': 'diagnostic',
        'patient_id': patient_id,
        'patient_name': patient_name,
        'investigation_type': investigation_type,
        'request_date': request_date,
        'requested_by': requested_by,
        'performed_date': performed_date,
        'results': results,
        'consultant_episode_id': consultant_episode_id,
        'pathway_id': pathway_id,
        'urgency': urgency,
        'location': location,
        'status': status,
        'notes': notes,
        'created_date': datetime.now().isoformat(),
        'created_by': user_email,
        'user_email': user_email
    }
    
    if SUPABASE_ENABLED:
        try:
            result = supabase.table('episodes').insert(episode_data).execute()
            return {
                'success': True,
                'episode_id': episode_id,
                'message': f'Diagnostic episode created: {episode_id}'
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    else:
        save_episode_local(episode_data)
        return {
            'success': True,
            'episode_id': episode_id,
            'message': f'Diagnostic episode created: {episode_id}'
        }


# ============================================
# EPISODE QUERIES
# ============================================

def get_patient_episodes(patient_id: str) -> Dict:
    """Get all episodes for a patient"""
    user_email = get_current_user_email()
    
    if SUPABASE_ENABLED:
        try:
            result = supabase.table('episodes')\
                .select('*')\
                .eq('user_email', user_email)\
                .eq('patient_id', patient_id)\
                .order('created_date', desc=True)\
                .execute()
            
            episodes = result.data if result.data else []
            
            # Group by type
            consultant_episodes = [e for e in episodes if e.get('episode_type') == 'consultant']
            treatment_episodes = [e for e in episodes if e.get('episode_type') == 'treatment']
            diagnostic_episodes = [e for e in episodes if e.get('episode_type') == 'diagnostic']
            
            return {
                'all_episodes': episodes,
                'consultant': consultant_episodes,
                'treatment': treatment_episodes,
                'diagnostic': diagnostic_episodes,
                'total_count': len(episodes)
            }
        except Exception as e:
            print(f"Error fetching episodes: {e}")
            return {'all_episodes': [], 'consultant': [], 'treatment': [], 'diagnostic': [], 'total_count': 0}
    else:
        return get_patient_episodes_local(patient_id)


def get_all_episodes() -> List[Dict]:
    """Get all episodes for current user"""
    user_email = get_current_user_email()
    
    if SUPABASE_ENABLED:
        try:
            result = supabase.table('episodes')\
                .select('*')\
                .eq('user_email', user_email)\
                .order('created_date', desc=True)\
                .execute()
            
            return result.data if result.data else []
        except Exception as e:
            print(f"Error fetching episodes: {e}")
            return []
    else:
        return get_all_episodes_local()


def close_consultant_episode(episode_id: str, end_date: str, discharge_reason: str = "") -> Dict:
    """Close/end a consultant episode"""
    user_email = get_current_user_email()
    
    if SUPABASE_ENABLED:
        try:
            result = supabase.table('episodes')\
                .update({
                    'end_date': end_date,
                    'status': 'closed',
                    'discharge_reason': discharge_reason,
                    'closed_date': datetime.now().isoformat()
                })\
                .eq('episode_id', episode_id)\
                .eq('user_email', user_email)\
                .execute()
            
            return {'success': True, 'message': 'Episode closed successfully'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    else:
        return close_episode_local(episode_id, end_date, discharge_reason)


# ============================================
# LOCAL STORAGE (FALLBACK)
# ============================================

def save_episode_local(episode_data: Dict):
    """Save episode to local JSON file"""
    episodes_file = 'episodes.json'
    
    if os.path.exists(episodes_file):
        with open(episodes_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        data = {'episodes': []}
    
    data['episodes'].append(episode_data)
    
    with open(episodes_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def get_patient_episodes_local(patient_id: str) -> Dict:
    """Get patient episodes from local storage"""
    episodes_file = 'episodes.json'
    
    if not os.path.exists(episodes_file):
        return {'all_episodes': [], 'consultant': [], 'treatment': [], 'diagnostic': [], 'total_count': 0}
    
    with open(episodes_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    episodes = [e for e in data.get('episodes', []) if e.get('patient_id') == patient_id]
    
    consultant_episodes = [e for e in episodes if e.get('episode_type') == 'consultant']
    treatment_episodes = [e for e in episodes if e.get('episode_type') == 'treatment']
    diagnostic_episodes = [e for e in episodes if e.get('episode_type') == 'diagnostic']
    
    return {
        'all_episodes': episodes,
        'consultant': consultant_episodes,
        'treatment': treatment_episodes,
        'diagnostic': diagnostic_episodes,
        'total_count': len(episodes)
    }


def get_all_episodes_local() -> List[Dict]:
    """Get all episodes from local storage"""
    episodes_file = 'episodes.json'
    
    if not os.path.exists(episodes_file):
        return []
    
    with open(episodes_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    return data.get('episodes', [])


def close_episode_local(episode_id: str, end_date: str, discharge_reason: str) -> Dict:
    """Close episode in local storage"""
    episodes_file = 'episodes.json'
    
    if not os.path.exists(episodes_file):
        return {'success': False, 'error': 'Episodes file not found'}
    
    with open(episodes_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    for episode in data['episodes']:
        if episode.get('episode_id') == episode_id:
            episode['end_date'] = end_date
            episode['status'] = 'closed'
            episode['discharge_reason'] = discharge_reason
            episode['closed_date'] = datetime.now().isoformat()
            break
    
    with open(episodes_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    return {'success': True, 'message': 'Episode closed successfully'}


# ============================================
# STATISTICS
# ============================================

def get_episode_stats() -> Dict:
    """Get episode statistics"""
    episodes = get_all_episodes()
    
    total = len(episodes)
    consultant = len([e for e in episodes if e.get('episode_type') == 'consultant'])
    treatment = len([e for e in episodes if e.get('episode_type') == 'treatment'])
    diagnostic = len([e for e in episodes if e.get('episode_type') == 'diagnostic'])
    
    active = len([e for e in episodes if e.get('status') == 'active'])
    closed = len([e for e in episodes if e.get('status') == 'closed'])
    
    return {
        'total_episodes': total,
        'consultant_episodes': consultant,
        'treatment_episodes': treatment,
        'diagnostic_episodes': diagnostic,
        'active_episodes': active,
        'closed_episodes': closed
    }
