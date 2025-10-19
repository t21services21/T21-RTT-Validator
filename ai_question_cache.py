"""
AI QUESTION CACHE SYSTEM
Save AI responses to avoid re-using OpenAI credits for similar questions

HOW IT WORKS:
1. Student asks question
2. Check cache for similar question
3. If found → Return cached answer (FREE!)
4. If not found → Use OpenAI → Save to cache
5. Next student gets cached answer (FREE!)

BENEFITS:
- Reduce OpenAI costs by 50-90%
- Faster responses (cached answers are instant)
- Build knowledge base from actual student questions
- System gets smarter over time
"""

import sqlite3
import json
from datetime import datetime
from difflib import SequenceMatcher
import hashlib


# Database file
CACHE_DB = "ai_question_cache.db"


def init_cache_database():
    """Initialize the question-answer cache database"""
    conn = sqlite3.connect(CACHE_DB)
    cursor = conn.cursor()
    
    # Create cache table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS question_cache (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question_hash TEXT UNIQUE,
        question_text TEXT,
        question_normalized TEXT,
        answer_text TEXT,
        source TEXT,
        times_used INTEGER DEFAULT 1,
        cost_saved REAL DEFAULT 0.0,
        created_date TEXT,
        last_used_date TEXT
    )
    """)
    
    # Create similarity index
    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_question_normalized 
    ON question_cache(question_normalized)
    """)
    
    conn.commit()
    conn.close()


def normalize_question(question):
    """
    Normalize question for better matching
    - Convert to lowercase
    - Remove punctuation
    - Remove extra spaces
    - Sort words for better matching
    """
    import string
    
    # Lowercase
    q = question.lower()
    
    # Remove punctuation
    q = q.translate(str.maketrans('', '', string.punctuation))
    
    # Remove extra spaces
    q = ' '.join(q.split())
    
    return q


def calculate_similarity(str1, str2):
    """Calculate similarity between two strings (0.0 to 1.0)"""
    return SequenceMatcher(None, str1, str2).ratio()


def get_question_hash(question):
    """Generate hash for exact question matching"""
    return hashlib.md5(normalize_question(question).encode()).hexdigest()


def search_cache(question, similarity_threshold=0.85):
    """
    Search cache for similar question
    
    Args:
        question: The question to search for
        similarity_threshold: Minimum similarity (0.85 = 85% similar)
    
    Returns:
        Cached answer if found, None otherwise
    """
    try:
        conn = sqlite3.connect(CACHE_DB)
        cursor = conn.cursor()
        
        # First try exact match by hash
        question_hash = get_question_hash(question)
        cursor.execute("""
        SELECT question_text, answer_text, times_used, source
        FROM question_cache
        WHERE question_hash = ?
        """, (question_hash,))
        
        result = cursor.fetchone()
        if result:
            # Exact match found!
            update_cache_usage(question_hash, conn)
            conn.close()
            return {
                'question': result[0],
                'answer': result[1],
                'times_used': result[2],
                'source': result[3],
                'match_type': 'exact'
            }
        
        # No exact match, try similarity search
        question_normalized = normalize_question(question)
        
        cursor.execute("""
        SELECT question_hash, question_text, question_normalized, 
               answer_text, times_used, source
        FROM question_cache
        """)
        
        all_cached = cursor.fetchall()
        
        best_match = None
        best_similarity = 0.0
        
        for cached in all_cached:
            cached_hash, cached_q, cached_norm, cached_a, times_used, source = cached
            similarity = calculate_similarity(question_normalized, cached_norm)
            
            if similarity > best_similarity and similarity >= similarity_threshold:
                best_similarity = similarity
                best_match = {
                    'hash': cached_hash,
                    'question': cached_q,
                    'answer': cached_a,
                    'times_used': times_used,
                    'source': source,
                    'match_type': 'similar',
                    'similarity': similarity
                }
        
        if best_match:
            update_cache_usage(best_match['hash'], conn)
        
        conn.close()
        return best_match
        
    except Exception as e:
        print(f"Cache search error: {e}")
        return None


def update_cache_usage(question_hash, conn=None):
    """Update usage count and last used date"""
    close_conn = False
    if conn is None:
        conn = sqlite3.connect(CACHE_DB)
        close_conn = True
    
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE question_cache
    SET times_used = times_used + 1,
        last_used_date = ?,
        cost_saved = cost_saved + 0.03
    WHERE question_hash = ?
    """, (datetime.now().isoformat(), question_hash))
    
    conn.commit()
    
    if close_conn:
        conn.close()


def save_to_cache(question, answer, source="openai"):
    """
    Save question-answer pair to cache
    
    Args:
        question: The question asked
        answer: The answer provided
        source: Where answer came from (openai, builtin, etc.)
    """
    try:
        conn = sqlite3.connect(CACHE_DB)
        cursor = conn.cursor()
        
        question_hash = get_question_hash(question)
        question_normalized = normalize_question(question)
        
        # Check if already exists
        cursor.execute("""
        SELECT id FROM question_cache WHERE question_hash = ?
        """, (question_hash,))
        
        if cursor.fetchone():
            # Already exists, update it
            cursor.execute("""
            UPDATE question_cache
            SET answer_text = ?,
                last_used_date = ?
            WHERE question_hash = ?
            """, (answer, datetime.now().isoformat(), question_hash))
        else:
            # New entry
            cursor.execute("""
            INSERT INTO question_cache 
            (question_hash, question_text, question_normalized, answer_text, 
             source, created_date, last_used_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                question_hash,
                question,
                question_normalized,
                answer,
                source,
                datetime.now().isoformat(),
                datetime.now().isoformat()
            ))
        
        conn.commit()
        conn.close()
        return True
        
    except Exception as e:
        print(f"Cache save error: {e}")
        return False


def get_cache_stats():
    """Get statistics about the cache"""
    try:
        conn = sqlite3.connect(CACHE_DB)
        cursor = conn.cursor()
        
        # Total questions cached
        cursor.execute("SELECT COUNT(*) FROM question_cache")
        total_cached = cursor.fetchone()[0]
        
        # Total times cache was used
        cursor.execute("SELECT SUM(times_used) FROM question_cache")
        total_uses = cursor.fetchone()[0] or 0
        
        # Total cost saved
        cursor.execute("SELECT SUM(cost_saved) FROM question_cache")
        total_saved = cursor.fetchone()[0] or 0.0
        
        # Most popular questions
        cursor.execute("""
        SELECT question_text, times_used
        FROM question_cache
        ORDER BY times_used DESC
        LIMIT 10
        """)
        popular = cursor.fetchall()
        
        conn.close()
        
        return {
            'total_cached': total_cached,
            'total_uses': total_uses,
            'total_saved': f"${total_saved:.2f}",
            'cache_hit_rate': f"{(total_uses / max(total_cached, 1)) * 100:.1f}%",
            'popular_questions': popular
        }
        
    except Exception as e:
        print(f"Stats error: {e}")
        return None


def clear_old_cache(days=90):
    """Clear cache entries older than X days"""
    try:
        conn = sqlite3.connect(CACHE_DB)
        cursor = conn.cursor()
        
        from datetime import timedelta
        cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
        
        cursor.execute("""
        DELETE FROM question_cache
        WHERE last_used_date < ? AND times_used = 1
        """, (cutoff_date,))
        
        deleted = cursor.rowcount
        conn.commit()
        conn.close()
        
        return deleted
        
    except Exception as e:
        print(f"Clear cache error: {e}")
        return 0


# Initialize database on import
init_cache_database()
