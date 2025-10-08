"""
Smart Alerts System for T21 RTT Validator
Automatic detection of critical issues and breach warnings
"""

from datetime import datetime, timedelta
from database import create_alert

def check_breach_alerts(referral_date_str, current_date_str=None):
    """
    Check for RTT breach alerts
    Returns list of alerts
    """
    alerts = []
    
    if not referral_date_str:
        return alerts
    
    try:
        referral_date = datetime.strptime(referral_date_str, '%d/%m/%Y')
        current_date = datetime.strptime(current_date_str, '%d/%m/%Y') if current_date_str else datetime.now()
        
        days_elapsed = (current_date - referral_date).days
        weeks_elapsed = days_elapsed / 7
        
        # 52-week breach (CRITICAL)
        if weeks_elapsed >= 52:
            alerts.append({
                'type': '52_WEEK_BREACH',
                'level': 'CRITICAL',
                'message': f'🚨 CRITICAL: 52-WEEK BREACH - {int(weeks_elapsed)} weeks elapsed since referral',
                'weeks': int(weeks_elapsed)
            })
        
        # 26-week breach (SERIOUS)
        elif weeks_elapsed >= 26:
            alerts.append({
                'type': '26_WEEK_BREACH',
                'level': 'HIGH',
                'message': f'⚠️ SERIOUS: 26-WEEK BREACH - {int(weeks_elapsed)} weeks elapsed since referral',
                'weeks': int(weeks_elapsed)
            })
        
        # 18-week approaching (WARNING)
        elif weeks_elapsed >= 16:
            weeks_remaining = 18 - weeks_elapsed
            alerts.append({
                'type': '18_WEEK_WARNING',
                'level': 'MEDIUM',
                'message': f'⏰ WARNING: Approaching 18-week target - {weeks_remaining:.1f} weeks remaining',
                'weeks': int(weeks_elapsed)
            })
    
    except:
        pass
    
    return alerts


def check_duplicate_pathway(nhs_number, specialty, pathway_date_str, tolerance_weeks=26):
    """
    Check for potential duplicate pathways
    """
    # This would check database - simplified for now
    alerts = []
    
    # In full implementation, query database for:
    # - Same NHS number
    # - Same specialty
    # - Within tolerance_weeks
    
    return alerts


def check_dna_pattern(nhs_number, dna_count=3):
    """
    Check if patient has pattern of DNAs
    """
    alerts = []
    
    # In full implementation, query database for DNA history
    # If patient has DNA'd multiple times, create alert
    
    return alerts


def validate_and_generate_alerts(validation_data):
    """
    Main function to check all alert conditions
    Returns: List of alerts
    """
    all_alerts = []
    
    # Breach alerts
    if validation_data.get('referral_date'):
        breach_alerts = check_breach_alerts(
            validation_data['referral_date'],
            validation_data.get('validation_date')
        )
        all_alerts.extend(breach_alerts)
    
    # Critical gaps alert
    gaps_found = validation_data.get('gaps_found', 0)
    if gaps_found >= 5:
        all_alerts.append({
            'type': 'HIGH_GAP_COUNT',
            'level': 'HIGH',
            'message': f'⚠️ HIGH GAP COUNT: {gaps_found} actions outstanding - immediate attention required'
        })
    
    # Urgent referral not prioritized
    if validation_data.get('urgent_referral') and validation_data.get('priority_flag') != 'Y':
        all_alerts.append({
            'type': 'URGENT_NOT_FLAGGED',
            'level': 'CRITICAL',
            'message': '🚨 URGENT REFERRAL: 2WW/Urgent flag NOT set in system - must expedite'
        })
    
    # PBL timeout
    if validation_data.get('on_pbl') and validation_data.get('pbl_weeks', 0) > 6:
        all_alerts.append({
            'type': 'PBL_TIMEOUT',
            'level': 'MEDIUM',
            'message': f'⏰ PBL TIMEOUT: Patient on PBL for {validation_data.get("pbl_weeks")} weeks - book appointment'
        })
    
    return all_alerts
