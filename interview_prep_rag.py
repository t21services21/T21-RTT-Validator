"""
T21 INTERVIEW PREP - RAG (Retrieval Augmented Generation) SYSTEM

Makes interview prep SMARTER by learning from:
1. Which questions actually appear in interviews
2. Which candidates get jobs
3. Job description patterns
4. Successful answer strategies

How it works:
- User reports interview outcome
- System learns which questions appeared
- Adjusts likelihood % for future users
- Builds job-specific question banks
- Shares successful strategies
"""

from learning_system_core import learning_system
from typing import List, Dict, Optional
import json
from datetime import datetime


class InterviewPrepRAG:
    """
    RAG-enhanced interview preparation
    Learns from real interview outcomes
    """
    
    def __init__(self):
        self.module_name = "interview_prep"
        self.learning_system = learning_system
    
    def record_interview_outcome(self, job_title: str, job_description: str,
                                 questions_generated: List[Dict],
                                 questions_appeared: List[str] = None,
                                 outcome: str = None,
                                 company_name: str = None,
                                 industry: str = None):
        """
        Record what happened in a real interview
        
        This is GOLD for learning:
        - Which questions actually came up
        - Did the candidate get the job
        - What industry/company patterns exist
        """
        
        # Anonymize job description (remove company-specific info)
        anonymized_job = self._anonymize_job_description(job_description, company_name)
        
        # Determine success
        is_successful = outcome == "Got the job! 🎉" if outcome else None
        
        # Record as feedback
        self.learning_system.record_feedback(
            module=self.module_name,
            ai_suggestion=json.dumps({
                'questions_count': len(questions_generated),
                'categories': list(set([q.get('category') for q in questions_generated]))
            }),
            user_correction=json.dumps({
                'questions_appeared': questions_appeared or [],
                'outcome': outcome
            }),
            is_correct=is_successful,
            feedback_type="interview_outcome",
            metadata={
                'job_title': job_title,
                'company_name': company_name,
                'industry': industry,
                'questions_appeared_count': len(questions_appeared) if questions_appeared else 0,
                'total_questions': len(questions_generated)
            }
        )
        
        # Update question likelihoods
        if questions_appeared:
            for q in questions_generated:
                if q['question'] in questions_appeared:
                    # This question appeared!
                    self.learning_system.log_metric(
                        self.module_name,
                        f"question_appeared_{q['category']}",
                        1,
                        metadata={'question': q['question'], 'job_title': job_title}
                    )
                else:
                    # This question didn't appear
                    self.learning_system.log_metric(
                        self.module_name,
                        f"question_missed_{q['category']}",
                        1,
                        metadata={'question': q['question'], 'job_title': job_title}
                    )
        
        # If successful, save as high-quality example
        if is_successful and questions_appeared:
            self.learning_system.add_example(
                module=self.module_name,
                category=self._categorize_job(job_title),
                anonymized_input=anonymized_job,
                validated_output=json.dumps({
                    'questions_that_worked': questions_appeared,
                    'job_title': job_title,
                    'outcome': 'success'
                }),
                scenario_type='successful_interview',
                specialty=industry,
                metadata={'success': True, 'questions_count': len(questions_appeared)}
            )
        
        # Log overall metrics
        self.learning_system.log_metric(self.module_name, "interviews_reported", 1)
        if is_successful:
            self.learning_system.log_metric(self.module_name, "successful_interviews", 1)
    
    def get_enhanced_question_set(self, job_title: str, job_description: str,
                                  industry: str = None) -> Dict:
        """
        Get question set enhanced by learning from past interviews
        
        Returns questions with ADJUSTED likelihoods based on real data
        """
        
        category = self._categorize_job(job_title)
        
        # Get similar successful examples
        similar_examples = self.learning_system.get_similar_examples(
            module=self.module_name,
            category=category,
            specialty=industry,
            limit=5
        )
        
        # Extract patterns from successful interviews
        common_questions = {}
        total_interviews = len(similar_examples)
        
        for example in similar_examples:
            output = json.loads(example['output'])
            for question in output.get('questions_that_worked', []):
                common_questions[question] = common_questions.get(question, 0) + 1
        
        # Build enhancement data
        enhancement = {
            'has_learning_data': len(similar_examples) > 0,
            'similar_interviews_count': total_interviews,
            'common_questions': {},
            'recommended_focus': []
        }
        
        if total_interviews > 0:
            # Calculate frequency %
            for question, count in common_questions.items():
                frequency = (count / total_interviews) * 100
                if frequency >= 50:  # Appeared in 50%+ of interviews
                    enhancement['common_questions'][question] = f"{frequency:.0f}%"
                    enhancement['recommended_focus'].append({
                        'question': question,
                        'frequency': frequency
                    })
        
        return enhancement
    
    def get_likelihood_adjustment(self, question: str, category: str,
                                  job_title: str) -> Dict:
        """
        Calculate adjusted likelihood based on historical data
        
        Returns: {
            'original_likelihood': '85%',
            'adjusted_likelihood': '95%',
            'reason': 'Appeared in 8/10 similar interviews'
        }
        """
        
        # Get analytics for this category
        analytics = self.learning_system.get_analytics_summary(
            module=self.module_name,
            days=180  # Last 6 months
        )
        
        module_data = analytics.get(self.module_name, {})
        
        # Calculate appearance rate
        appeared_metric = f"question_appeared_{category}"
        missed_metric = f"question_missed_{category}"
        
        appeared_count = module_data.get(appeared_metric, {}).get('total', 0)
        missed_count = module_data.get(missed_metric, {}).get('total', 0)
        
        total_count = appeared_count + missed_count
        
        if total_count == 0:
            return {
                'has_data': False,
                'message': 'No historical data yet - using AI prediction'
            }
        
        # Calculate actual likelihood
        actual_likelihood = (appeared_count / total_count) * 100
        
        # Determine adjustment
        if actual_likelihood >= 80:
            adjustment = "VERY HIGH"
            reason = f"Appeared in {appeared_count}/{total_count} similar interviews"
        elif actual_likelihood >= 60:
            adjustment = "HIGH"
            reason = f"Common question - appeared in {appeared_count}/{total_count} interviews"
        elif actual_likelihood >= 40:
            adjustment = "MEDIUM"
            reason = f"Sometimes appears - {appeared_count}/{total_count} interviews"
        else:
            adjustment = "LOW"
            reason = f"Rarely appears - only {appeared_count}/{total_count} interviews"
        
        return {
            'has_data': True,
            'adjusted_likelihood': f"{actual_likelihood:.0f}%",
            'adjustment_level': adjustment,
            'reason': reason,
            'sample_size': total_count
        }
    
    def get_success_insights(self, job_title: str) -> List[Dict]:
        """
        Get insights from successful interviews for similar jobs
        """
        
        category = self._categorize_job(job_title)
        
        # Get successful examples
        examples = self.learning_system.get_similar_examples(
            module=self.module_name,
            category=category,
            limit=10
        )
        
        insights = []
        
        if examples:
            successful = [e for e in examples if e.get('metadata', {}).get('success')]
            
            if successful:
                insights.append({
                    'type': 'success_rate',
                    'message': f"We have data from {len(successful)} successful interviews for {job_title}",
                    'priority': 'high'
                })
                
                # Aggregate common questions
                all_questions = {}
                for ex in successful:
                    output = json.loads(ex['output'])
                    for q in output.get('questions_that_worked', []):
                        all_questions[q] = all_questions.get(q, 0) + 1
                
                # Most common questions
                sorted_questions = sorted(all_questions.items(), key=lambda x: x[1], reverse=True)
                if sorted_questions:
                    top_3 = sorted_questions[:3]
                    insights.append({
                        'type': 'top_questions',
                        'message': f"Top 3 questions for {job_title}:",
                        'questions': [q[0] for q in top_3],
                        'priority': 'high'
                    })
        
        return insights
    
    def get_learning_stats(self) -> Dict:
        """Get interview prep learning statistics"""
        
        stats = self.learning_system.get_example_library_stats()
        analytics = self.learning_system.get_analytics_summary(module=self.module_name)
        
        return {
            'example_library': stats.get(self.module_name, {}),
            'analytics': analytics.get(self.module_name, {}),
            'timestamp': datetime.now().isoformat()
        }
    
    def _anonymize_job_description(self, job_desc: str, company_name: str = None) -> str:
        """Remove company-specific info from job description"""
        
        anonymized = job_desc
        
        if company_name:
            anonymized = anonymized.replace(company_name, '[COMPANY]')
        
        # Remove other identifying info
        # (This is simplified - could use data_anonymizer for thorough anonymization)
        
        return anonymized
    
    def _categorize_job(self, job_title: str) -> str:
        """Categorize job for better matching"""
        
        title_lower = job_title.lower()
        
        if any(word in title_lower for word in ['medical secretary', 'secretary']):
            return 'medical_secretary'
        elif any(word in title_lower for word in ['validation', 'rtt', 'pathway']):
            return 'rtt_validation'
        elif any(word in title_lower for word in ['healthcare assistant', 'hca', 'care assistant']):
            return 'healthcare_assistant'
        elif any(word in title_lower for word in ['teaching assistant', 'classroom']):
            return 'teaching_assistant'
        elif any(word in title_lower for word in ['admin', 'administrator']):
            return 'administration'
        else:
            return 'general'


# Global instance
interview_prep_rag = InterviewPrepRAG()


if __name__ == "__main__":
    # Test the RAG system
    print("T21 Interview Prep RAG System\n")
    
    # Simulate recording an interview outcome
    test_questions = [
        {'category': 'Technical', 'question': 'Can you explain your experience with medical terminology?'},
        {'category': 'Motivation', 'question': 'Why do you want this role?'},
        {'category': 'Competency', 'question': 'Describe a time you worked under pressure'}
    ]
    
    interview_prep_rag.record_interview_outcome(
        job_title="Medical Secretary",
        job_description="Looking for experienced medical secretary...",
        questions_generated=test_questions,
        questions_appeared=[
            'Can you explain your experience with medical terminology?',
            'Why do you want this role?'
        ],
        outcome="Got the job! 🎉",
        company_name="Test Hospital",
        industry="Healthcare"
    )
    
    print("Recorded test interview outcome\n")
    
    # Get stats
    stats = interview_prep_rag.get_learning_stats()
    print("Learning Statistics:")
    print(json.dumps(stats, indent=2))
    
    # Get insights
    insights = interview_prep_rag.get_success_insights("Medical Secretary")
    print("\nSuccess Insights:")
    for insight in insights:
        print(f"- {insight['message']}")


# Export
__all__ = ['interview_prep_rag', 'InterviewPrepRAG']
