"""
BROWSER HISTORY HANDLER
Implements proper browser back/forward functionality with clean URLs
Uses HTML5 History API
"""

import streamlit as st
import streamlit.components.v1 as components

def push_history_state(page_name, url_path):
    """
    Push a new state to browser history with clean URL
    
    Args:
        page_name: Display name for the page
        url_path: URL path (e.g., '/clinical_exceptions')
    """
    # Use HTML5 History API to add history entry
    components.html(f"""
    <script>
        // Push new state to browser history
        if (window.parent) {{
            window.parent.history.pushState(
                {{page: '{page_name}'}}, 
                '{page_name}', 
                '{url_path}'
            );
        }}
    </script>
    """, height=0)

def setup_history_listener():
    """
    Set up listener for browser back/forward buttons
    """
    # Listen for popstate events (back/forward buttons)
    components.html("""
    <script>
        // Handle browser back/forward
        window.addEventListener('popstate', function(event) {
            if (event.state && event.state.page) {
                // Reload page when back/forward is pressed
                window.parent.location.reload();
            }
        });
        
        // Set initial state
        if (!window.parent.history.state) {
            window.parent.history.replaceState(
                {page: 'dashboard'}, 
                'Dashboard', 
                window.parent.location.pathname
            );
        }
    </script>
    """, height=0)

def navigate_with_history(page_name, page_path, streamlit_page):
    """
    Navigate to a page with proper browser history
    
    Args:
        page_name: Display name (e.g., 'Clinical Exceptions')
        page_path: URL path (e.g., '/clinical_exceptions')
        streamlit_page: Streamlit page to switch to
    """
    # Store the target page in session state
    st.session_state['_target_page'] = streamlit_page
    
    # Push to history and trigger navigation
    components.html(f"""
    <script>
        // Push new state to browser history
        if (window.parent) {{
            window.parent.history.pushState(
                {{page: '{page_name}'}}, 
                '{page_name}', 
                '{page_path}'
            );
            
            // Force navigation by reloading
            window.parent.location.href = window.parent.location.origin + '{page_path}';
        }}
    </script>
    """, height=0)
    
    # Don't call st.switch_page() - let the URL change handle it
    st.stop()
