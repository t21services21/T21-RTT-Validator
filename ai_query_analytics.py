"""
AI QUERY TRACKING & ANALYTICS SYSTEM
Track all AI queries, responses, and user feedback to improve the system

🚀 COMPETITIVE ADVANTAGE: Learn from real usage like Sigma does
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import hashlib


# Query logs directory
QUERY_LOGS_DIR = "ai_query_logs"
os.makedirs(QUERY_LOGS_DIR, exist_ok=True)


def log_ai_query(
    user_email: str,
    query: str,
    response: str,
    response_time_seconds: float,
    trust_id: str = "",
    module: str = "AI RTT Tutor",
    confidence_score: float = 0.0
) -> str:
    """
    Log an AI query and response
    
    Returns: query_id
    """
    
    try:
        timestamp = datetime.now()
        query_id = hashlib.md5(f"{user_email}{timestamp.isoformat()}{query}".encode()).hexdigest()[:16]
        
        log_entry = {
            'query_id': query_id,
            'timestamp': timestamp.isoformat(),
            'user_email': user_email,
            'trust_id': trust_id,
            'module': module,
            'query': query,
            'response': response,
            'response_time_seconds': response_time_seconds,
            'confidence_score': confidence_score,
            'feedback': None,  # To be filled later
            'helpful': None,  # To be filled later
            'word_count_query': len(query.split()),
            'word_count_response': len(response.split()),
            'tags': extract_tags_from_query(query)
        }
        
        # Save to daily log file
        log_file = os.path.join(QUERY_LOGS_DIR, f"queries_{timestamp.strftime('%Y%m%d')}.json")
        
        if os.path.exists(log_file):
            with open(log_file, 'r', encoding='utf-8') as f:
                logs = json.load(f)
        else:
            logs = []
        
        logs.append(log_entry)
        
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(logs, f, indent=2)
        
        return query_id
        
    except Exception as e:
        print(f"Error logging query: {e}")
        return ""


def extract_tags_from_query(query: str) -> List[str]:
    """Extract relevant tags from query text"""
    
    query_lower = query.lower()
    tags = []
    
    # RTT code references
    rtt_codes = ['code 02', 'code 03', 'code 10', 'code 11', 'code 12', 'code 13', 
                 'code 20', 'code 21', 'code 31', 'code 32', 'code 91', 'code 92', 'code 93']
    for code in rtt_codes:
        if code in query_lower:
            tags.append(code.replace(' ', '_'))
    
    # Topics
    topics = {
        'clock_start': ['clock start', 'start clock', 'start date'],
        'clock_stop': ['clock stop', 'stop clock', 'end clock'],
        'clock_pause': ['clock pause', 'pause clock', 'suspend'],
        'breach': ['breach', 'breaching', '18 week'],
        'cancer': ['cancer', '2ww', '62 day', '31 day'],
        'booking': ['booking', 'appointment', 'schedule'],
        'dna': ['dna', 'did not attend', 'missed appointment'],
        'referral': ['referral', 'refer', 'gp referral'],
        'pathway': ['pathway', 'patient pathway'],
        'validation': ['validation', 'validate', 'data quality']
    }
    
    for tag, keywords in topics.items():
        if any(keyword in query_lower for keyword in keywords):
            tags.append(tag)
    
    return tags


def add_query_feedback(
    query_id: str,
    helpful: bool,
    feedback_text: str = ""
) -> Dict:
    """
    Add user feedback to a query
    
    Args:
        query_id: Query ID from log_ai_query
        helpful: True if response was helpful
        feedback_text: Optional text feedback
    """
    
    try:
        # Find query in logs
        for filename in os.listdir(QUERY_LOGS_DIR):
            if filename.startswith('queries_') and filename.endswith('.json'):
                filepath = os.path.join(QUERY_LOGS_DIR, filename)
                
                with open(filepath, 'r', encoding='utf-8') as f:
                    logs = json.load(f)
                
                # Find and update query
                for log in logs:
                    if log.get('query_id') == query_id:
                        log['helpful'] = helpful
                        log['feedback'] = feedback_text
                        log['feedback_timestamp'] = datetime.now().isoformat()
                        
                        # Save back
                        with open(filepath, 'w', encoding='utf-8') as f:
                            json.dump(logs, f, indent=2)
                        
                        return {'success': True, 'message': 'Feedback saved'}
        
        return {'success': False, 'error': 'Query not found'}
        
    except Exception as e:
        return {'success': False, 'error': str(e)}


def get_query_analytics(
    days: int = 7,
    trust_id: Optional[str] = None,
    user_email: Optional[str] = None
) -> Dict:
    """
    Get analytics for AI queries
    
    Returns comprehensive statistics
    """
    
    cutoff_date = datetime.now() - timedelta(days=days)
    
    all_queries = []
    
    # Load queries from files
    for filename in os.listdir(QUERY_LOGS_DIR):
        if filename.startswith('queries_') and filename.endswith('.json'):
            # Check if file is within date range
            date_str = filename.replace('queries_', '').replace('.json', '')
            try:
                file_date = datetime.strptime(date_str, '%Y%m%d')
                if file_date < cutoff_date:
                    continue
            except:
                continue
            
            filepath = os.path.join(QUERY_LOGS_DIR, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    logs = json.load(f)
                    all_queries.extend(logs)
            except:
                continue
    
    # Filter by trust and user if specified
    if trust_id:
        all_queries = [q for q in all_queries if q.get('trust_id') == trust_id]
    if user_email:
        all_queries = [q for q in all_queries if q.get('user_email') == user_email]
    
    # Calculate statistics
    total_queries = len(all_queries)
    
    if total_queries == 0:
        return {
            'total_queries': 0,
            'avg_response_time': 0,
            'satisfaction_rate': 0,
            'top_tags': [],
            'queries_by_day': [],
            'top_users': []
        }
    
    # Average response time
    response_times = [q.get('response_time_seconds', 0) for q in all_queries]
    avg_response_time = sum(response_times) / len(response_times) if response_times else 0
    
    # Satisfaction rate (helpful feedback)
    helpful_count = sum(1 for q in all_queries if q.get('helpful') == True)
    feedback_count = sum(1 for q in all_queries if q.get('helpful') is not None)
    satisfaction_rate = (helpful_count / feedback_count * 100) if feedback_count > 0 else 0
    
    # Top tags
    tag_counts = {}
    for q in all_queries:
        for tag in q.get('tags', []):
            tag_counts[tag] = tag_counts.get(tag, 0) + 1
    top_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    
    # Queries by day
    queries_by_day = {}
    for q in all_queries:
        try:
            day = q['timestamp'][:10]
            queries_by_day[day] = queries_by_day.get(day, 0) + 1
        except:
            continue
    
    # Top users
    user_counts = {}
    for q in all_queries:
        email = q.get('user_email', 'unknown')
        user_counts[email] = user_counts.get(email, 0) + 1
    top_users = sorted(user_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    
    # Common queries (most frequent)
    query_texts = {}
    for q in all_queries:
        query_lower = q.get('query', '').lower()[:100]  # First 100 chars
        if len(query_lower) > 10:  # Ignore very short queries
            query_texts[query_lower] = query_texts.get(query_lower, 0) + 1
    common_queries = sorted(query_texts.items(), key=lambda x: x[1], reverse=True)[:10]
    
    return {
        'total_queries': total_queries,
        'avg_response_time': round(avg_response_time, 2),
        'satisfaction_rate': round(satisfaction_rate, 1),
        'helpful_count': helpful_count,
        'feedback_count': feedback_count,
        'top_tags': top_tags,
        'queries_by_day': sorted(queries_by_day.items()),
        'top_users': top_users,
        'common_queries': common_queries,
        'avg_query_length': sum(q.get('word_count_query', 0) for q in all_queries) / total_queries,
        'avg_response_length': sum(q.get('word_count_response', 0) for q in all_queries) / total_queries
    }


def get_unanswered_queries(days: int = 7) -> List[Dict]:
    """
    Get queries with low satisfaction (marked as not helpful)
    These need attention for improvement
    """
    
    cutoff_date = datetime.now() - timedelta(days=days)
    
    unanswered = []
    
    for filename in os.listdir(QUERY_LOGS_DIR):
        if filename.startswith('queries_') and filename.endswith('.json'):
            filepath = os.path.join(QUERY_LOGS_DIR, filename)
            
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    logs = json.load(f)
                
                for q in logs:
                    # Check if marked as not helpful
                    if q.get('helpful') == False:
                        unanswered.append({
                            'query_id': q.get('query_id'),
                            'timestamp': q.get('timestamp'),
                            'query': q.get('query'),
                            'response': q.get('response'),
                            'feedback': q.get('feedback', ''),
                            'user_email': q.get('user_email')
                        })
            except:
                continue
    
    return sorted(unanswered, key=lambda x: x['timestamp'], reverse=True)


def export_queries_to_json(output_file: str = "query_export.json", days: int = 30) -> str:
    """Export queries to JSON file for analysis"""
    
    cutoff_date = datetime.now() - timedelta(days=days)
    all_queries = []
    
    for filename in os.listdir(QUERY_LOGS_DIR):
        if filename.startswith('queries_') and filename.endswith('.json'):
            filepath = os.path.join(QUERY_LOGS_DIR, filename)
            
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    logs = json.load(f)
                    all_queries.extend(logs)
            except:
                continue
    
    # Save to export file
    export_path = os.path.join(QUERY_LOGS_DIR, output_file)
    with open(export_path, 'w', encoding='utf-8') as f:
        json.dump(all_queries, f, indent=2)
    
    return export_path
