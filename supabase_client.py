"""
SUPABASE CLIENT FACTORY
Provides get_supabase_client() function for all modules
"""

from supabase_database import supabase

def get_supabase_client():
    """Get Supabase client instance - returns None if not configured"""
    try:
        # Test if client is working
        return supabase
    except:
        return None
