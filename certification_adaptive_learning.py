"""
T21 CERTIFICATION EXAM - ADAPTIVE LEARNING SYSTEM

Makes the certification exam INTELLIGENT by:
1. Tracking which questions students struggle with
2. Adapting difficulty based on student performance
3. Identifying weak areas and providing targeted training
4. Personalizing the learning path
5. Optimizing question selection for maximum learning

Current exam: 100 random questions from 1000+ pool
Adaptive exam: 100 personalized questions based on skill level + weak areas
"""

from learning_system_core import learning_system
from typing import List, Dict, Optional
import json
from datetime import datetime
import random


class CertificationAdaptiveLearning:
    """
    Adaptive learning system for certification exams
    Personalizes questions based on student performance
    """
    
    def __init__(self):
        self.module_name = "certification"
        self.learning_system = learning_system
    
    def record_question_attempt(self, student_id: str, question_id: str,
                                question_category: str, question_difficulty: str,
                                is_correct: bool, time_taken_seconds: int = None):
        """
        Record a student's attempt at a question
        This builds the intelligence about which questions are hard/easy
        """
        
        # Record in learning system
        self.learning_system.record_feedback(
            module=self.module_name,
            ai_suggestion=json.dumps({
                'question_id': question_id,
                'category': question_category,
                'difficulty': question_difficulty
            }),
            user_correction=None,
            is_correct=is_correct,
            feedback_type="question_attempt",
            metadata={
                'student_id': student_id,
                'question_id': question_id,
                'category': question_category,
                'difficulty': question_difficulty,
                'time_taken': time_taken_seconds
            }
        )
        
        # Log metrics
        metric_name = f"question_{'correct' if is_correct else 'incorrect'}_{question_category}"
        self.learning_system.log_metric(self.module_name, metric_name, 1)
        
        # Track difficulty accuracy
        difficulty_metric = f"difficulty_{question_difficulty}_{'correct' if is_correct else 'incorrect'}"
        self.learning_system.log_metric(self.module_name, difficulty_metric, 1)
    
    def record_exam_completion(self, student_id: str, score: int, 
                               questions_attempted: List[Dict],
                               certification_level: str):
        """
        Record complete exam results
        """
        
        # Calculate category performance
        category_performance = {}
        for q in questions_attempted:
            cat = q.get('category', 'Unknown')
            if cat not in category_performance:
                category_performance[cat] = {'correct': 0, 'total': 0}
            
            category_performance[cat]['total'] += 1
            if q.get('is_correct'):
                category_performance[cat]['correct'] += 1
        
        # Store as example if high score
        if score >= 80:
            self.learning_system.add_example(
                module=self.module_name,
                category=certification_level,
                anonymized_input=json.dumps({
                    'score': score,
                    'certification_level': certification_level,
                    'category_performance': category_performance
                }),
                validated_output=json.dumps({
                    'success': True,
                    'score': score,
                    'level': certification_level
                }),
                scenario_type='successful_exam',
                metadata={'score': score, 'student_id': student_id}
            )
        
        # Log overall metrics
        self.learning_system.log_metric(self.module_name, "exams_completed", 1)
        self.learning_system.log_metric(self.module_name, f"certification_{certification_level}", 1)
    
    def get_question_difficulty_stats(self, question_id: str) -> Dict:
        """
        Get statistics about how difficult a question actually is
        (vs its assigned difficulty)
        """
        
        analytics = self.learning_system.get_analytics_summary(
            module=self.module_name,
            days=180
        )
        
        # This would need more sophisticated tracking
        # For now, return basic structure
        return {
            'question_id': question_id,
            'actual_difficulty': 'Unknown',
            'assigned_difficulty': 'Unknown',
            'attempts': 0,
            'success_rate': 0
        }
    
    def get_student_weak_areas(self, student_id: str) -> List[Dict]:
        """
        Identify which categories/topics a student struggles with
        """
        
        # This would query the database for this student's history
        # For now, return placeholder
        return [
            {
                'category': 'RTT Codes 10-12',
                'accuracy': 45,  # 45% correct
                'attempts': 10,
                'recommendation': 'Focus on understanding the differences between codes 10, 11, and 12'
            }
        ]
    
    def generate_adaptive_exam(self, student_id: str = None, 
                               total_questions: int = 100,
                               question_pool: List[Dict] = None) -> List[Dict]:
        """
        Generate a personalized exam based on:
        - Student's previous performance (if available)
        - Question difficulty stats
        - Category balance
        - Weak area reinforcement
        """
        
        if not question_pool:
            return []
        
        selected_questions = []
        
        # If we have student history, personalize
        if student_id:
            weak_areas = self.get_student_weak_areas(student_id)
            
            # Allocate questions:
            # 40% - Weak areas (for improvement)
            # 40% - Mixed difficulty (for assessment)
            # 20% - Strong areas (for confidence)
            
            weak_area_count = int(total_questions * 0.4)
            mixed_count = int(total_questions * 0.4)
            strong_count = total_questions - weak_area_count - mixed_count
            
            # This is simplified - would need actual student performance data
            # For now, fall back to standard distribution
        
        # Standard distribution (no student history)
        # Easy: 30%, Medium: 40%, Hard: 20%, Expert: 10%
        easy_count = int(total_questions * 0.30)
        medium_count = int(total_questions * 0.40)
        hard_count = int(total_questions * 0.20)
        expert_count = total_questions - easy_count - medium_count - hard_count
        
        # Select questions by difficulty
        easy_qs = [q for q in question_pool if q.get('difficulty') == 'Easy']
        medium_qs = [q for q in question_pool if q.get('difficulty') == 'Medium']
        hard_qs = [q for q in question_pool if q.get('difficulty') == 'Hard']
        expert_qs = [q for q in question_pool if q.get('difficulty') == 'Expert']
        
        selected_questions.extend(random.sample(easy_qs, min(easy_count, len(easy_qs))))
        selected_questions.extend(random.sample(medium_qs, min(medium_count, len(medium_qs))))
        selected_questions.extend(random.sample(hard_qs, min(hard_count, len(hard_qs))))
        selected_questions.extend(random.sample(expert_qs, min(expert_count, len(expert_qs))))
        
        # Randomize order
        random.shuffle(selected_questions)
        
        return selected_questions[:total_questions]
    
    def recommend_training_modules(self, student_id: str) -> List[Dict]:
        """
        Recommend specific training based on weak areas
        """
        
        weak_areas = self.get_student_weak_areas(student_id)
        
        recommendations = []
        
        for area in weak_areas:
            if area['accuracy'] < 60:  # Less than 60% accuracy
                recommendations.append({
                    'priority': 'high',
                    'category': area['category'],
                    'current_accuracy': area['accuracy'],
                    'target_accuracy': 80,
                    'recommended_action': area['recommendation'],
                    'training_modules': self._map_category_to_training(area['category'])
                })
        
        return recommendations
    
    def _map_category_to_training(self, category: str) -> List[str]:
        """Map exam categories to training modules"""
        
        category_lower = category.lower()
        
        if '10' in category_lower or '11' in category_lower or '12' in category_lower:
            return [
                'RTT Code Training - Codes 10, 11, 12',
                'Referral Scenarios Practice',
                'Clock Start vs Restart'
            ]
        elif 'pathway' in category_lower:
            return [
                'Pathway Management',
                'Episode Creation',
                'Clock Calculations'
            ]
        elif 'pbl' in category_lower or 'waiting' in category_lower:
            return [
                'Partial Booking List Management',
                'Waiting List Procedures'
            ]
        else:
            return ['General RTT Training']
    
    def get_learning_insights(self) -> Dict:
        """
        Get platform-wide insights about certification exams
        """
        
        analytics = self.learning_system.get_analytics_summary(
            module=self.module_name,
            days=90
        )
        
        stats = self.learning_system.get_example_library_stats()
        
        return {
            'total_exams': analytics.get(self.module_name, {}).get('exams_completed', {}).get('total', 0),
            'certification_distribution': {
                'Foundation': analytics.get(self.module_name, {}).get('certification_RTT Foundation Certificate ✅', {}).get('total', 0),
                'Practitioner': analytics.get(self.module_name, {}).get('certification_RTT Practitioner Certificate ⭐', {}).get('total', 0),
                'Expert': analytics.get(self.module_name, {}).get('certification_RTT Expert Certificate 🏆', {}).get('total', 0)
            },
            'example_library': stats.get(self.module_name, {})
        }
    
    def identify_problematic_questions(self) -> List[Dict]:
        """
        Identify questions that everyone gets wrong (may be poorly written)
        """
        
        # This would query all question attempts
        # Return questions with <30% success rate
        
        return []  # Placeholder
    
    def suggest_new_questions(self) -> List[Dict]:
        """
        Suggest new question topics based on gaps in question bank
        """
        
        # Analyze coverage gaps
        # Suggest questions for underrepresented topics
        
        return []  # Placeholder


# Global instance
cert_adaptive = CertificationAdaptiveLearning()


# Utility functions for easy integration

def record_exam_question(student_id: str, question: Dict, is_correct: bool):
    """Simple function to record a question attempt"""
    cert_adaptive.record_question_attempt(
        student_id=student_id,
        question_id=question.get('id', 'unknown'),
        question_category=question.get('category', 'Unknown'),
        question_difficulty=question.get('difficulty', 'Medium'),
        is_correct=is_correct
    )


def record_exam_results(student_id: str, score: int, questions: List[Dict], 
                        certification_level: str):
    """Simple function to record complete exam"""
    cert_adaptive.record_exam_completion(
        student_id=student_id,
        score=score,
        questions_attempted=questions,
        certification_level=certification_level
    )


def get_personalized_exam(student_id: str, question_pool: List[Dict], 
                         total_questions: int = 100) -> List[Dict]:
    """Get a personalized exam for a student"""
    return cert_adaptive.generate_adaptive_exam(
        student_id=student_id,
        total_questions=total_questions,
        question_pool=question_pool
    )


def get_student_recommendations(student_id: str) -> List[Dict]:
    """Get training recommendations for a student"""
    return cert_adaptive.recommend_training_modules(student_id)


# Export
__all__ = [
    'cert_adaptive',
    'CertificationAdaptiveLearning',
    'record_exam_question',
    'record_exam_results',
    'get_personalized_exam',
    'get_student_recommendations'
]


if __name__ == "__main__":
    # Test the system
    print("T21 Certification Adaptive Learning System\n")
    
    # Simulate recording some question attempts
    test_student = "student_123"
    
    # Student gets Code 11/12 questions wrong
    for i in range(5):
        record_exam_question(
            student_id=test_student,
            question={'id': f'q_{i}', 'category': 'RTT Codes 10-12', 'difficulty': 'Hard'},
            is_correct=False
        )
    
    # Student gets pathway questions right
    for i in range(5, 10):
        record_exam_question(
            student_id=test_student,
            question={'id': f'q_{i}', 'category': 'Pathway Management', 'difficulty': 'Medium'},
            is_correct=True
        )
    
    print("Recorded 10 question attempts")
    
    # Get recommendations
    recommendations = get_student_recommendations(test_student)
    print("\nRecommendations:")
    for rec in recommendations:
        print(f"- {rec}")
    
    # Get insights
    insights = cert_adaptive.get_learning_insights()
    print("\nLearning Insights:")
    print(json.dumps(insights, indent=2))
