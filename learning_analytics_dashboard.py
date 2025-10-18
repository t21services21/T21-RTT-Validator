"""
T21 LEARNING ANALYTICS DASHBOARD

Comprehensive analytics showing how the entire platform is learning and improving.

Shows:
- Overall platform learning statistics
- Module-by-module performance
- Improvement trends over time
- Coverage gaps and recommendations
- User contribution leaderboard
- Exportable reports

This is the "brain monitor" for the T21 learning system.
"""

import streamlit as st
from learning_system_core import learning_system
from letter_interpreter_rag import letter_rag
from interview_prep_rag import interview_prep_rag
from datetime import datetime, timedelta
import json
import sqlite3


def render_learning_analytics_dashboard():
    """
    Main analytics dashboard showing platform-wide learning
    """
    
    st.title("📊 Learning Analytics Dashboard")
    st.markdown("**Platform Intelligence - How T21 is Learning and Improving**")
    
    st.info("""
    🧠 **About This Dashboard:**
    This shows how the T21 platform is learning from user interactions across all modules.
    Every validation, every feedback, every success makes the system smarter!
    """)
    
    # Time period selector
    col1, col2, col3 = st.columns([2, 2, 2])
    
    with col1:
        time_period = st.selectbox(
            "📅 Time Period:",
            ["Last 7 Days", "Last 30 Days", "Last 90 Days", "All Time"],
            index=1
        )
    
    with col2:
        module_filter = st.selectbox(
            "📦 Module:",
            ["All Modules", "Letter Interpreter", "Interview Prep", "Certification", "RTT Training"],
            index=0
        )
    
    with col3:
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.rerun()
    
    # Convert time period to days
    days_map = {
        "Last 7 Days": 7,
        "Last 30 Days": 30,
        "Last 90 Days": 90,
        "All Time": 36500  # ~100 years
    }
    days = days_map[time_period]
    
    # Get overall stats
    overall_stats = get_overall_statistics(days)
    module_stats = get_module_breakdown(days)
    trends = get_improvement_trends(days)
    gaps = get_coverage_gaps()
    recommendations = generate_recommendations()
    
    # ===== OVERALL STATS =====
    st.markdown("---")
    st.subheader("📈 Overall Platform Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="📚 Total Examples",
            value=overall_stats['total_examples'],
            delta=f"+{overall_stats['examples_this_period']}" if overall_stats['examples_this_period'] > 0 else None
        )
    
    with col2:
        st.metric(
            label="💬 Total Feedbacks",
            value=overall_stats['total_feedbacks'],
            delta=f"+{overall_stats['feedbacks_this_period']}" if overall_stats['feedbacks_this_period'] > 0 else None
        )
    
    with col3:
        st.metric(
            label="🎯 Modules Learning",
            value=f"{overall_stats['active_modules']}/8",
            delta="Growing" if overall_stats['active_modules'] > 0 else None
        )
    
    with col4:
        if overall_stats['avg_improvement'] is not None:
            st.metric(
                label="📊 Avg Improvement",
                value=f"{overall_stats['avg_improvement']:.1f}%",
                delta="Improving" if overall_stats['avg_improvement'] > 0 else None
            )
        else:
            st.metric(
                label="📊 Avg Improvement",
                value="N/A",
                delta="Need more data"
            )
    
    # ===== MODULE BREAKDOWN =====
    st.markdown("---")
    st.subheader("📦 Module-by-Module Performance")
    
    if module_filter == "All Modules" or module_filter == "Letter Interpreter":
        render_letter_interpreter_stats(module_stats.get('letter_interpreter', {}), days)
    
    if module_filter == "All Modules" or module_filter == "Interview Prep":
        render_interview_prep_stats(module_stats.get('interview_prep', {}), days)
    
    if module_filter == "All Modules" or module_filter == "Certification":
        render_certification_stats(module_stats.get('certification', {}), days)
    
    # ===== IMPROVEMENT TRENDS =====
    st.markdown("---")
    st.subheader("📈 Improvement Trends")
    
    if trends['has_data']:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Accuracy Over Time:**")
            # Simple trend visualization
            for week, accuracy in trends['weekly_accuracy']:
                st.progress(accuracy / 100, text=f"Week {week}: {accuracy:.1f}%")
        
        with col2:
            st.markdown("**Example Growth:**")
            for week, count in trends['weekly_examples']:
                st.write(f"Week {week}: {count} examples")
    else:
        st.info("📊 Not enough data yet. Keep using the system to see trends!")
    
    # ===== COVERAGE GAPS =====
    st.markdown("---")
    st.subheader("⚠️ Coverage Gaps & Opportunities")
    
    if gaps:
        for gap in gaps:
            if gap['severity'] == 'high':
                st.error(f"🔴 **{gap['area']}:** {gap['description']}")
            elif gap['severity'] == 'medium':
                st.warning(f"🟡 **{gap['area']}:** {gap['description']}")
            else:
                st.info(f"🔵 **{gap['area']}:** {gap['description']}")
    else:
        st.success("✅ No major coverage gaps detected!")
    
    # ===== RECOMMENDATIONS =====
    st.markdown("---")
    st.subheader("💡 AI-Generated Recommendations")
    
    if recommendations:
        for rec in recommendations:
            with st.expander(f"{'🔥' if rec['priority'] == 'high' else '📌'} {rec['title']}", expanded=(rec['priority'] == 'high')):
                st.write(rec['description'])
                if rec.get('action'):
                    st.success(f"**Suggested Action:** {rec['action']}")
    else:
        st.info("System is learning well! No critical recommendations at this time.")
    
    # ===== USER CONTRIBUTIONS =====
    st.markdown("---")
    st.subheader("🏆 Top Contributors")
    st.caption("Users who have helped the system learn the most")
    
    contributors = get_top_contributors(days)
    if contributors:
        for i, contrib in enumerate(contributors[:10], 1):
            col1, col2, col3 = st.columns([1, 3, 2])
            with col1:
                st.write(f"#{i}")
            with col2:
                st.write(contrib['name'])
            with col3:
                st.write(f"{contrib['contributions']} contributions")
    else:
        st.info("Start contributing to see the leaderboard!")
    
    # ===== EXPORT OPTIONS =====
    st.markdown("---")
    st.subheader("📥 Export Analytics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📄 Export Full Report (PDF)", use_container_width=True):
            st.info("PDF export coming soon!")
    
    with col2:
        if st.button("📊 Export Data (CSV)", use_container_width=True):
            csv_data = export_to_csv(overall_stats, module_stats, days)
            st.download_button(
                label="⬇️ Download CSV",
                data=csv_data,
                file_name=f"t21_learning_analytics_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )
    
    with col3:
        if st.button("📋 Copy Summary", use_container_width=True):
            summary = generate_text_summary(overall_stats, module_stats, trends)
            st.code(summary, language=None)


def get_overall_statistics(days: int) -> dict:
    """Get overall platform-wide statistics"""
    
    try:
        stats = learning_system.get_example_library_stats()
        analytics = learning_system.get_analytics_summary(days=days)
        
        # Calculate totals
        total_examples = sum(mod.get('total_examples', 0) for mod in stats.values())
        total_feedbacks = sum(
            sum(metric.get('count', 0) for metric in mod_analytics.values())
            for mod_analytics in analytics.values()
        )
        
        # Active modules (with at least some examples)
        active_modules = len([mod for mod in stats.values() if mod.get('total_examples', 0) > 0])
        
        # Improvement calculation (simplified - would need more historical data)
        avg_improvement = None  # Placeholder
        
        return {
            'total_examples': total_examples,
            'examples_this_period': total_examples,  # Simplified
            'total_feedbacks': total_feedbacks,
            'feedbacks_this_period': total_feedbacks,  # Simplified
            'active_modules': active_modules,
            'avg_improvement': avg_improvement
        }
    except Exception as e:
        st.error(f"Error getting overall stats: {e}")
        return {
            'total_examples': 0,
            'examples_this_period': 0,
            'total_feedbacks': 0,
            'feedbacks_this_period': 0,
            'active_modules': 0,
            'avg_improvement': None
        }


def get_module_breakdown(days: int) -> dict:
    """Get detailed breakdown by module"""
    
    try:
        stats = learning_system.get_example_library_stats()
        analytics = learning_system.get_analytics_summary(days=days)
        
        return {
            'letter_interpreter': {
                'stats': stats.get('letter_interpreter', {}),
                'analytics': analytics.get('letter_interpreter', {})
            },
            'interview_prep': {
                'stats': stats.get('interview_prep', {}),
                'analytics': analytics.get('interview_prep', {})
            },
            'certification': {
                'stats': stats.get('certification', {}),
                'analytics': analytics.get('certification', {})
            }
        }
    except Exception as e:
        st.error(f"Error getting module breakdown: {e}")
        return {}


def render_letter_interpreter_stats(module_data: dict, days: int):
    """Render Letter Interpreter specific stats"""
    
    st.markdown("### 📝 Letter Interpreter")
    
    if not module_data or not module_data.get('stats'):
        st.info("No data yet. Start validating letters to see statistics!")
        return
    
    stats = module_data['stats']
    analytics = module_data.get('analytics', {})
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Validated Examples",
            stats.get('total_examples', 0)
        )
    
    with col2:
        correct = analytics.get('correct_interpretations', {}).get('total', 0)
        corrections = analytics.get('corrections_needed', {}).get('total', 0)
        total = correct + corrections
        accuracy = (correct / total * 100) if total > 0 else 0
        
        st.metric(
            "Accuracy",
            f"{accuracy:.1f}%",
            delta=f"{correct}/{total}" if total > 0 else None
        )
    
    with col3:
        categories = stats.get('categories', {})
        st.metric(
            "Letter Types",
            len(categories)
        )
    
    # Category breakdown
    if categories:
        st.markdown("**Coverage by Letter Type:**")
        for category, data in categories.items():
            st.write(f"• **{category.title()}:** {data.get('count', 0)} examples")


def render_interview_prep_stats(module_data: dict, days: int):
    """Render Interview Prep specific stats"""
    
    st.markdown("### 💼 Interview Prep")
    
    if not module_data or not module_data.get('stats'):
        st.info("No data yet. Submit interview feedback to see statistics!")
        return
    
    stats = module_data['stats']
    analytics = module_data.get('analytics', {})
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        interviews_reported = analytics.get('interviews_reported', {}).get('total', 0)
        st.metric(
            "Interviews Reported",
            interviews_reported
        )
    
    with col2:
        successful = analytics.get('successful_interviews', {}).get('total', 0)
        success_rate = (successful / interviews_reported * 100) if interviews_reported > 0 else 0
        
        st.metric(
            "Success Rate",
            f"{success_rate:.1f}%",
            delta=f"{successful} hired" if successful > 0 else None
        )
    
    with col3:
        st.metric(
            "Job Types",
            stats.get('total_examples', 0)
        )
    
    # Top job categories
    categories = stats.get('categories', {})
    if categories:
        st.markdown("**Most Common Job Types:**")
        sorted_cats = sorted(categories.items(), key=lambda x: x[1].get('count', 0), reverse=True)
        for category, data in sorted_cats[:5]:
            st.write(f"• **{category.replace('_', ' ').title()}:** {data.get('count', 0)} interviews")


def render_certification_stats(module_data: dict, days: int):
    """Render Certification specific stats"""
    
    st.markdown("### 🎓 Certification Exams")
    st.info("📊 Adaptive learning coming soon! This will track question difficulty and student performance.")


def get_improvement_trends(days: int) -> dict:
    """Calculate improvement trends over time"""
    
    # Placeholder - would need time-series data
    return {
        'has_data': False,
        'weekly_accuracy': [],
        'weekly_examples': []
    }


def get_coverage_gaps() -> list:
    """Identify coverage gaps in the learning system"""
    
    gaps = []
    
    try:
        stats = learning_system.get_example_library_stats()
        
        # Check letter interpreter coverage
        if 'letter_interpreter' in stats:
            categories = stats['letter_interpreter'].get('categories', {})
            
            if 'referral' not in categories or categories.get('referral', {}).get('count', 0) < 5:
                gaps.append({
                    'severity': 'high',
                    'area': 'Letter Interpreter - Referrals',
                    'description': 'Need more referral letter examples (less than 5 currently)'
                })
            
            if 'discharge' not in categories or categories.get('discharge', {}).get('count', 0) < 5:
                gaps.append({
                    'severity': 'medium',
                    'area': 'Letter Interpreter - Discharges',
                    'description': 'Need more discharge letter examples'
                })
        else:
            gaps.append({
                'severity': 'high',
                'area': 'Letter Interpreter',
                'description': 'No letter interpreter examples yet - start validating letters!'
            })
        
        # Check interview prep coverage
        if 'interview_prep' in stats:
            categories = stats['interview_prep'].get('categories', {})
            
            if len(categories) < 3:
                gaps.append({
                    'severity': 'medium',
                    'area': 'Interview Prep - Job Diversity',
                    'description': 'Limited job type diversity - encourage feedback for more roles'
                })
        else:
            gaps.append({
                'severity': 'medium',
                'area': 'Interview Prep',
                'description': 'No interview feedback yet - submit interview outcomes!'
            })
    
    except Exception as e:
        st.error(f"Error checking coverage gaps: {e}")
    
    return gaps


def generate_recommendations() -> list:
    """Generate AI recommendations based on current state"""
    
    recommendations = []
    
    try:
        stats = learning_system.get_example_library_stats()
        
        # Check overall progress
        total_examples = sum(mod.get('total_examples', 0) for mod in stats.values())
        
        if total_examples < 10:
            recommendations.append({
                'priority': 'high',
                'title': 'Build Initial Example Library',
                'description': 'You have less than 10 validated examples total. Focus on collecting examples across all modules.',
                'action': 'Validate 5-10 letters and submit 2-3 interview feedbacks this week'
            })
        elif total_examples < 50:
            recommendations.append({
                'priority': 'medium',
                'title': 'Expand Example Coverage',
                'description': 'Good start! Now focus on covering more letter types and job categories.',
                'action': 'Add examples for underrepresented categories'
            })
        else:
            recommendations.append({
                'priority': 'low',
                'title': 'Excellent Progress!',
                'description': f'You have {total_examples} examples. The system is learning well!',
                'action': 'Continue regular validation and feedback collection'
            })
        
        # Module-specific recommendations
        if 'letter_interpreter' in stats:
            categories = stats['letter_interpreter'].get('categories', {})
            if len(categories) < 4:
                recommendations.append({
                    'priority': 'medium',
                    'title': 'Diversify Letter Types',
                    'description': 'Focus on validating different letter types (referral, discharge, treatment, etc.)',
                    'action': 'Add at least 1 example of each major letter type'
                })
    
    except Exception as e:
        st.error(f"Error generating recommendations: {e}")
    
    return recommendations


def get_top_contributors(days: int) -> list:
    """Get top contributors (anonymized)"""
    
    # Placeholder - would need user tracking
    return []


def export_to_csv(overall_stats: dict, module_stats: dict, days: int) -> str:
    """Export analytics data to CSV"""
    
    csv_data = f"""T21 Learning Analytics Export
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Time Period: Last {days} days

OVERALL STATISTICS
Total Examples,{overall_stats['total_examples']}
Total Feedbacks,{overall_stats['total_feedbacks']}
Active Modules,{overall_stats['active_modules']}

MODULE BREAKDOWN
Module,Examples,Accuracy,Status
Letter Interpreter,{module_stats.get('letter_interpreter', {}).get('stats', {}).get('total_examples', 0)},N/A,Active
Interview Prep,{module_stats.get('interview_prep', {}).get('stats', {}).get('total_examples', 0)},N/A,Active
"""
    
    return csv_data


def generate_text_summary(overall_stats: dict, module_stats: dict, trends: dict) -> str:
    """Generate text summary for copying"""
    
    summary = f"""T21 LEARNING ANALYTICS SUMMARY
{'='*50}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

OVERALL PLATFORM:
• Total Examples: {overall_stats['total_examples']}
• Total Feedbacks: {overall_stats['total_feedbacks']}
• Active Modules: {overall_stats['active_modules']}/8

LETTER INTERPRETER:
• Examples: {module_stats.get('letter_interpreter', {}).get('stats', {}).get('total_examples', 0)}
• Status: {'Active' if module_stats.get('letter_interpreter') else 'No data'}

INTERVIEW PREP:
• Feedbacks: {module_stats.get('interview_prep', {}).get('stats', {}).get('total_examples', 0)}
• Status: {'Active' if module_stats.get('interview_prep') else 'No data'}

The T21 platform is learning and improving!
{'='*50}
"""
    
    return summary


# Export
__all__ = ['render_learning_analytics_dashboard']
