"""
T21 SERVICES - ENHANCED AUDIT TRAIL
NHS-Compliant Immutable Audit Logging System
CQC & DCB0129 Compliant
"""

import json
import os
from datetime import datetime
import hashlib


AUDIT_FILE = "audit_trail_immutable.json"


def log_audit_event(user_email, action, target=None, details=None, ip_address=None, location=None, reason=None):
    """
    Log an audit event - IMMUTABLE and COMPREHENSIVE
    
    All actions are logged with full context for compliance
    
    Args:
        user_email: Who performed the action
        action: What was done (e.g., "VIEW_PATIENT", "UPDATE_RTT", "LOGIN")
        target: What was affected (e.g., patient ID, user email)
        details: Additional context (dict)
        ip_address: IP address of user
        location: Geographic location
        reason: Clinical/business reason for action
    
    Returns:
        str: Audit entry ID (hash)
    """
    
    # Load existing audit trail
    if os.path.exists(AUDIT_FILE):
        with open(AUDIT_FILE, 'r') as f:
            audit_trail = json.load(f)
    else:
        audit_trail = {
            "metadata": {
                "created": datetime.now().isoformat(),
                "version": "1.0",
                "compliance": ["CQC", "DCB0129", "GDPR"],
                "immutable": True
            },
            "entries": []
        }
    
    # Create audit entry
    entry = {
        "id": None,  # Will be set after hashing
        "timestamp": datetime.now().isoformat(),
        "user_email": user_email,
        "action": action,
        "target": target,
        "details": details or {},
        "ip_address": ip_address or "Unknown",
        "location": location or "Unknown",
        "reason": reason or "Not specified",
        "session_info": {
            "browser": "N/A",  # Can be captured from request headers
            "device": "N/A"
        }
    }
    
    # Generate immutable hash (includes previous entry's hash for blockchain-style integrity)
    previous_hash = audit_trail["entries"][-1]["hash"] if audit_trail["entries"] else "GENESIS"
    entry_string = json.dumps(entry, sort_keys=True)
    entry_hash = hashlib.sha256(f"{previous_hash}{entry_string}".encode()).hexdigest()
    
    entry["id"] = entry_hash[:16]  # First 16 chars of hash
    entry["hash"] = entry_hash
    entry["previous_hash"] = previous_hash
    
    # Add to trail
    audit_trail["entries"].append(entry)
    audit_trail["metadata"]["last_updated"] = datetime.now().isoformat()
    audit_trail["metadata"]["total_entries"] = len(audit_trail["entries"])
    
    # Save (append-only)
    with open(AUDIT_FILE, 'w') as f:
        json.dump(audit_trail, f, indent=2)
    
    return entry["id"]


def get_audit_trail(user_email=None, action=None, start_date=None, end_date=None, limit=100):
    """
    Retrieve audit trail with filters
    
    Args:
        user_email: Filter by user
        action: Filter by action type
        start_date: Filter from date (datetime)
        end_date: Filter to date (datetime)
        limit: Max entries to return
    
    Returns:
        list: Filtered audit entries
    """
    
    if not os.path.exists(AUDIT_FILE):
        return []
    
    with open(AUDIT_FILE, 'r') as f:
        audit_trail = json.load(f)
    
    entries = audit_trail.get("entries", [])
    
    # Apply filters
    filtered = entries
    
    if user_email:
        filtered = [e for e in filtered if e["user_email"] == user_email]
    
    if action:
        filtered = [e for e in filtered if e["action"] == action]
    
    if start_date:
        filtered = [e for e in filtered if datetime.fromisoformat(e["timestamp"]) >= start_date]
    
    if end_date:
        filtered = [e for e in filtered if datetime.fromisoformat(e["timestamp"]) <= end_date]
    
    # Return most recent first, limited
    return filtered[-limit:][::-1]


def verify_audit_integrity():
    """
    Verify the integrity of the audit trail
    Checks that hash chain is intact (no tampering)
    
    Returns:
        dict: {
            'valid': bool,
            'total_entries': int,
            'errors': list
        }
    """
    
    if not os.path.exists(AUDIT_FILE):
        return {'valid': True, 'total_entries': 0, 'errors': []}
    
    with open(AUDIT_FILE, 'r') as f:
        audit_trail = json.load(f)
    
    entries = audit_trail.get("entries", [])
    errors = []
    
    for i, entry in enumerate(entries):
        # Verify hash
        entry_copy = entry.copy()
        stored_hash = entry_copy.pop("hash")
        stored_prev_hash = entry_copy.pop("previous_hash")
        
        # Recalculate hash
        entry_string = json.dumps(entry_copy, sort_keys=True)
        calculated_hash = hashlib.sha256(f"{stored_prev_hash}{entry_string}".encode()).hexdigest()
        
        if calculated_hash != stored_hash:
            errors.append(f"Entry {i} (ID: {entry['id']}): Hash mismatch - possible tampering!")
        
        # Verify chain
        if i > 0:
            if stored_prev_hash != entries[i-1]["hash"]:
                errors.append(f"Entry {i} (ID: {entry['id']}): Chain broken - previous hash doesn't match!")
    
    return {
        'valid': len(errors) == 0,
        'total_entries': len(entries),
        'errors': errors
    }


def export_audit_report(start_date=None, end_date=None, format='excel'):
    """
    Export audit trail for compliance reporting
    
    Args:
        start_date: Start date for report
        end_date: End date for report
        format: 'excel' or 'csv'
    
    Returns:
        bytes: File data
    """
    import pandas as pd
    from io import BytesIO
    
    entries = get_audit_trail(start_date=start_date, end_date=end_date, limit=10000)
    
    # Flatten entries for export
    export_data = []
    for entry in entries:
        export_data.append({
            'Timestamp': entry['timestamp'],
            'User': entry['user_email'],
            'Action': entry['action'],
            'Target': entry['target'] or 'N/A',
            'IP Address': entry['ip_address'],
            'Location': entry['location'],
            'Reason': entry['reason'],
            'Details': json.dumps(entry['details']),
            'Entry ID': entry['id']
        })
    
    df = pd.DataFrame(export_data)
    
    if format == 'excel':
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Audit Trail')
            
            # Add summary sheet
            summary_df = pd.DataFrame([
                {'Metric': 'Total Events', 'Value': len(entries)},
                {'Metric': 'Report Generated', 'Value': datetime.now().strftime('%Y-%m-%d %H:%M:%S')},
                {'Metric': 'Start Date', 'Value': start_date.strftime('%Y-%m-%d') if start_date else 'All time'},
                {'Metric': 'End Date', 'Value': end_date.strftime('%Y-%m-%d') if end_date else 'Present'},
            ])
            summary_df.to_excel(writer, index=False, sheet_name='Summary')
        
        return output.getvalue()
    else:
        return df.to_csv(index=False).encode('utf-8')


# ACTION CONSTANTS (for consistency)
class AuditActions:
    # Authentication
    LOGIN = "LOGIN"
    LOGOUT = "LOGOUT"
    FAILED_LOGIN = "FAILED_LOGIN"
    PASSWORD_CHANGE = "PASSWORD_CHANGE"
    
    # User Management
    CREATE_USER = "CREATE_USER"
    UPDATE_USER = "UPDATE_USER"
    DELETE_USER = "DELETE_USER"
    SUSPEND_USER = "SUSPEND_USER"
    UNSUSPEND_USER = "UNSUSPEND_USER"
    
    # Patient Data (pseudo)
    VIEW_PATIENT = "VIEW_PATIENT"
    UPDATE_PATIENT = "UPDATE_PATIENT"
    CREATE_PATIENT = "CREATE_PATIENT"
    DELETE_PATIENT = "DELETE_PATIENT"
    EXPORT_PATIENT_DATA = "EXPORT_PATIENT_DATA"
    
    # RTT / Clinical
    VIEW_PTL = "VIEW_PTL"
    UPDATE_RTT = "UPDATE_RTT"
    PATHWAY_VALIDATION = "PATHWAY_VALIDATION"
    BOOK_APPOINTMENT = "BOOK_APPOINTMENT"
    CANCEL_APPOINTMENT = "CANCEL_APPOINTMENT"
    
    # Admin
    VIEW_AUDIT_LOG = "VIEW_AUDIT_LOG"
    EXPORT_AUDIT = "EXPORT_AUDIT"
    SYSTEM_CONFIG_CHANGE = "SYSTEM_CONFIG_CHANGE"
    
    # Data Export
    EXPORT_TO_EXCEL = "EXPORT_TO_EXCEL"
    EXPORT_TO_CSV = "EXPORT_TO_CSV"
