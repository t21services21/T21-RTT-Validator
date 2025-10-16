"""
PERFORMANCE OPTIMIZATION UTILITIES
Improves platform speed and responsiveness

Features:
- Data caching for faster page loads
- Pagination for large datasets
- Query optimization
- Lazy loading
- Session state management
"""

import streamlit as st
from functools import wraps
from datetime import datetime, timedelta
from typing import Any, Callable, List, Dict
import time

# ============================================
# CACHING UTILITIES
# ============================================

def cache_for_session(timeout_minutes: int = 15):
    """
    Cache function results in session state
    Useful for expensive database queries
    
    Usage:
        @cache_for_session(timeout_minutes=15)
        def get_all_patients():
            return expensive_database_query()
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Create cache key from function name and arguments
            cache_key = f"cache_{func.__name__}_{str(args)}_{str(kwargs)}"
            timeout_key = f"{cache_key}_timeout"
            
            # Check if cached and not expired
            if cache_key in st.session_state:
                if timeout_key in st.session_state:
                    if datetime.now() < st.session_state[timeout_key]:
                        return st.session_state[cache_key]
            
            # Call function and cache result
            result = func(*args, **kwargs)
            st.session_state[cache_key] = result
            st.session_state[timeout_key] = datetime.now() + timedelta(minutes=timeout_minutes)
            
            return result
        
        return wrapper
    return decorator


def clear_cache(prefix: str = ""):
    """
    Clear cached data from session state
    
    Usage:
        clear_cache("cache_get_all_patients")  # Clear specific cache
        clear_cache()  # Clear all caches
    """
    keys_to_delete = []
    for key in st.session_state.keys():
        if key.startswith(f"cache_{prefix}"):
            keys_to_delete.append(key)
    
    for key in keys_to_delete:
        del st.session_state[key]


# ============================================
# PAGINATION UTILITIES
# ============================================

class Paginator:
    """
    Paginate large datasets for better performance
    
    Usage:
        paginator = Paginator(all_patients, items_per_page=25)
        current_page_data = paginator.get_current_page()
        paginator.render_controls()
    """
    
    def __init__(self, data: List[Any], items_per_page: int = 25, key: str = "default"):
        self.data = data
        self.items_per_page = items_per_page
        self.total_items = len(data)
        self.total_pages = max(1, (self.total_items + items_per_page - 1) // items_per_page)
        self.key = key
        
        # Initialize current page in session state
        if f"page_{key}" not in st.session_state:
            st.session_state[f"page_{key}"] = 1
    
    def get_current_page(self) -> List[Any]:
        """Get data for current page"""
        current_page = st.session_state[f"page_{self.key}"]
        start_idx = (current_page - 1) * self.items_per_page
        end_idx = start_idx + self.items_per_page
        return self.data[start_idx:end_idx]
    
    def render_controls(self):
        """Render pagination controls"""
        current_page = st.session_state[f"page_{self.key}"]
        
        col1, col2, col3, col4, col5 = st.columns([1, 1, 2, 1, 1])
        
        with col1:
            if st.button("⏮️ First", key=f"first_{self.key}", disabled=(current_page == 1)):
                st.session_state[f"page_{self.key}"] = 1
                st.rerun()
        
        with col2:
            if st.button("◀️ Previous", key=f"prev_{self.key}", disabled=(current_page == 1)):
                st.session_state[f"page_{self.key}"] = max(1, current_page - 1)
                st.rerun()
        
        with col3:
            st.markdown(f"<div style='text-align: center; padding: 8px;'>Page {current_page} of {self.total_pages} ({self.total_items} total items)</div>", unsafe_allow_html=True)
        
        with col4:
            if st.button("▶️ Next", key=f"next_{self.key}", disabled=(current_page >= self.total_pages)):
                st.session_state[f"page_{self.key}"] = min(self.total_pages, current_page + 1)
                st.rerun()
        
        with col5:
            if st.button("⏭️ Last", key=f"last_{self.key}", disabled=(current_page >= self.total_pages)):
                st.session_state[f"page_{self.key}"] = self.total_pages
                st.rerun()


# ============================================
# PERFORMANCE MONITORING
# ============================================

class PerformanceMonitor:
    """
    Monitor function execution time
    
    Usage:
        with PerformanceMonitor("Load Patients"):
            patients = load_all_patients()
    """
    
    def __init__(self, operation_name: str, show_in_ui: bool = False):
        self.operation_name = operation_name
        self.show_in_ui = show_in_ui
        self.start_time = None
    
    def __enter__(self):
        self.start_time = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        elapsed = time.time() - self.start_time
        
        if self.show_in_ui:
            if elapsed > 2.0:
                st.warning(f"⚠️ {self.operation_name} took {elapsed:.2f}s (slow)")
            else:
                st.success(f"✅ {self.operation_name} completed in {elapsed:.2f}s")
        
        # Log slow operations
        if elapsed > 5.0:
            print(f"SLOW OPERATION: {self.operation_name} took {elapsed:.2f}s")


# ============================================
# DATA OPTIMIZATION
# ============================================

def optimize_dataframe(df, columns_to_keep: List[str] = None):
    """
    Optimize pandas DataFrame memory usage
    
    - Keep only needed columns
    - Convert to appropriate data types
    - Remove duplicates
    """
    if columns_to_keep:
        df = df[columns_to_keep]
    
    # Convert object columns with few unique values to category
    for col in df.select_dtypes(include=['object']).columns:
        if df[col].nunique() < len(df) * 0.5:  # Less than 50% unique values
            df[col] = df[col].astype('category')
    
    return df


def batch_process(items: List[Any], batch_size: int = 100, process_func: Callable = None):
    """
    Process large lists in batches to avoid memory issues
    
    Usage:
        def process_patient(patient):
            return validate_patient(patient)
        
        results = batch_process(all_patients, batch_size=100, process_func=process_patient)
    """
    results = []
    total = len(items)
    
    for i in range(0, total, batch_size):
        batch = items[i:i+batch_size]
        if process_func:
            batch_results = [process_func(item) for item in batch]
            results.extend(batch_results)
        else:
            results.extend(batch)
    
    return results


# ============================================
# LAZY LOADING
# ============================================

def lazy_load_section(section_name: str, load_function: Callable, expander_label: str = None):
    """
    Lazy load expensive content in expanders
    
    Usage:
        lazy_load_section(
            "patient_history",
            lambda: load_patient_history(nhs_number),
            "📜 Patient History"
        )
    """
    label = expander_label or section_name
    
    with st.expander(label):
        if f"loaded_{section_name}" not in st.session_state:
            with st.spinner("Loading..."):
                content = load_function()
                st.session_state[f"loaded_{section_name}"] = content
        
        st.write(st.session_state[f"loaded_{section_name}"])


# ============================================
# SEARCH OPTIMIZATION
# ============================================

def fuzzy_search(query: str, items: List[Dict], search_fields: List[str], threshold: float = 0.6) -> List[Dict]:
    """
    Perform fuzzy search on list of dictionaries
    Faster than loading all records
    
    Usage:
        results = fuzzy_search(
            "john smith",
            all_patients,
            ["name", "nhs_number"],
            threshold=0.6
        )
    """
    if not query:
        return items
    
    query_lower = query.lower()
    results = []
    
    for item in items:
        # Check each search field
        for field in search_fields:
            if field in item and item[field]:
                field_value = str(item[field]).lower()
                if query_lower in field_value:
                    results.append(item)
                    break
    
    return results


# Export
__all__ = [
    'cache_for_session',
    'clear_cache',
    'Paginator',
    'PerformanceMonitor',
    'optimize_dataframe',
    'batch_process',
    'lazy_load_section',
    'fuzzy_search'
]
