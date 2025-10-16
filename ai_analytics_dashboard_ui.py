"""
AI ANALYTICS DASHBOARD UI
Track AI performance, user queries, and system improvements

🚀 COMPETITIVE ADVANTAGE: Data-driven AI improvement (like Sigma's tracking)
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from ai_query_analytics import (
    get_query_analytics,
    get_unanswered_queries,
    export_queries_to_json
)
from trust_customization_system import get_trust_from_email


def render_ai_analytics_dashboard():
    """Main AI analytics dashboard"""
    
    st.header("📊 AI Query Analytics Dashboard")
    
    st.success("""
    **🚀 COMPETITIVE ADVANTAGE:**
    Track every AI interaction to continuously improve responses!
    
    ✅ Monitor response times
    ✅ Track user satisfaction
    ✅ Identify knowledge gaps
    ✅ Improve AI accuracy
    """)
    
    # Date range selector
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        days = st.selectbox("Time Period", [7, 14, 30, 90, 365], index=2)
    with col2:
        user_email = st.session_state.get('user_email', '')
        trust_id = get_trust_from_email(user_email)
        filter_trust = st.checkbox("Filter by my Trust only", value=False)
    with col3:
        if st.button("🔄 Refresh"):
            st.rerun()
    
    # Get analytics
    analytics = get_query_analytics(
        days=days,
        trust_id=trust_id if filter_trust else None
    )
    
    # Key metrics
    st.markdown("### 📈 Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Queries",
            f"{analytics['total_queries']:,}",
            help="Total AI queries in selected period"
        )
    
    with col2:
        st.metric(
            "Avg Response Time",
            f"{analytics['avg_response_time']:.2f}s",
            help="Average time to generate response"
        )
    
    with col3:
        satisfaction_delta = analytics['satisfaction_rate'] - 80  # 80% is target
        st.metric(
            "Satisfaction Rate",
            f"{analytics['satisfaction_rate']:.1f}%",
            delta=f"{satisfaction_delta:+.1f}%",
            help="Percentage of queries marked as helpful"
        )
    
    with col4:
        st.metric(
            "Feedback Received",
            f"{analytics['feedback_count']}/{analytics['total_queries']}",
            help="Users who provided feedback"
        )
    
    st.markdown("---")
    
    # Tabs for different views
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Overview",
        "🏷️ Popular Topics",
        "📉 Problem Queries",
        "📅 Trends",
        "💡 Insights"
    ])
    
    with tab1:
        render_overview_tab(analytics)
    
    with tab2:
        render_topics_tab(analytics)
    
    with tab3:
        render_problem_queries_tab(days)
    
    with tab4:
        render_trends_tab(analytics)
    
    with tab5:
        render_insights_tab(analytics)


def render_overview_tab(analytics: dict):
    """Overview statistics"""
    
    st.subheader("📊 Query Overview")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📝 Query Characteristics")
        st.metric("Avg Query Length", f"{analytics['avg_query_length']:.0f} words")
        st.metric("Avg Response Length", f"{analytics['avg_response_length']:.0f} words")
        
        # Response quality
        if analytics['feedback_count'] > 0:
            feedback_rate = (analytics['feedback_count'] / analytics['total_queries'] * 100)
            st.metric("Feedback Rate", f"{feedback_rate:.1f}%")
    
    with col2:
        st.markdown("#### 🎯 Performance")
        
        # Response time rating
        rt = analytics['avg_response_time']
        if rt < 1.0:
            rt_rating = "🚀 Excellent"
        elif rt < 2.0:
            rt_rating = "✅ Good"
        elif rt < 3.0:
            rt_rating = "⚠️ Acceptable"
        else:
            rt_rating = "❌ Needs Improvement"
        
        st.write(f"**Response Speed:** {rt_rating}")
        
        # Satisfaction rating
        sat = analytics['satisfaction_rate']
        if sat >= 90:
            sat_rating = "🏆 Outstanding"
        elif sat >= 80:
            sat_rating = "✅ Good"
        elif sat >= 70:
            sat_rating = "⚠️ Fair"
        else:
            sat_rating = "❌ Poor"
        
        st.write(f"**User Satisfaction:** {sat_rating}")
    
    # Top users
    if analytics['top_users']:
        st.markdown("---")
        st.markdown("#### 👥 Most Active Users")
        for i, (user, count) in enumerate(analytics['top_users'][:5], 1):
            st.write(f"{i}. {user}: {count} queries")


def render_topics_tab(analytics: dict):
    """Popular topics and tags"""
    
    st.subheader("🏷️ Popular Topics")
    
    if not analytics['top_tags']:
        st.info("No tagged queries yet. Use the AI tutor to generate data!")
        return
    
    st.markdown("### Most Frequently Asked Topics")
    
    # Convert to dataframe for better display
    df_tags = pd.DataFrame(analytics['top_tags'], columns=['Topic', 'Count'])
    df_tags['Percentage'] = (df_tags['Count'] / analytics['total_queries'] * 100).round(1)
    
    # Display as table
    st.dataframe(
        df_tags,
        hide_index=True,
        use_container_width=True
    )
    
    # Common queries
    if analytics['common_queries']:
        st.markdown("---")
        st.markdown("### 💬 Most Common Questions")
        
        for i, (query, count) in enumerate(analytics['common_queries'][:10], 1):
            st.write(f"**{i}.** {query[:100]}... ({count} times)")


def render_problem_queries_tab(days: int):
    """Queries that weren't helpful"""
    
    st.subheader("📉 Problem Queries")
    
    st.info("""
    These queries were marked as **not helpful** by users.
    Review these to improve the AI's knowledge base.
    """)
    
    problem_queries = get_unanswered_queries(days=days)
    
    if not problem_queries:
        st.success("✅ No problem queries! All users found responses helpful.")
        return
    
    st.warning(f"⚠️ {len(problem_queries)} queries need attention")
    
    for i, q in enumerate(problem_queries[:20], 1):
        with st.expander(f"Query {i}: {q['query'][:80]}...", expanded=False):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**Query:** {q['query']}")
                st.markdown(f"**AI Response:** {q['response'][:300]}...")
                if q.get('feedback'):
                    st.markdown(f"**User Feedback:** {q['feedback']}")
            
            with col2:
                st.write(f"**Date:** {q['timestamp'][:10]}")
                st.write(f"**User:** {q.get('user_email', 'N/A')}")
            
            # Action buttons
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("📝 Improve Response", key=f"improve_{i}"):
                    st.info("💡 Add relevant Trust documents or SOPs to improve AI knowledge!")
            with col_b:
                if st.button("✅ Mark Resolved", key=f"resolve_{i}"):
                    st.success("Marked as resolved!")


def render_trends_tab(analytics: dict):
    """Query trends over time"""
    
    st.subheader("📅 Query Trends")
    
    if not analytics['queries_by_day']:
        st.info("Not enough data to show trends yet.")
        return
    
    # Convert to dataframe
    df_trends = pd.DataFrame(analytics['queries_by_day'], columns=['Date', 'Queries'])
    
    # Display as line chart
    st.line_chart(df_trends.set_index('Date'))
    
    st.markdown("---")
    st.markdown("### Daily Query Statistics")
    
    # Show table
    st.dataframe(
        df_trends.sort_values('Date', ascending=False),
        hide_index=True,
        use_container_width=True
    )


def render_insights_tab(analytics: dict):
    """AI-generated insights and recommendations"""
    
    st.subheader("💡 Insights & Recommendations")
    
    total = analytics['total_queries']
    
    if total == 0:
        st.info("No queries yet. Start using the AI tutor to generate insights!")
        return
    
    # Generate insights
    insights = []
    recommendations = []
    
    # Response time insights
    if analytics['avg_response_time'] > 3.0:
        insights.append("⚠️ **Slow Response Times:** Average response time is above 3 seconds")
        recommendations.append("🔧 Consider optimizing AI model or upgrading infrastructure")
    elif analytics['avg_response_time'] < 1.0:
        insights.append("✅ **Excellent Response Times:** AI responds in under 1 second")
    
    # Satisfaction insights
    if analytics['satisfaction_rate'] < 70:
        insights.append("❌ **Low Satisfaction:** Less than 70% of users find responses helpful")
        recommendations.append("📚 Add more Trust-specific documents to improve AI knowledge")
        recommendations.append("🔍 Review problem queries and improve training data")
    elif analytics['satisfaction_rate'] >= 90:
        insights.append("🏆 **Outstanding Satisfaction:** Over 90% of users satisfied")
    
    # Feedback rate insights
    feedback_rate = (analytics['feedback_count'] / total * 100) if total > 0 else 0
    if feedback_rate < 20:
        insights.append("📊 **Low Feedback Rate:** Only {feedback_rate:.0f}% of users provide feedback")
        recommendations.append("💬 Encourage users to provide feedback after each query")
    
    # Usage insights
    if total < 10:
        insights.append("📈 **Low Usage:** Limited AI query data available")
        recommendations.append("📢 Promote AI tutor to users - highlight benefits")
    elif total > 100:
        insights.append("🚀 **High Adoption:** Users are actively using the AI tutor")
    
    # Top topics insights
    if analytics['top_tags']:
        top_topic = analytics['top_tags'][0]
        insights.append(f"🔥 **Hottest Topic:** '{top_topic[0]}' ({top_topic[1]} queries)")
        recommendations.append(f"📖 Consider creating dedicated training module for '{top_topic[0]}'")
    
    # Display insights
    if insights:
        st.markdown("### 🔍 Key Insights")
        for insight in insights:
            st.markdown(f"- {insight}")
    
    if recommendations:
        st.markdown("---")
        st.markdown("### 🎯 Recommendations")
        for rec in recommendations:
            st.markdown(f"- {rec}")
    
    # Export option
    st.markdown("---")
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("📥 Export Data", type="primary"):
            with st.spinner("Exporting..."):
                export_path = export_queries_to_json(days=30)
                st.success(f"✅ Data exported to: {export_path}")
