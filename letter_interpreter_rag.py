"""
T21 LETTER INTERPRETER - RAG (Retrieval Augmented Generation) SYSTEM

This enhances the letter interpreter by:
1. Retrieving similar validated examples from the learning library
2. Feeding examples to AI as context
3. Collecting feedback to improve future interpretations
4. Building trust-specific expertise over time

How it works:
User uploads letter → System finds 3 similar validated examples →
AI sees examples as context → Generates better interpretation →
User validates/corrects → System learns for next time
"""

from learning_system_core import learning_system
from data_anonymizer import anonymizer
from typing import List, Dict, Optional
import json
from datetime import datetime


class LetterInterpreterRAG:
    """
    RAG-enhanced letter interpreter
    Uses validated examples to improve interpretation accuracy
    """
    
    def __init__(self):
        self.module_name = "letter_interpreter"
        self.learning_system = learning_system
        self.anonymizer = anonymizer
    
    def get_contextual_examples(self, letter_text: str, letter_type: str = None,
                                specialty: str = None, limit: int = 3) -> List[Dict]:
        """
        Retrieve relevant examples to provide as context to the AI
        
        This is the core RAG functionality - finds similar validated examples
        """
        # Determine letter type if not provided
        if not letter_type:
            letter_type = self._detect_letter_type(letter_text)
        
        # Get similar examples from learning library
        examples = self.learning_system.get_similar_examples(
            module=self.module_name,
            category=letter_type,
            specialty=specialty,
            limit=limit
        )
        
        return examples
    
    def build_enhanced_prompt(self, letter_text: str, base_prompt: str,
                             letter_type: str = None, specialty: str = None) -> str:
        """
        Enhance the AI prompt with relevant examples
        
        This dramatically improves accuracy by showing the AI what
        expert validators have done in similar situations
        """
        # Get relevant examples
        examples = self.get_contextual_examples(letter_text, letter_type, specialty)
        
        if not examples:
            # No examples yet - use base prompt
            return base_prompt
        
        # Build enhanced prompt with examples
        examples_section = "\n\n🎓 **LEARN FROM THESE VALIDATED EXAMPLES:**\n\n"
        examples_section += "These are real examples from expert NHS validators in YOUR trust:\n\n"
        
        for idx, example in enumerate(examples, 1):
            examples_section += f"**Example {idx}:**\n"
            examples_section += f"Input: {example['input'][:200]}...\n"
            examples_section += f"Expert Comment: {example['output']}\n"
            if example.get('specialty'):
                examples_section += f"Specialty: {example['specialty']}\n"
            examples_section += "\n"
        
        examples_section += "Use these examples to guide your interpretation. "
        examples_section += "Match the commenting style and level of detail.\n\n"
        
        # Insert examples section into base prompt
        enhanced_prompt = base_prompt.replace(
            "CLINICAL LETTER:",
            examples_section + "CLINICAL LETTER:"
        )
        
        return enhanced_prompt
    
    def record_interpretation(self, letter_text: str, ai_interpretation: Dict,
                            is_correct: bool = None, user_correction: str = None,
                            metadata: Dict = None):
        """
        Record an interpretation for learning purposes
        
        If the interpretation is correct → Add as validated example
        If incorrect → Record as feedback for improvement
        """
        # Anonymize the letter first
        anonymized_data = self.anonymizer.anonymize_for_learning(
            letter_text,
            letter_metadata=metadata
        )
        
        if is_correct:
            # Add as validated example
            comment = ai_interpretation.get('step5_nhs_comment_format', {}).get('comment_line', '')
            letter_type = ai_interpretation.get('step1_identify_letter_type', {}).get('letter_type', '')
            
            self.learning_system.add_example(
                module=self.module_name,
                category=self._map_letter_type_to_category(letter_type),
                anonymized_input=anonymized_data['anonymized_letter'],
                validated_output=comment,
                scenario_type=metadata.get('scenario_type') if metadata else None,
                specialty=metadata.get('specialty') if metadata else None,
                metadata=anonymized_data['preserved_elements'],
                created_by=metadata.get('user_id') if metadata else None
            )
            
            # Log successful interpretation
            self.learning_system.log_metric(self.module_name, "correct_interpretations", 1)
        
        elif is_correct is False and user_correction:
            # Record as feedback - AI was wrong
            self.learning_system.record_feedback(
                module=self.module_name,
                ai_suggestion=ai_interpretation.get('step5_nhs_comment_format', {}).get('comment_line', ''),
                user_correction=user_correction,
                is_correct=False,
                feedback_type="correction",
                improvement_notes=f"AI suggested wrong interpretation for {ai_interpretation.get('step1_identify_letter_type', {}).get('letter_type', 'unknown')} letter",
                metadata=metadata
            )
            
            # Still add the CORRECTED version as an example
            letter_type = ai_interpretation.get('step1_identify_letter_type', {}).get('letter_type', '')
            
            self.learning_system.add_example(
                module=self.module_name,
                category=self._map_letter_type_to_category(letter_type),
                anonymized_input=anonymized_data['anonymized_letter'],
                validated_output=user_correction,  # Use corrected version
                scenario_type=metadata.get('scenario_type') if metadata else None,
                specialty=metadata.get('specialty') if metadata else None,
                metadata={**anonymized_data['preserved_elements'], 'corrected_from_ai': True},
                created_by=metadata.get('user_id') if metadata else None
            )
            
            # Log correction needed
            self.learning_system.log_metric(self.module_name, "corrections_needed", 1)
    
    def _detect_letter_type(self, letter_text: str) -> str:
        """Simple letter type detection"""
        letter_lower = letter_text.lower()
        
        if any(word in letter_lower for word in ['refer', 'referral']):
            return 'referral'
        elif any(word in letter_lower for word in ['discharg', 'no further']):
            return 'discharge'
        elif any(word in letter_lower for word in ['treatment', 'procedure completed']):
            return 'treatment'
        else:
            return 'clinic_outcome'
    
    def _map_letter_type_to_category(self, letter_type: str) -> str:
        """Map letter type descriptions to categories"""
        type_lower = letter_type.lower()
        
        if 'referral' in type_lower:
            return 'referral'
        elif 'discharge' in type_lower:
            return 'discharge'
        elif 'treatment' in type_lower:
            return 'treatment'
        elif 'outcome' in type_lower:
            return 'clinic_outcome'
        else:
            return 'other'
    
    def get_learning_stats(self) -> Dict:
        """Get statistics about letter interpreter learning"""
        stats = self.learning_system.get_example_library_stats()
        analytics = self.learning_system.get_analytics_summary(module=self.module_name)
        
        return {
            'example_library': stats.get(self.module_name, {}),
            'analytics': analytics.get(self.module_name, {}),
            'timestamp': datetime.now().isoformat()
        }
    
    def get_improvement_suggestions(self) -> List[Dict]:
        """
        Analyze patterns and suggest improvements
        
        Example: "You need more Orthopaedics examples"
                 "Common mistake: Confusing Code 10 vs 11"
        """
        patterns = self.learning_system.detect_patterns(self.module_name)
        stats = self.get_learning_stats()
        
        suggestions = []
        
        # Check for low coverage areas
        library_stats = stats.get('example_library', {})
        categories = library_stats.get('categories', {})
        
        common_categories = ['referral', 'discharge', 'treatment', 'clinic_outcome']
        for category in common_categories:
            if category not in categories or categories[category]['count'] < 5:
                suggestions.append({
                    'type': 'coverage_gap',
                    'priority': 'medium',
                    'message': f"Need more examples for {category} letters",
                    'action': f"Save validated {category} letters to improve AI accuracy"
                })
        
        # Check for high correction rate
        analytics = stats.get('analytics', {})
        if 'corrections_needed' in analytics and 'correct_interpretations' in analytics:
            corrections = analytics['corrections_needed'].get('total', 0)
            correct = analytics['correct_interpretations'].get('total', 0)
            
            if correct > 0:
                error_rate = corrections / (corrections + correct)
                if error_rate > 0.3:  # More than 30% error rate
                    suggestions.append({
                        'type': 'accuracy_issue',
                        'priority': 'high',
                        'message': f"High correction rate detected ({error_rate*100:.1f}%)",
                        'action': "Review recent corrections and add more examples for problematic scenarios"
                    })
        
        # Add pattern-based suggestions
        for pattern in patterns:
            suggestions.append({
                'type': 'pattern_detected',
                'priority': 'medium',
                'message': f"Common pattern: {pattern['description']}",
                'action': "Consider creating a specific training scenario"
            })
        
        return suggestions


# Global instance
letter_rag = LetterInterpreterRAG()


if __name__ == "__main__":
    # Test the RAG system
    print("T21 Letter Interpreter RAG System\n")
    
    # Add some test examples
    test_examples = [
        {
            'input': "GP referral for chest pain investigation in 45-year-old patient",
            'output': "18/10/2025 T21 - REF REC'D 01/10/2025 FOR CHEST PAIN - PT ON PBL - AWAITING 1ST OPA CARDIOLOGY",
            'specialty': "Cardiology",
            'category': "referral"
        },
        {
            'input': "Discharge letter after successful treatment for hypertension",
            'output': "CS (15/09/2025)(34) TSO PT DISCHARGED - HYPERTENSION CONTROLLED - NO FURTHER TX REQUIRED",
            'specialty': "Cardiology",
            'category': "discharge"
        }
    ]
    
    for ex in test_examples:
        learning_system.add_example(
            module="letter_interpreter",
            category=ex['category'],
            anonymized_input=ex['input'],
            validated_output=ex['output'],
            specialty=ex['specialty'],
            created_by="test_system"
        )
    
    print("Added test examples\n")
    
    # Test retrieval
    examples = letter_rag.get_contextual_examples(
        "Referral for cardiac investigation",
        letter_type="referral",
        specialty="Cardiology"
    )
    
    print(f"Retrieved {len(examples)} contextual examples:")
    for idx, ex in enumerate(examples, 1):
        print(f"\nExample {idx}:")
        print(f"  Input: {ex['input'][:60]}...")
        print(f"  Output: {ex['output'][:60]}...")
        print(f"  Specialty: {ex.get('specialty', 'N/A')}")
    
    # Get stats
    stats = letter_rag.get_learning_stats()
    print("\n\nLearning Statistics:")
    print(json.dumps(stats, indent=2))
    
    # Get suggestions
    suggestions = letter_rag.get_improvement_suggestions()
    print("\n\nImprovement Suggestions:")
    for suggestion in suggestions:
        print(f"[{suggestion['priority'].upper()}] {suggestion['message']}")
        print(f"  Action: {suggestion['action']}\n")
