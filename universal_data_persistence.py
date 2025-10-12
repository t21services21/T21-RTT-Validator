"""
UNIVERSAL DATA PERSISTENCE SYSTEM
Ensures ALL module data persists across sessions for each user
"""

import json
import os
from datetime import datetime
import streamlit as st

def get_user_email_safe():
    """Get current user's email in file-safe format"""
    if 'user_email' in st.session_state:
        return st.session_state.user_email.replace('@', '_at_').replace('.', '_')
    return 'anonymous'

def save_user_data(module_name, data):
    """
    Save data for a specific module and user
    
    Args:
        module_name: Name of module (e.g., 'cancer_patients', 'dna_cases')
        data: Data to save (list or dict)
    """
    email_safe = get_user_email_safe()
    filename = f"data/{module_name}_{email_safe}.json"
    
    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)
    
    # Add metadata
    save_data = {
        'module': module_name,
        'user': st.session_state.get('user_email', 'unknown'),
        'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'data': data
    }
    
    try:
        with open(filename, 'w') as f:
            json.dump(save_data, f, indent=2)
        return True
    except Exception as e:
        st.error(f"Error saving data: {e}")
        return False

def load_user_data(module_name, default=None):
    """
    Load data for a specific module and user
    
    Args:
        module_name: Name of module (e.g., 'cancer_patients', 'dna_cases')
        default: Default value if file doesn't exist
    
    Returns:
        Loaded data or default value
    """
    email_safe = get_user_email_safe()
    filename = f"data/{module_name}_{email_safe}.json"
    
    if default is None:
        default = []
    
    if os.path.exists(filename):
        try:
            with open(filename, 'r') as f:
                loaded = json.load(f)
                return loaded.get('data', default)
        except Exception as e:
            st.warning(f"Error loading data: {e}")
            return default
    
    return default

def append_user_data(module_name, new_item):
    """
    Append new item to user's data for a module
    
    Args:
        module_name: Name of module
        new_item: New item to append (dict)
    """
    current_data = load_user_data(module_name, default=[])
    
    if not isinstance(current_data, list):
        current_data = [current_data]
    
    current_data.append(new_item)
    return save_user_data(module_name, current_data)

def update_user_data_item(module_name, item_id, updated_item, id_field='id'):
    """
    Update specific item in user's data
    
    Args:
        module_name: Name of module
        item_id: ID of item to update
        updated_item: Updated item data
        id_field: Field name used as ID
    """
    current_data = load_user_data(module_name, default=[])
    
    for i, item in enumerate(current_data):
        if item.get(id_field) == item_id:
            current_data[i] = updated_item
            return save_user_data(module_name, current_data)
    
    return False

def delete_user_data_item(module_name, item_id, id_field='id'):
    """
    Delete specific item from user's data
    
    Args:
        module_name: Name of module
        item_id: ID of item to delete
        id_field: Field name used as ID
    """
    current_data = load_user_data(module_name, default=[])
    
    current_data = [item for item in current_data if item.get(id_field) != item_id]
    
    return save_user_data(module_name, current_data)

def get_all_user_modules():
    """Get list of all modules user has data for"""
    email_safe = get_user_email_safe()
    data_dir = "data"
    
    if not os.path.exists(data_dir):
        return []
    
    user_files = []
    for filename in os.listdir(data_dir):
        if filename.endswith(f"_{email_safe}.json"):
            module_name = filename.replace(f"_{email_safe}.json", "")
            user_files.append(module_name)
    
    return user_files

# Module-specific helpers
def save_cancer_patients(patients):
    """Save cancer patients for current user"""
    return save_user_data('cancer_patients', patients)

def load_cancer_patients():
    """Load cancer patients for current user"""
    return load_user_data('cancer_patients', default=[])

def save_dna_cases(cases):
    """Save DNA cases for current user"""
    return save_user_data('dna_cases', cases)

def load_dna_cases():
    """Load DNA cases for current user"""
    return load_user_data('dna_cases', default=[])

def save_cancellations(cancellations):
    """Save cancellations for current user"""
    return save_user_data('cancellations', cancellations)

def load_cancellations():
    """Load cancellations for current user"""
    return load_user_data('cancellations', default=[])

def save_patient_choice(choices):
    """Save patient choice records for current user"""
    return save_user_data('patient_choice', choices)

def load_patient_choice():
    """Load patient choice records for current user"""
    return load_user_data('patient_choice', default=[])

def save_transfers(transfers):
    """Save transfer records for current user"""
    return save_user_data('transfers', transfers)

def load_transfers():
    """Load transfer records for current user"""
    return load_user_data('transfers', default=[])

def save_clinical_exceptions(exceptions):
    """Save clinical exceptions for current user"""
    return save_user_data('clinical_exceptions', exceptions)

def load_clinical_exceptions():
    """Load clinical exceptions for current user"""
    return load_user_data('clinical_exceptions', default=[])

def save_capacity_plans(plans):
    """Save capacity plans for current user"""
    return save_user_data('capacity_plans', plans)

def load_capacity_plans():
    """Load capacity plans for current user"""
    return load_user_data('capacity_plans', default=[])

def save_mdt_coordination(mdt_data):
    """Save MDT coordination data for current user"""
    return save_user_data('mdt_coordination', mdt_data)

def load_mdt_coordination():
    """Load MDT coordination data for current user"""
    return load_user_data('mdt_coordination', default=[])
