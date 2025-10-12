"""
UNIVERSAL CRUD SYSTEM
Provides Create, Read, Update, Delete functionality for all modules
"""

import streamlit as st
import json
import os
from datetime import datetime
import pandas as pd

def get_user_email_safe():
    """Get current user's email in file-safe format"""
    if 'user_email' in st.session_state:
        return st.session_state.user_email.replace('@', '_at_').replace('.', '_')
    return 'anonymous'

def create_record(module_name, record_data):
    """
    Create a new record in a module's data store
    
    Args:
        module_name: Name of module (e.g., 'dna_cases')
        record_data: Dictionary with record data
    
    Returns:
        bool: Success status
    """
    email_safe = get_user_email_safe()
    filename = f"data/{module_name}_{email_safe}.json"
    
    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)
    
    # Load existing records
    records = read_all_records(module_name)
    
    # Add timestamp and ID if not present
    if 'id' not in record_data:
        record_data['id'] = f"{module_name}_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
    if 'created_at' not in record_data:
        record_data['created_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if 'updated_at' not in record_data:
        record_data['updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Append new record
    records.append(record_data)
    
    # Save to file
    save_data = {
        'module': module_name,
        'user': st.session_state.get('user_email', 'unknown'),
        'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'total_records': len(records),
        'data': records
    }
    
    try:
        with open(filename, 'w') as f:
            json.dump(save_data, f, indent=2)
        return True
    except Exception as e:
        st.error(f"Error saving: {e}")
        return False

def read_all_records(module_name, default=None):
    """
    Read all records from a module's data store
    
    Args:
        module_name: Name of module
        default: Default value if no records exist
    
    Returns:
        list: List of records
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

def read_record_by_id(module_name, record_id):
    """
    Read a single record by ID
    
    Args:
        module_name: Name of module
        record_id: ID of record to retrieve
    
    Returns:
        dict: Record data or None if not found
    """
    records = read_all_records(module_name)
    
    for record in records:
        if record.get('id') == record_id:
            return record
    
    return None

def update_record(module_name, record_id, updated_data):
    """
    Update an existing record
    
    Args:
        module_name: Name of module
        record_id: ID of record to update
        updated_data: Dictionary with updated data
    
    Returns:
        bool: Success status
    """
    records = read_all_records(module_name)
    
    for i, record in enumerate(records):
        if record.get('id') == record_id:
            # Update the record
            updated_data['id'] = record_id  # Preserve ID
            updated_data['created_at'] = record.get('created_at')  # Preserve creation time
            updated_data['updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            records[i] = updated_data
            
            # Save back
            email_safe = get_user_email_safe()
            filename = f"data/{module_name}_{email_safe}.json"
            
            save_data = {
                'module': module_name,
                'user': st.session_state.get('user_email', 'unknown'),
                'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'total_records': len(records),
                'data': records
            }
            
            try:
                with open(filename, 'w') as f:
                    json.dump(save_data, f, indent=2)
                return True
            except Exception as e:
                st.error(f"Error updating: {e}")
                return False
    
    return False

def delete_record(module_name, record_id):
    """
    Delete a record by ID
    
    Args:
        module_name: Name of module
        record_id: ID of record to delete
    
    Returns:
        bool: Success status
    """
    records = read_all_records(module_name)
    
    # Filter out the record to delete
    new_records = [r for r in records if r.get('id') != record_id]
    
    if len(new_records) == len(records):
        # Record not found
        return False
    
    # Save updated list
    email_safe = get_user_email_safe()
    filename = f"data/{module_name}_{email_safe}.json"
    
    save_data = {
        'module': module_name,
        'user': st.session_state.get('user_email', 'unknown'),
        'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'total_records': len(new_records),
        'data': new_records
    }
    
    try:
        with open(filename, 'w') as f:
            json.dump(save_data, f, indent=2)
        return True
    except Exception as e:
        st.error(f"Error deleting: {e}")
        return False

def search_records(module_name, search_term, search_fields=None):
    """
    Search records by term in specified fields
    
    Args:
        module_name: Name of module
        search_term: Term to search for
        search_fields: List of fields to search in (None = all fields)
    
    Returns:
        list: Matching records
    """
    records = read_all_records(module_name)
    
    if not search_term:
        return records
    
    search_term = search_term.lower()
    results = []
    
    for record in records:
        if search_fields:
            # Search only specified fields
            for field in search_fields:
                if field in record:
                    if search_term in str(record[field]).lower():
                        results.append(record)
                        break
        else:
            # Search all fields
            record_str = json.dumps(record).lower()
            if search_term in record_str:
                results.append(record)
    
    return results

def render_record_table(records, columns_to_show=None, show_actions=True):
    """
    Render records as a table with optional action buttons
    
    Args:
        records: List of record dictionaries
        columns_to_show: List of column names to display (None = all)
        show_actions: Whether to show edit/delete buttons
    
    Returns:
        tuple: (selected_record_id, action) where action is 'edit', 'delete', or None
    """
    if not records:
        st.info("No records found")
        return None, None
    
    # Convert to DataFrame
    df = pd.DataFrame(records)
    
    # Select columns to show
    if columns_to_show:
        display_cols = [col for col in columns_to_show if col in df.columns]
        df_display = df[display_cols]
    else:
        df_display = df
    
    # Display table
    st.dataframe(df_display, use_container_width=True, hide_index=True)
    
    # Action buttons
    if show_actions and len(records) > 0:
        st.markdown("### Actions")
        cols = st.columns([3, 1, 1])
        
        with cols[0]:
            selected_id = st.selectbox(
                "Select record:",
                options=[r.get('id') for r in records],
                format_func=lambda x: f"Record: {x[:20]}..."
            )
        
        with cols[1]:
            if st.button("✏️ Edit", key=f"edit_{selected_id}", use_container_width=True):
                return selected_id, 'edit'
        
        with cols[2]:
            if st.button("🗑️ Delete", key=f"delete_{selected_id}", use_container_width=True, type="secondary"):
                return selected_id, 'delete'
    
    return None, None

def export_to_csv(records, filename="export.csv"):
    """
    Export records to CSV
    
    Args:
        records: List of record dictionaries
        filename: Name of CSV file
    
    Returns:
        str: CSV data as string
    """
    if not records:
        return None
    
    df = pd.DataFrame(records)
    return df.to_csv(index=False)
