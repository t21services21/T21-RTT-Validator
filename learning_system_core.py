"""
T21 PLATFORM-WIDE LEARNING SYSTEM - CORE INFRASTRUCTURE

This is the foundational learning engine that powers ALL T21 modules:
- Letter Interpretation
- Certification Exams
- RTT Code Training
- Pathway Management
- PBL Optimization
- Validation Workflows

Architecture:
1. Data Collection Layer - Captures anonymized interactions
2. Pattern Detection - Identifies trends and common scenarios
3. RAG Engine - Retrieves relevant examples for context
4. Feedback Loop - Learns from corrections and validations
5. Analytics Dashboard - Shows learning progress and insights
"""

import sqlite3
import json
from datetime import datetime
from typing import Dict, List, Optional, Any
import hashlib
import os


class LearningSystemCore:
    """
    Central learning engine for the entire T21 platform
    Manages data collection, storage, retrieval, and analytics
    """
    
    def __init__(self, db_path: str = "t21_learning_system.db"):
        """Initialize learning system with database"""
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Create database tables for learning system"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Example Library - Stores validated examples from all modules
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS example_library (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                module TEXT NOT NULL,
                category TEXT NOT NULL,
                scenario_type TEXT,
                specialty TEXT,
                content_hash TEXT UNIQUE,
                anonymized_input TEXT,
                validated_output TEXT,
                metadata TEXT,
                quality_score REAL DEFAULT 1.0,
                usage_count INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                created_by TEXT,
                is_active BOOLEAN DEFAULT 1
            )
        """)
        
        # Feedback Collection - User corrections and validations
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                module TEXT NOT NULL,
                session_id TEXT,
                ai_suggestion TEXT,
                user_correction TEXT,
                feedback_type TEXT,
                is_correct BOOLEAN,
                improvement_notes TEXT,
                metadata TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                user_role TEXT
            )
        """)
        
        # Pattern Detection - Identified trends and common scenarios
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                module TEXT NOT NULL,
                pattern_type TEXT,
                pattern_description TEXT,
                frequency INTEGER,
                confidence_score REAL,
                metadata TEXT,
                detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Usage Analytics - Track system usage and effectiveness
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS analytics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                module TEXT NOT NULL,
                metric_name TEXT,
                metric_value REAL,
                metadata TEXT,
                recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Learning Insights - Automatically generated insights
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS insights (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                module TEXT NOT NULL,
                insight_type TEXT,
                insight_text TEXT,
                action_recommended TEXT,
                priority TEXT,
                is_resolved BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create indexes for faster retrieval
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_examples_module ON example_library(module)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_examples_category ON example_library(category)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_examples_specialty ON example_library(specialty)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_feedback_module ON feedback(module)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_patterns_module ON patterns(module)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_analytics_module ON analytics(module)")
        
        conn.commit()
        conn.close()
    
    def add_example(self, module: str, category: str, anonymized_input: str, 
                    validated_output: str, scenario_type: str = None, 
                    specialty: str = None, metadata: Dict = None,
                    created_by: str = None) -> int:
        """
        Add a validated example to the learning library
        
        Args:
            module: Which T21 module (e.g., 'letter_interpreter', 'certification')
            category: Category within module (e.g., 'referral', 'discharge')
            anonymized_input: Input with patient data removed
            validated_output: Correct/validated output
            scenario_type: Specific scenario type
            specialty: Clinical specialty if applicable
            metadata: Additional context
            created_by: User who validated this example
        
        Returns:
            Example ID
        """
        # Create content hash to prevent duplicates
        content_hash = hashlib.md5(
            f"{anonymized_input}{validated_output}".encode()
        ).hexdigest()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO example_library 
                (module, category, scenario_type, specialty, content_hash, 
                 anonymized_input, validated_output, metadata, created_by)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                module, category, scenario_type, specialty, content_hash,
                anonymized_input, validated_output, 
                json.dumps(metadata) if metadata else None,
                created_by
            ))
            
            example_id = cursor.lastrowid
            conn.commit()
            
            # Log analytics
            self.log_metric(module, "examples_added", 1)
            
            return example_id
            
        except sqlite3.IntegrityError:
            # Duplicate example - update usage count instead
            cursor.execute("""
                UPDATE example_library 
                SET usage_count = usage_count + 1
                WHERE content_hash = ?
            """, (content_hash,))
            conn.commit()
            return None
        
        finally:
            conn.close()
    
    def record_feedback(self, module: str, ai_suggestion: str, 
                       user_correction: str = None, is_correct: bool = None,
                       feedback_type: str = "validation", 
                       improvement_notes: str = None,
                       metadata: Dict = None, session_id: str = None,
                       user_role: str = None):
        """
        Record user feedback on AI suggestions
        
        This is crucial for learning - captures when AI is right/wrong
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO feedback 
            (module, session_id, ai_suggestion, user_correction, feedback_type,
             is_correct, improvement_notes, metadata, user_role)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            module, session_id, ai_suggestion, user_correction, feedback_type,
            is_correct, improvement_notes,
            json.dumps(metadata) if metadata else None,
            user_role
        ))
        
        conn.commit()
        conn.close()
        
        # If corrected, potentially add as example
        if user_correction and is_correct is False:
            self.log_metric(module, "ai_corrections_needed", 1)
    
    def get_similar_examples(self, module: str, category: str = None,
                            specialty: str = None, limit: int = 3) -> List[Dict]:
        """
        Retrieve similar examples for RAG (Retrieval Augmented Generation)
        
        This is the core of the learning system - finds relevant examples
        to feed to AI as context
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Build query based on filters
        query = """
            SELECT anonymized_input, validated_output, scenario_type, 
                   specialty, metadata, quality_score, usage_count
            FROM example_library
            WHERE module = ? AND is_active = 1
        """
        params = [module]
        
        if category:
            query += " AND category = ?"
            params.append(category)
        
        if specialty:
            query += " AND (specialty = ? OR specialty IS NULL)"
            params.append(specialty)
        
        # Order by quality and relevance
        query += " ORDER BY quality_score DESC, usage_count DESC LIMIT ?"
        params.append(limit)
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        examples = []
        for row in rows:
            examples.append({
                'input': row[0],
                'output': row[1],
                'scenario_type': row[2],
                'specialty': row[3],
                'metadata': json.loads(row[4]) if row[4] else {},
                'quality_score': row[5],
                'usage_count': row[6]
            })
            
            # Increment usage count
            cursor.execute("""
                UPDATE example_library 
                SET usage_count = usage_count + 1
                WHERE anonymized_input = ? AND validated_output = ?
            """, (row[0], row[1]))
        
        conn.commit()
        conn.close()
        
        return examples
    
    def log_metric(self, module: str, metric_name: str, metric_value: float,
                   metadata: Dict = None):
        """Log a metric for analytics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO analytics (module, metric_name, metric_value, metadata)
            VALUES (?, ?, ?, ?)
        """, (
            module, metric_name, metric_value,
            json.dumps(metadata) if metadata else None
        ))
        
        conn.commit()
        conn.close()
    
    def get_analytics_summary(self, module: str = None, 
                             days: int = 30) -> Dict:
        """Get analytics summary for a module or entire platform"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = """
            SELECT module, metric_name, COUNT(*) as count, 
                   AVG(metric_value) as avg_value, SUM(metric_value) as total_value
            FROM analytics
            WHERE recorded_at >= datetime('now', '-' || ? || ' days')
        """
        params = [days]
        
        if module:
            query += " AND module = ?"
            params.append(module)
        
        query += " GROUP BY module, metric_name ORDER BY module, count DESC"
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        summary = {}
        for row in rows:
            mod = row[0]
            if mod not in summary:
                summary[mod] = {}
            
            summary[mod][row[1]] = {
                'count': row[2],
                'average': row[3],
                'total': row[4]
            }
        
        conn.close()
        return summary
    
    def get_example_library_stats(self) -> Dict:
        """Get statistics about the example library"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                module,
                category,
                COUNT(*) as example_count,
                AVG(quality_score) as avg_quality,
                SUM(usage_count) as total_usage
            FROM example_library
            WHERE is_active = 1
            GROUP BY module, category
            ORDER BY module, example_count DESC
        """)
        
        rows = cursor.fetchall()
        
        stats = {}
        for row in rows:
            module = row[0]
            if module not in stats:
                stats[module] = {'categories': {}, 'total_examples': 0}
            
            stats[module]['categories'][row[1]] = {
                'count': row[2],
                'avg_quality': row[3],
                'total_usage': row[4]
            }
            stats[module]['total_examples'] += row[2]
        
        conn.close()
        return stats
    
    def detect_patterns(self, module: str, days: int = 30) -> List[Dict]:
        """
        Analyze feedback to detect patterns (common mistakes, trends)
        This runs periodically to identify learning opportunities
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Find common corrections
        cursor.execute("""
            SELECT user_correction, COUNT(*) as frequency
            FROM feedback
            WHERE module = ? 
                AND is_correct = 0 
                AND created_at >= datetime('now', '-' || ? || ' days')
            GROUP BY user_correction
            HAVING frequency > 2
            ORDER BY frequency DESC
            LIMIT 10
        """, (module, days))
        
        patterns = []
        for row in cursor.fetchall():
            if row[0]:  # If there's a correction
                patterns.append({
                    'type': 'common_correction',
                    'description': row[0],
                    'frequency': row[1]
                })
        
        conn.close()
        return patterns


# Global instance
learning_system = LearningSystemCore()


if __name__ == "__main__":
    # Test the system
    print("T21 Learning System initialized successfully!")
    print(f"Database: {learning_system.db_path}")
    
    # Add test example
    example_id = learning_system.add_example(
        module="letter_interpreter",
        category="referral",
        anonymized_input="GP referral for chest pain investigation",
        validated_output="18/10/2025 T21 - REF REC'D 01/10/2025 FOR CHEST PAIN - PT ON PBL - AWAITING 1ST OPA CARDIOLOGY",
        scenario_type="referral_on_pbl",
        specialty="Cardiology",
        created_by="test_user"
    )
    
    print(f"Added test example: ID {example_id}")
    
    # Get stats
    stats = learning_system.get_example_library_stats()
    print("\nExample Library Stats:")
    print(json.dumps(stats, indent=2))
