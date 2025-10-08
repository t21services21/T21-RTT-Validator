"""
Database layer for T21 RTT Validator
Stores validation history, patient pathways, and analytics
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path

# Database file location
DB_PATH = Path(__file__).parent / "rtt_validation.db"

def init_database():
    """Initialize database with all required tables"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Table 1: Validation History
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS validations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            validation_date TEXT NOT NULL,
            validator_initials TEXT NOT NULL,
            patient_nhs_number TEXT,
            patient_name TEXT,
            rtt_code TEXT NOT NULL,
            clock_status TEXT,
            outcome TEXT,
            letter_text TEXT,
            actions_required INTEGER,
            actions_completed INTEGER,
            gaps_found INTEGER,
            compliance_rate REAL,
            flag_color TEXT,
            validation_comments TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Table 2: Patient Pathways
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patient_pathways (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nhs_number TEXT NOT NULL,
            patient_name TEXT,
            pathway_number TEXT,
            specialty TEXT,
            referral_date TEXT,
            clock_start_date TEXT,
            clock_stop_date TEXT,
            pathway_status TEXT,
            current_rtt_code TEXT,
            weeks_elapsed INTEGER,
            breach_status TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Table 3: Pathway Events (Timeline)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pathway_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pathway_id INTEGER,
            event_date TEXT NOT NULL,
            rtt_code TEXT NOT NULL,
            event_description TEXT,
            validator_initials TEXT,
            validation_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (pathway_id) REFERENCES patient_pathways(id),
            FOREIGN KEY (validation_id) REFERENCES validations(id)
        )
    """)
    
    # Table 4: Gap Analysis
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS gaps (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            validation_id INTEGER,
            gap_type TEXT NOT NULL,
            gap_description TEXT NOT NULL,
            priority TEXT,
            resolved BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (validation_id) REFERENCES validations(id)
        )
    """)
    
    # Table 5: Trust Rules Configuration
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS trust_rules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rule_name TEXT UNIQUE NOT NULL,
            rule_value TEXT NOT NULL,
            rule_description TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Table 6: Validator Notes
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS validator_notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            validation_id INTEGER,
            validator_initials TEXT NOT NULL,
            note_text TEXT NOT NULL,
            note_type TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (validation_id) REFERENCES validations(id)
        )
    """)
    
    # Table 7: Alerts
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            alert_type TEXT NOT NULL,
            alert_level TEXT NOT NULL,
            nhs_number TEXT,
            patient_name TEXT,
            message TEXT NOT NULL,
            acknowledged BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()


def save_validation(validation_data):
    """Save validation result to database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO validations (
            validation_date, validator_initials, patient_nhs_number, patient_name,
            rtt_code, clock_status, outcome, letter_text,
            actions_required, actions_completed, gaps_found, compliance_rate,
            flag_color, validation_comments
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        validation_data.get('validation_date'),
        validation_data.get('validator_initials'),
        validation_data.get('nhs_number'),
        validation_data.get('patient_name'),
        validation_data.get('rtt_code'),
        validation_data.get('clock_status'),
        validation_data.get('outcome'),
        validation_data.get('letter_text'),
        validation_data.get('actions_required'),
        validation_data.get('actions_completed'),
        validation_data.get('gaps_found'),
        validation_data.get('compliance_rate'),
        validation_data.get('flag_color'),
        validation_data.get('validation_comments')
    ))
    
    validation_id = cursor.lastrowid
    
    # Save gaps
    for gap in validation_data.get('gaps', []):
        cursor.execute("""
            INSERT INTO gaps (validation_id, gap_type, gap_description, priority)
            VALUES (?, ?, ?, ?)
        """, (validation_id, gap.get('type', 'General'), gap.get('description'), gap.get('priority', 'Medium')))
    
    conn.commit()
    conn.close()
    
    return validation_id


def get_validation_history(validator_initials=None, limit=100):
    """Get validation history"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    if validator_initials:
        cursor.execute("""
            SELECT * FROM validations 
            WHERE validator_initials = ?
            ORDER BY created_at DESC LIMIT ?
        """, (validator_initials, limit))
    else:
        cursor.execute("""
            SELECT * FROM validations 
            ORDER BY created_at DESC LIMIT ?
        """, (limit,))
    
    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return results


def get_dashboard_stats(validator_initials=None, date_from=None):
    """Get dashboard statistics"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    stats = {}
    
    # Base query condition
    where_clause = "1=1"
    params = []
    
    if validator_initials:
        where_clause += " AND validator_initials = ?"
        params.append(validator_initials)
    
    if date_from:
        where_clause += " AND validation_date >= ?"
        params.append(date_from)
    
    # Total validations
    cursor.execute(f"SELECT COUNT(*) as count FROM validations WHERE {where_clause}", params)
    stats['total_validations'] = cursor.fetchone()['count']
    
    # Pass rate
    cursor.execute(f"SELECT COUNT(*) as count FROM validations WHERE {where_clause} AND flag_color = 'GREEN'", params)
    green_count = cursor.fetchone()['count']
    stats['pass_rate'] = (green_count / stats['total_validations'] * 100) if stats['total_validations'] > 0 else 0
    
    # Average compliance
    cursor.execute(f"SELECT AVG(compliance_rate) as avg_compliance FROM validations WHERE {where_clause}", params)
    stats['avg_compliance'] = cursor.fetchone()['avg_compliance'] or 0
    
    # Most common gaps
    cursor.execute(f"""
        SELECT gap_description, COUNT(*) as count 
        FROM gaps g
        JOIN validations v ON g.validation_id = v.id
        WHERE {where_clause}
        GROUP BY gap_description
        ORDER BY count DESC
        LIMIT 10
    """, params)
    stats['common_gaps'] = [dict(row) for row in cursor.fetchall()]
    
    # Flag distribution
    cursor.execute(f"""
        SELECT flag_color, COUNT(*) as count 
        FROM validations 
        WHERE {where_clause}
        GROUP BY flag_color
    """, params)
    stats['flag_distribution'] = {row['flag_color']: row['count'] for row in cursor.fetchall()}
    
    conn.close()
    return stats


def create_alert(alert_type, alert_level, message, nhs_number=None, patient_name=None):
    """Create a new alert"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO alerts (alert_type, alert_level, nhs_number, patient_name, message)
        VALUES (?, ?, ?, ?, ?)
    """, (alert_type, alert_level, nhs_number, patient_name, message))
    
    conn.commit()
    conn.close()


def get_active_alerts():
    """Get unacknowledged alerts"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM alerts 
        WHERE acknowledged = 0 
        ORDER BY created_at DESC
    """)
    
    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return results


def acknowledge_alert(alert_id):
    """Mark alert as acknowledged"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("UPDATE alerts SET acknowledged = 1 WHERE id = ?", (alert_id,))
    
    conn.commit()
    conn.close()


# Initialize database on import
init_database()
