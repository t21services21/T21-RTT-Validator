"""
PATHWAY STATUS AUTOMATION - NHS Workflow
Automatically updates pathway status based on last episode's RTT code

NHS Rule: The last episode's RTT code determines the pathway status
- Clock Stop Codes (30-96) → Pathway CLOSED
- Clock Continue Codes (10-21) → Pathway ACTIVE
- Code 11 after closed pathway → RESTARTS clock (NEW pathway period)
"""

from typing import Dict, Optional
from datetime import datetime

# RTT Clock Stop Codes (Pathway should be CLOSED)
CLOCK_STOP_CODES = [
    '30',  # Treatment - Clock Stop
    '31',  # Patient declined treatment
    '32',  # Patient DNA (Did Not Attend) - Clock Stop
    '34',  # Discharged - no further treatment needed
    '91',  # Patient DNA'd 2+ times - removed from pathway
    '92',  # Patient no longer requires treatment
    '93',  # Patient moved out of area
    '94',  # Patient died
    '95',  # Patient requested removal
    '96',  # Other admin removal
]

# RTT Clock Continue Codes (Pathway remains ACTIVE)
CLOCK_CONTINUE_CODES = [
    '10',  # First Outpatient Attendance - New referral
    '11',  # Active Monitoring Starter - Clock RESTART after previous stop
    '12',  # Consultant-to-Consultant for NEW condition
    '20',  # Clock continues - awaiting treatment
    '21',  # Clock continues - further outpatient
]


def determine_pathway_status_from_episode(episode_code: str, episode_status: str = None) -> str:
    """
    Determine pathway status based on episode code
    
    Args:
        episode_code: RTT code or episode status code
        episode_status: Alternative status field
    
    Returns:
        'closed' or 'active'
    """
    # Check both episode_code and episode_status fields
    code_to_check = episode_code or episode_status or ''
    code_str = str(code_to_check).strip()
    
    # Check if it's a clock stop code
    if code_str in CLOCK_STOP_CODES:
        return 'closed'
    
    # Check if it's a clock continue code
    if code_str in CLOCK_CONTINUE_CODES:
        return 'active'
    
    # Default: if code not recognized, keep active
    return 'active'


def check_if_code_11_restart(episode_code: str, pathway_current_status: str) -> bool:
    """
    Check if this is a Code 11 restart scenario
    
    Args:
        episode_code: The new episode's code
        pathway_current_status: Current pathway status
    
    Returns:
        True if this is a Code 11 restart (pathway was closed, now restarting)
    """
    return episode_code == '11' and pathway_current_status == 'closed'


def update_pathway_status_from_episodes(pathway_id: str) -> Dict:
    """
    Update pathway status based on all its episodes (uses LAST episode)
    
    NHS Logic:
    1. Get all episodes for pathway
    2. Find the most recent episode (by date)
    3. Check its RTT code
    4. Update pathway status accordingly
    
    Args:
        pathway_id: Pathway to update
    
    Returns:
        Result dict with success status
    """
    try:
        # Import here to avoid circular dependencies
        from episode_management_system import get_patient_episodes
        from pathway_management_system import update_pathway_status_auto
        
        # Get pathway details first
        try:
            from pathway_management_system import get_pathway_by_id
            pathway = get_pathway_by_id(pathway_id)
            if not pathway:
                return {'success': False, 'error': 'Pathway not found'}
            
            patient_id = pathway.get('patient_id')
        except Exception as e:
            return {'success': False, 'error': f'Could not get pathway: {e}'}
        
        # Get all episodes for this patient
        episodes_data = get_patient_episodes(patient_id)
        all_episodes = episodes_data.get('all_episodes', [])
        
        # Filter episodes for this specific pathway
        pathway_episodes = [ep for ep in all_episodes if ep.get('pathway_id') == pathway_id]
        
        if not pathway_episodes:
            # No episodes yet - keep pathway active
            return {'success': True, 'message': 'No episodes yet, pathway remains active', 'status': 'active'}
        
        # Sort by date to find LAST episode
        sorted_episodes = sorted(
            pathway_episodes,
            key=lambda x: x.get('start_date') or x.get('created_date') or '1900-01-01',
            reverse=True  # Most recent first
        )
        
        last_episode = sorted_episodes[0]
        
        # Get the RTT code from episode
        episode_code = last_episode.get('episode_code') or last_episode.get('status') or ''
        
        # Determine new pathway status
        new_status = determine_pathway_status_from_episode(episode_code)
        
        # Check for Code 11 restart scenario
        current_status = pathway.get('status', 'active')
        is_code_11_restart = check_if_code_11_restart(episode_code, current_status)
        
        if is_code_11_restart:
            # Code 11 after closed pathway = RESTART clock
            new_status = 'active'
            message = f'Code 11 detected: Restarting pathway after previous closure'
        else:
            message = f'Pathway status updated based on last episode (Code: {episode_code})'
        
        # Update pathway status
        try:
            update_pathway_status_auto(pathway_id, new_status)
            return {
                'success': True,
                'message': message,
                'status': new_status,
                'last_episode_code': episode_code,
                'last_episode_id': last_episode.get('episode_id')
            }
        except Exception as e:
            return {'success': False, 'error': f'Failed to update pathway: {e}'}
    
    except Exception as e:
        return {'success': False, 'error': f'Error updating pathway status: {e}'}


def get_episode_code_description(code: str) -> str:
    """Get description of RTT code"""
    code_descriptions = {
        '10': 'First Outpatient - New referral',
        '11': 'Active Monitoring Starter - Clock RESTART',
        '12': 'Consultant-to-Consultant - NEW condition',
        '20': 'Clock continues - Awaiting treatment',
        '21': 'Clock continues - Further outpatient',
        '30': 'Treatment - Clock STOP',
        '31': 'Patient declined treatment - Clock STOP',
        '32': 'Patient DNA - Clock STOP',
        '34': 'Discharged - Clock STOP',
        '91': 'Patient DNA 2+ times - Removed',
        '92': 'No longer requires treatment',
        '93': 'Patient moved out of area',
        '94': 'Patient died',
        '95': 'Patient requested removal',
        '96': 'Other admin removal'
    }
    return code_descriptions.get(str(code), f'Code {code}')


def validate_episode_code(code: str) -> Dict:
    """
    Validate if episode code is a valid RTT code
    
    Returns:
        Dict with validation result and code type
    """
    code_str = str(code).strip()
    
    if code_str in CLOCK_STOP_CODES:
        return {
            'valid': True,
            'type': 'clock_stop',
            'description': get_episode_code_description(code_str),
            'pathway_action': 'Pathway will be CLOSED'
        }
    
    if code_str in CLOCK_CONTINUE_CODES:
        return {
            'valid': True,
            'type': 'clock_continue',
            'description': get_episode_code_description(code_str),
            'pathway_action': 'Pathway remains ACTIVE'
        }
    
    return {
        'valid': False,
        'type': 'unknown',
        'description': 'Not a recognized RTT code',
        'pathway_action': 'No automatic pathway status change'
    }
